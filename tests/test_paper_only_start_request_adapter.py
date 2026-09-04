from pathlib import Path
from src.ui.control_center.paper_only_start_request_adapter import *
from src.ui.control_center.paper_only_start_schema import PAPER_ONLY_START_FIELDS

def test_default_result_is_blocked_and_safe():
    r=build_ui_paper_start_request_payload(); assert r.status=="BLOCKED"; assert r.blocking_reason=="PAPER_START_NOT_GRANTED_YET"; assert r.operator_message=="UI_PAPER_START_REQUEST_ADAPTER_READY_NO_START"; assert r.next_allowed_action=="REVIEW_ADAPTER_BEFORE_CONTROLLED_START"; assert validate_ui_paper_start_request_payload(r)

def test_payload_is_45_fields_and_schema_ordered():
    r=build_ui_paper_start_request_payload(); assert len(r.payload)==45; assert tuple(r.payload)==PAPER_ONLY_START_FIELDS

def test_adapter_uses_safe_builder_and_forces_flags():
    r=build_ui_paper_start_request_payload({"requested_mode":"LIVE","live_trading_flag":True,"live_order_sending_allowed":True,"paper_start_allowed":True,"real_order_capability":"FOUND"});v=r.payload; assert v["requested_mode"]=="PAPER" and v["effective_mode"]=="PAPER" and v["paper_start_permission"]=="NOT_GRANTED_YET"; assert v["paper_start_allowed"] is False and v["live_start_allowed"] is False and v["order_send_allowed"] is False; assert v["real_order_capability"]=="NONE"; assert r.blocking_reason=="LIVE_LOCK_VIOLATION"

def test_candle_and_gate_blocks():
    for req,reason in [({},"PAPER_START_NOT_GRANTED_YET"),({"requested_mode":"LIVE"},"NON_PAPER_MODE_REQUESTED"),({"risk_gate_status":"FAIL"},"PAPER_START_NOT_GRANTED_YET"),({"diagnostic_status":"FAIL"},"PAPER_START_NOT_GRANTED_YET"),({"ledger_consistency_status":"FAIL"},"PAPER_START_NOT_GRANTED_YET"),({"position_consistency_status":"FAIL"},"PAPER_START_NOT_GRANTED_YET"),({"pnl_consistency_status":"FAIL"},"PAPER_START_NOT_GRANTED_YET")]:
        runtime={} if not req else {"candle_wait_state":"CLOSED_CANDLE_READY","current_candle_state":"CLOSED"}
        r=build_ui_paper_start_request_payload(req,runtime,{});assert r.blocking_reason==reason

def test_runtime_pending_and_accessors():
    r=build_ui_paper_start_request_payload({}, {"runtime_provider_status":"PENDING","candle_wait_state":"CLOSED_CANDLE_READY","current_candle_state":"CLOSED"}, {}); assert r.blocking_reason=="PAPER_START_NOT_GRANTED_YET"; assert get_ui_paper_start_blocking_reason(r)==r.blocking_reason; assert get_ui_paper_start_operator_message(r)==r.operator_message; assert get_ui_paper_start_next_allowed_action(r)==r.next_allowed_action

def test_adapter_source_has_no_forbidden_paths_or_callable_names():
    s=Path(__file__).parents[1].joinpath("src/ui/control_center/paper_only_start_request_adapter.py").read_text(encoding="utf-8").lower();forbidden=("binance","send_order","create_order","market_order","futures_create_order","requests","httpx","websocket","ccxt","subprocess","os.system","start_server","uvicorn","flask","fastapi","live_trading = true","live_order_sending_allowed = true");assert not any(x in s for x in forbidden);assert "start_paper" not in s and "start_server" not in s and "start_scheduler" not in s and "execute" not in s
