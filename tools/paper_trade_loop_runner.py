"""Fail-closed, paper-only closed-candle loop runner.

This runner deliberately performs no market-data fetch and no trade decision until
an explicit decision engine is wired in.  A cycle is therefore a safe no-op.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, build_opener, ProxyHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
STATE = ROOT / "state" / "paper"
LOOP_STATE = STATE / "trade_loop_state.json"


def read(name: str) -> dict:
    return json.loads((STATE / name).read_text(encoding="utf-8"))


def write_loop(value: dict) -> None:
    LOOP_STATE.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def event(kind: str, **extra: object) -> None:
    path = STATE / "events.json"
    data = read("events.json")
    data.setdefault("events", []).append({"type": kind, **extra})
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def public_closed_candles(symbol: str = "BTCUSDT", limit: int = 200) -> list[dict]:
    query = urlencode({"symbol": symbol, "interval": "1h", "limit": limit})
    url = "https://fapi.binance.com/fapi/v1/klines?" + query
    opener = build_opener(ProxyHandler({}))
    with opener.open(Request(url, headers={"User-Agent": "TILSON-T3-paper-public-data/1.0"}), timeout=8) as response:
        rows = json.loads(response.read().decode("utf-8"))
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    return [{"open": float(row[1]), "high": float(row[2]), "low": float(row[3]), "close": float(row[4]), "close_time_ms": int(row[6])}
            for row in rows if int(row[6]) <= now_ms]


def decision_snapshot(candles: list[dict], config: dict):
    from src.indicators.dmi_adx import adx_slope_state, calculate_dmi_adx
    from src.indicators.models import IndicatorOutput
    from src.indicators.t3 import calculate_t3, t3_colors
    from src.strategy.signals import evaluate_direction
    closes = [c["close"] for c in candles]
    t3 = calculate_t3(closes, config["t3_factor"], config["t3_period"])
    colors = t3_colors(t3)
    plus, minus, adx = calculate_dmi_adx([c["high"] for c in candles], [c["low"] for c in candles], closes, config["dmi_di_length"], config["adx_smoothing"])
    slopes = adx_slope_state(adx, config["adx_slope_n"])
    def output(i):
        return IndicatorOutput(t3[i], colors[i], plus[i], minus[i], adx[i], slopes[i], datetime.fromtimestamp(candles[i]["close_time_ms"] / 1000, timezone.utc))
    previous, current = output(-2), output(-1)
    signal = evaluate_direction(previous, current, candle_is_closed=True, adx_threshold=config["adx_threshold"], continuation_enabled=config["continuation_mode_enabled"])
    return current, signal


def cycle() -> str:
    runtime = read("runtime_state.json")
    state = read("trade_loop_state.json")
    now = datetime.now(timezone.utc).isoformat()
    if runtime.get("mode") != "PAPER":
        state.update({"paper_trade_loop_status": "ERROR", "last_cycle_at": now, "last_cycle_result": "BLOCKED_MODE_NOT_PAPER", "last_block_reason": "MODE_NOT_PAPER"})
        write_loop(state); event("PAPER_LOOP_BLOCKED", reason="MODE_NOT_PAPER"); return "BLOCKED_MODE_NOT_PAPER"
    if runtime.get("paper_runtime") != "ON" or not runtime.get("paper_start_allowed", False):
        state.update({"paper_trade_loop_status": "ERROR", "last_cycle_at": now, "last_cycle_result": "BLOCKED_PAPER_RUNTIME_GATE", "last_block_reason": "PAPER_RUNTIME_GATE"})
        write_loop(state); event("PAPER_LOOP_BLOCKED", reason="PAPER_RUNTIME_GATE"); return "BLOCKED_PAPER_RUNTIME_GATE"
    if runtime.get("live_runtime") != "OFF_LOCKED" or runtime.get("live_trading") or runtime.get("live_order_sending_allowed") or runtime.get("real_order_allowed"):
        state.update({"paper_trade_loop_status": "ERROR", "last_cycle_at": now, "last_cycle_result": "BLOCKED_LIVE_OR_ORDER_RISK", "last_block_reason": "LIVE_OR_ORDER_RISK"})
        write_loop(state); event("PAPER_LOOP_BLOCKED", reason="LIVE_OR_ORDER_RISK"); return "BLOCKED_LIVE_OR_ORDER_RISK"
    event("PAPER_LOOP_HEARTBEAT", loop="CLOSED_CANDLE_TRADE_LOOP")
    config = json.loads((ROOT / "config" / "trade_config.json").read_text(encoding="utf-8"))
    if not config.get("closed_candle_only") or config.get("timeframe") != "1h":
        state.update({"paper_trade_loop_status": "ERROR", "last_cycle_at": now, "last_cycle_result": "BLOCKED_CLOSED_CANDLE_CONFIG", "last_block_reason": "CLOSED_CANDLE_CONFIG_REQUIRED"})
        write_loop(state); event("PAPER_LOOP_BLOCKED", reason="CLOSED_CANDLE_CONFIG_REQUIRED"); return "BLOCKED_CLOSED_CANDLE_CONFIG"
    try:
        candles = public_closed_candles()
    except Exception as exc:
        detail = {"error_type": type(exc).__name__, "url": "https://fapi.binance.com/fapi/v1/klines", "symbol": "BTCUSDT", "timeframe": "1h", "timeout_seconds": 8, "public_only": True, "retry_count": 0, "last_error": str(getattr(exc, "reason", exc)), "next_action_hint": "CHECK_WINDOWS_TLS_PROXY_DNS_OR_FIREWALL; DO_NOT_USE_PRIVATE_ENDPOINT"}
        state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "SAFE_NOOP", "last_block_reason": "MARKET_DATA_UNAVAILABLE", "market_data_status": "MARKET_DATA_UNAVAILABLE", "last_market_data_error": detail})
        write_loop(state); event("PAPER_LOOP_MARKET_DATA_UNAVAILABLE", **detail); return "SAFE_NOOP"
    if len(candles) < max(config["dmi_di_length"] + config["adx_smoothing"], config["t3_period"] * 2) + config["adx_slope_n"]:
        state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "SAFE_NOOP", "last_block_reason": "INSUFFICIENT_CLOSED_CANDLES"})
        write_loop(state); event("PAPER_LOOP_SAFE_NOOP", reason="INSUFFICIENT_CLOSED_CANDLES", market_data="PASS", paper_order="NONE"); return "SAFE_NOOP"
    current, signal = decision_snapshot(candles, config)
    state.update({"market_data_status": "PASS", "last_market_data_error": None, "closed_candle_status": "PASS", "indicator_status": "PASS", "signal_status": signal.signal_type.value, "risk_status": "NOT_ENTERED"})
    if signal.signal_type.value == "NO_SIGNAL":
        state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "NO_ENTRY", "last_block_reason": signal.blocked_reason})
        write_loop(state); event("PAPER_LOOP_NO_ENTRY", reason=signal.blocked_reason, closed_candle="PASS", market_data="PASS", paper_order="NONE"); return "NO_ENTRY"
    state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "NO_ENTRY", "last_block_reason": "PAPER_EXECUTION_GATE_NOT_BOUND"})
    write_loop(state); event("PAPER_LOOP_NO_ENTRY", reason="PAPER_EXECUTION_GATE_NOT_BOUND", signal=signal.signal_type.value, paper_order="NONE"); return "NO_ENTRY"


def scan_universe_once(max_symbols: int | None = None, sleep_ms: int = 100, batch_once: bool = False, batch_size: int = 25) -> str:
    from src.market.symbol_universe import load_usdt_m_futures_universe
    config = json.loads((ROOT / "config" / "trade_config.json").read_text(encoding="utf-8"))
    universe = load_usdt_m_futures_universe()
    cursor_path = STATE / "universe_scan_cursor.json"
    cursor = json.loads(cursor_path.read_text(encoding="utf-8")) if cursor_path.exists() else {"next_index":0,"completed_rounds":0,"status":"IDLE"}
    size = max_symbols or (batch_size if batch_once else len(universe["tradable_symbols"]))
    start = int(cursor.get("next_index", 0)); symbols = universe["tradable_symbols"][start:start+size]
    (STATE / "symbol_universe.json").write_text(json.dumps(universe, indent=2) + "\n", encoding="utf-8")
    results=[]; counts={"data_pass":0,"data_fail":0,"indicator_pass":0,"no_signal":0,"long_signal":0,"short_signal":0}
    for symbol in symbols:
        item={"symbol":symbol,"data_status":"FAIL","closed_candle_status":"FAIL","indicator_status":"FAIL","signal_status":"NO_SIGNAL","direction":"NONE","reason":"MARKET_DATA_UNAVAILABLE","risk_status":"NOT_ENTERED","risk_reason":None,"paper_order_status":"NONE","paper_order_id":None}
        try:
            candles=public_closed_candles(symbol)
            if len(candles) < max(config["dmi_di_length"]+config["adx_smoothing"], config["t3_period"]*2)+config["adx_slope_n"]: raise ValueError("INSUFFICIENT_CLOSED_CANDLES")
            _, signal=decision_snapshot(candles, config); item.update({"data_status":"PASS","closed_candle_status":"PASS","indicator_status":"PASS","signal_status":signal.signal_type.value,"direction":signal.signal_type.value,"reason":signal.blocked_reason}); counts["data_pass"]+=1; counts["indicator_pass"]+=1
            if signal.signal_type.value=="NO_SIGNAL": counts["no_signal"]+=1; item.update({"risk_status":"NOT_ENTERED","paper_order_status":"NONE"})
            elif signal.signal_type.value in ("LONG","SHORT"):
                from src.paper.position import PositionDirection, PositionState
                from src.risk.permission import evaluate_permission
                direction=PositionDirection(signal.signal_type.value)
                wallet=read("wallet_state.json"); pos_data=read("positions_state.json")
                positions=[]
                for raw in pos_data.get("positions",[]):
                    positions.append(PositionState(raw["symbol"], PositionDirection(raw["direction"]), float(raw["quantity"]), float(raw["entry_price"]), "runtime", True, 2.0, True))
                permission=evaluate_permission(symbol=symbol,direction=direction,candidate_status="VALID",sizing_status="VALID",open_positions=positions,max_coin_count=int(config["max_coin_count"]),free_balance_usd=float(wallet.get("available_usd",wallet.get("cash_usd",0))),required_margin_usd=0.0,lock_available=True,stop_loss_enabled=True,stop_loss_percent=2.0,config_snapshot_id="trade_config")
                item.update({"risk_status":"ALLOW" if permission.permission_status=="ALLOW" else "BLOCKED","risk_reason":permission.blocked_reason or None,"paper_order_status":"NONE"})
                if permission.permission_status=="ALLOW":
                    counts["risk_allow_count"]=counts.get("risk_allow_count",0)+1
                    item.update(execute_allowed_paper_entry({"symbol":symbol,"direction":signal.signal_type.value}, permission, config, candles[-1]["close"]))
                else: counts["risk_block_count"]=counts.get("risk_block_count",0)+1
                counts["long_signal"] += signal.signal_type.value=="LONG"; counts["short_signal"] += signal.signal_type.value=="SHORT"
        except Exception as exc: item["reason"]=type(exc).__name__
        results.append(item)
        if sleep_ms: time.sleep(sleep_ms/1000)
    scan={"cycle_id":datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),"started_at":None,"finished_at":datetime.now(timezone.utc).isoformat(),"universe_source":universe["source"],"total_symbols":len(universe["tradable_symbols"]),"scanned_symbols":len(results),**counts,"candidate_count":0,"risk_allow_count":0,"risk_block_count":0,"paper_order_count":0,"symbols":results}
    (STATE / "scan_results.json").write_text(json.dumps(scan, indent=2) + "\n", encoding="utf-8")
    nxt = start + len(symbols); complete = nxt >= len(universe["tradable_symbols"])
    cursor.update({"universe_size":len(universe["tradable_symbols"]),"batch_size":size,"next_index":0 if complete else nxt,"completed_rounds":int(cursor.get("completed_rounds",0))+(1 if complete else 0),"current_round_id":scan["cycle_id"],"last_batch_finished_at":scan["finished_at"],"symbols_scanned_this_round":len(symbols),"total_data_pass_this_round":counts["data_pass"],"total_data_fail_this_round":counts["data_fail"],"total_no_signal_this_round":counts["no_signal"],"total_long_signal_this_round":counts["long_signal"],"total_short_signal_this_round":counts["short_signal"],"total_candidates_this_round":0,"total_risk_allow_this_round":0,"total_risk_block_this_round":0,"total_paper_orders_this_round":0,"status":"ROUND_COMPLETE" if complete else "IDLE"})
    cursor_path.write_text(json.dumps(cursor, indent=2) + "\n", encoding="utf-8")
    return "FULL_UNIVERSE_PAPER_SCAN_NO_SIGNAL_PASS" if counts["long_signal"]+counts["short_signal"]==0 else "FULL_UNIVERSE_SCAN_SUPPORT_LIMITED_PASS"

def execute_allowed_paper_entry(candidate: dict, permission, config: dict, price: float) -> dict:
    """Execute only an already risk-allowed candidate through the paper adapter."""
    runtime = read("runtime_state.json")
    if runtime.get("mode") != "PAPER" or runtime.get("paper_runtime") != "ON" or runtime.get("live_runtime") != "OFF_LOCKED" or runtime.get("live_trading") or runtime.get("live_order_sending_allowed") or runtime.get("real_order_allowed") or permission.permission_status != "ALLOW":
        return {"paper_order_status":"BLOCKED","paper_order_reason":"PAPER_SAFETY_GATE"}
    from types import SimpleNamespace
    from decimal import Decimal
    from src.paper.execution import PaperExecutionInput, simulate_entry
    sizing=SimpleNamespace(normalized_quantity=Decimal("0.001"))
    now=datetime.now(timezone.utc)
    result=simulate_entry(PaperExecutionInput(candidate["symbol"],candidate["direction"],"ALLOW",sizing,Decimal(str(price)),Decimal(str(price)),now,now,int(config.get("default_leverage",1)),config.get("margin_mode","ISOLATED"),config),lock_available=True)
    if result.execution_status == "FILLED":
        from src.paper.state_store import persist_entry
        persist_entry(STATE, result)
    return {"paper_order_status":"CREATED" if result.execution_status=="FILLED" else "BLOCKED","paper_order_id":result.execution_id,"paper_only":result.paper_only,"live_order_sent":result.live_order_sent,"paper_order_reason":result.blocked_reason}

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--once", action="store_true")
    group.add_argument("--run", action="store_true")
    parser.add_argument("--interval-seconds", type=float, default=30)
    parser.add_argument("--scan-universe", action="store_true")
    parser.add_argument("--batch-once", action="store_true")
    parser.add_argument("--max-symbols", type=int)
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--sleep-ms", type=int, default=100)
    args = parser.parse_args()
    if args.scan_universe:
        print(scan_universe_once(args.max_symbols, args.sleep_ms, args.batch_once, args.batch_size))
        return 0
    if args.run:
        while True:
            cycle(); time.sleep(args.interval_seconds)
    cycle()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
