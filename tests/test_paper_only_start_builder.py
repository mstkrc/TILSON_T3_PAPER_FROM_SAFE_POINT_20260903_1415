from pathlib import Path
from src.ui.control_center.paper_only_start_builder import *
from src.ui.control_center.paper_only_start_schema import PAPER_ONLY_START_FIELDS

def test_default_payload_is_45_and_ordered():
    p=build_safe_paper_only_start_payload(); assert len(p.to_dict())==45; assert tuple(p.to_dict())==PAPER_ONLY_START_FIELDS; assert validate_paper_only_start_payload(p)

def test_safe_defaults_and_forced_authority():
    p=build_safe_paper_only_start_payload({"live_trading_flag":True,"live_order_sending_allowed":True,"paper_start_allowed":True,"requested_mode":"LIVE"}); v=p.to_dict(); assert v["requested_mode"]=="PAPER" and v["effective_mode"]=="PAPER"; assert all(v[x] is False for x in PAPER_ONLY_START_FORCED_FALSE_FIELDS); assert v["paper_start_permission"]=="NOT_GRANTED_YET"; assert v["real_order_capability"]=="NONE"; assert get_paper_only_start_blocking_reason(p)=="LIVE_LOCK_VIOLATION"

def test_fallbacks_and_required_true():
    v=build_safe_paper_only_start_payload().to_dict(); assert v["candle_wait_state"]=="WAITING_FOR_CLOSED_CANDLE"; assert v["operator_message"]=="GATED_BUILDER_READY_NO_START"; assert v["next_allowed_action"]=="REVIEW_GATED_BUILDER_BEFORE_CONTROLLED_START"; assert all(v[x] is True for x in PAPER_ONLY_START_REQUIRED_TRUE_FIELDS)

def test_priority_reasons():
    cases=[({"real_order_capability":"FOUND"},"REAL_ORDER_ENDPOINT_DETECTED"),({"requested_mode":"LIVE"},"NON_PAPER_MODE_REQUESTED"),({},"OPEN_CANDLE_OR_UNKNOWN_CANDLE")]
    for req,expected in cases:
        runtime = {} if expected == "OPEN_CANDLE_OR_UNKNOWN_CANDLE" else {"candle_wait_state":"CLOSED_CANDLE_READY","current_candle_state":"CLOSED"}
        assert get_paper_only_start_blocking_reason(build_safe_paper_only_start_payload(req, runtime, {}))==expected

def test_all_lower_priority_blocks():
    base={"candle_wait_state":"CLOSED_CANDLE_READY","current_candle_state":"CLOSED","risk_gate_status":"PASS","diagnostic_status":"PASS","ledger_consistency_status":"PASS","position_consistency_status":"PASS","pnl_consistency_status":"PASS"}
    for key,expected in [("risk_gate_status","RISK_GATE_NOT_PASS"),("diagnostic_status","DIAGNOSTIC_NOT_PASS"),("ledger_consistency_status","LEDGER_NOT_CONSISTENT"),("position_consistency_status","POSITION_NOT_CONSISTENT"),("pnl_consistency_status","PNL_NOT_CONSISTENT")]:
        q=dict(base);q[key]="FAIL";assert get_paper_only_start_blocking_reason(build_safe_paper_only_start_payload(q,q,q))==expected

def test_helpers_and_no_forbidden_runtime_paths():
    p=build_safe_paper_only_start_payload(); assert get_paper_only_start_next_allowed_action(p)=="REVIEW_GATED_BUILDER_BEFORE_CONTROLLED_START"; s=Path(__file__).parents[1].joinpath("src/ui/control_center/paper_only_start_builder.py").read_text(encoding="utf-8").lower(); forbidden=("binance","send_order","create_order","market_order","futures_create_order","requests","httpx","websocket","ccxt","subprocess","os.system","start_server","uvicorn","flask","fastapi","live_trading = true","live_order_sending_allowed = true"); assert not any(x in s for x in forbidden)
