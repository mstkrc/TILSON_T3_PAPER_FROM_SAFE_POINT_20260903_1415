"""Atomic persistence for paper-only execution results."""
from __future__ import annotations
import json
import os
from pathlib import Path

def _save(path: Path, value: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)

def persist_entry(state_dir: Path, result, source: str = "FULL_UNIVERSE_SCAN") -> None:
    if not result.paper_only or result.live_order_sent or result.execution_status != "FILLED":
        raise ValueError("PAPER_EXECUTION_RESULT_NOT_SAFE")
    positions_path=state_dir/"positions.json"; ledger_path=state_dir/"ledger.json"; events_path=state_dir/"events.json"
    positions=json.loads(positions_path.read_text(encoding="utf-8")); ledger=json.loads(ledger_path.read_text(encoding="utf-8")); events=json.loads(events_path.read_text(encoding="utf-8"))
    if any(x.get("execution_id")==result.execution_id for x in ledger.get("fills",[])): raise ValueError("DUPLICATE_EXECUTION_ID")
    fill={"execution_id":result.execution_id,"symbol":result.symbol,"direction":result.direction,"side":"BUY" if result.direction=="LONG" else "SELL","price":str(result.fill_price),"quantity":str(result.quantity),"notional_usd":str(result.fill_price*result.quantity),"fee":str(result.taker_fee_estimate),"realized_pnl":0,"paper_only":True,"live_order_sent":False}
    position={"symbol":result.symbol,"direction":result.direction,"entry_price":str(result.fill_price),"quantity":str(result.quantity),"notional_usd":str(result.fill_price*result.quantity),"paper_execution_id":result.execution_id,"source":source,"paper_only":True,"is_open":True}
    ledger.setdefault("fills",[]).append(fill); positions.setdefault("positions",[]).append(position); events.setdefault("events",[]).append({"type":"PAPER_ORDER_CREATED","execution_id":result.execution_id,"symbol":result.symbol,"direction":result.direction,"paper_only":True,"live_order_sent":False})
    _save(ledger_path,ledger); _save(positions_path,positions); _save(events_path,events)
