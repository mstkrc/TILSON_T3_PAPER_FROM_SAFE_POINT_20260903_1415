from pathlib import Path

from src.ui.control_center.ledger_pnl_position_schema import (
    LEDGER_PNL_POSITION_FIELDS,
    build_ledger_pnl_position_schema,
    get_required_ledger_pnl_position_fields,
    validate_ledger_pnl_position_schema,
)


def test_schema_has_exact_45_fields_in_contract_order():
    schema = build_ledger_pnl_position_schema()
    assert len(schema.fields) == 45
    assert tuple(field.name for field in schema.fields) == LEDGER_PNL_POSITION_FIELDS
    assert len(set(LEDGER_PNL_POSITION_FIELDS)) == 45


def test_all_fields_required_and_validation_passes():
    schema = build_ledger_pnl_position_schema()
    assert all(field.required for field in schema.fields)
    assert validate_ledger_pnl_position_schema(schema)
    assert get_required_ledger_pnl_position_fields() == LEDGER_PNL_POSITION_FIELDS


def test_safety_and_consistency_fallbacks_are_closed():
    values = {field.name: field.fallback_value for field in build_ledger_pnl_position_schema().fields}
    expected_true = ("display_only", "read_only")
    expected_false = ("can_write_ledger", "can_mutate_position", "can_recalculate_authoritatively", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "paper_ledger_write_allowed", "live_ledger_write_allowed")
    assert all(values[name] is True for name in expected_true)
    assert all(values[name] is False for name in expected_false)
    assert values["system_mode"] == "PAPER"
    assert all(values[name] == "PENDING" for name in ("ledger_provider_status", "pnl_provider_status", "position_provider_status"))
    assert values["ledger_consistency"] == values["pnl_consistency"] == values["position_consistency"] == "UNKNOWN"
    assert values["overall_consistency"] == "BLOCKED"
    assert values["fail_closed_reason"] == values["blocked_by"] == "CONSISTENCY_NOT_PROVEN"
    assert values["next_allowed_action"] == "DISPLAY_ONLY_REVIEW"


def test_schema_has_no_external_clients_or_runtime_authority():
    source = (Path(__file__).parents[1] / "src/ui/control_center/ledger_pnl_position_schema.py").read_text(encoding="utf-8").lower()
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi", "calculate_pnl")
    assert not any(item in source for item in forbidden)
