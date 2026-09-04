from pathlib import Path
from src.ui.control_center.paper_only_start_schema import *

def test_schema_has_exact_45_fields_and_order():
    s=build_paper_only_start_schema(); assert len(s.fields)==45; assert tuple(x.name for x in s.fields)==PAPER_ONLY_START_FIELDS; assert len(set(PAPER_ONLY_START_FIELDS))==45

def test_all_required_and_validates():
    s=build_paper_only_start_schema(); assert all(x.required for x in s.fields); assert validate_paper_only_start_schema(s)

def test_safe_fallbacks():
    expected={"requested_mode":"PAPER","effective_mode":"PAPER","paper_start_permission":"NOT_GRANTED_YET","paper_start_allowed":False,"live_start_allowed":False,"order_send_allowed":False,"config_write_allowed":False,"ledger_write_allowed":False,"position_mutation_allowed":False,"live_lock_status":"OFF_LOCKED","live_trading_flag":False,"live_order_sending_allowed":False,"ui_can_enable_live":False,"telegram_can_enable_live":False,"codex_can_enable_live":False,"requires_separate_live_gate":True,"real_order_capability":"NONE","execution_network_status":"NONE","order_endpoint_status":"NONE","closed_candle_rule":"REQUIRED","required_timeframe":"1H_CLOSED_CANDLE","candle_wait_state":"WAITING_FOR_CLOSED_CANDLE","blocking_reason":"PAPER_START_NOT_GRANTED_YET","next_allowed_action":"IMPLEMENT_PAPER_ONLY_START_GATED_PATH"}
    for k,v in expected.items(): assert SAFE_PAPER_ONLY_START_FALLBACKS[k]==v
    for k in ("audit_event_required","report_required","snapshot_required","rollback_reference_required"): assert SAFE_PAPER_ONLY_START_FALLBACKS[k] is True

def test_required_fields_returns_contract():
    assert get_required_paper_only_start_fields()==PAPER_ONLY_START_FIELDS and len(get_required_paper_only_start_fields())==45

def test_source_has_no_forbidden_runtime_paths():
    source=Path(__file__).parents[1].joinpath("src/ui/control_center/paper_only_start_schema.py").read_text(encoding="utf-8").lower()
    forbidden=("binance","send_order","create_order","market_order","futures_create_order","requests","httpx","websocket","ccxt","subprocess","os.system","start_server","uvicorn","flask","fastapi","live_trading = true","live_order_sending_allowed = true")
    assert not any(x in source for x in forbidden)

