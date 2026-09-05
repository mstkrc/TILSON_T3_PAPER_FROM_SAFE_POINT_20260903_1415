"""Fail-closed, paper-only closed-candle loop runner.

This runner deliberately performs no market-data fetch and no trade decision until
an explicit decision engine is wired in.  A cycle is therefore a safe no-op.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import urlopen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
    with urlopen("https://fapi.binance.com/fapi/v1/klines?" + query, timeout=8) as response:
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
    if signal.signal_type.value == "NO_SIGNAL":
        state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "NO_ENTRY", "last_block_reason": signal.blocked_reason})
        write_loop(state); event("PAPER_LOOP_NO_ENTRY", reason=signal.blocked_reason, closed_candle="PASS", market_data="PASS", paper_order="NONE"); return "NO_ENTRY"
    state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "NO_ENTRY", "last_block_reason": "PAPER_EXECUTION_GATE_NOT_BOUND"})
    write_loop(state); event("PAPER_LOOP_NO_ENTRY", reason="PAPER_EXECUTION_GATE_NOT_BOUND", signal=signal.signal_type.value, paper_order="NONE"); return "NO_ENTRY"


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--once", action="store_true")
    group.add_argument("--run", action="store_true")
    parser.add_argument("--interval-seconds", type=float, default=30)
    args = parser.parse_args()
    if args.run:
        while True:
            cycle(); time.sleep(args.interval_seconds)
    cycle()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
