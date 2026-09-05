"""Fail-closed, paper-only closed-candle loop runner.

This runner deliberately performs no market-data fetch and no trade decision until
an explicit decision engine is wired in.  A cycle is therefore a safe no-op.
"""
from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
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
    state.update({"paper_trade_loop_status": "SAFE_NOOP", "last_cycle_at": now, "last_cycle_result": "SAFE_NOOP", "last_block_reason": "PAPER_LOOP_NO_DECISION_ENGINE_AVAILABLE"})
    write_loop(state)
    event("PAPER_LOOP_HEARTBEAT", loop="CLOSED_CANDLE_TRADE_LOOP")
    event("PAPER_LOOP_SAFE_NOOP", reason="PAPER_LOOP_NO_DECISION_ENGINE_AVAILABLE", market_data="NOT_STARTED", paper_order="NONE")
    return "SAFE_NOOP"


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
