from pathlib import Path

from src.ui.control_center.error_repair_diagnostic_schema import (
    ERROR_REPAIR_DIAGNOSTIC_FIELDS,
    build_error_repair_diagnostic_schema,
    get_required_error_repair_diagnostic_fields,
    validate_error_repair_diagnostic_schema,
)


def test_schema_has_50_fields_in_exact_order_and_all_required():
    schema = build_error_repair_diagnostic_schema()
    assert len(schema.fields) == 50
    assert tuple(field.name for field in schema.fields) == ERROR_REPAIR_DIAGNOSTIC_FIELDS
    assert len(set(ERROR_REPAIR_DIAGNOSTIC_FIELDS)) == 50
    assert all(field.required for field in schema.fields)


def test_schema_validation_and_required_fields_pass():
    schema = build_error_repair_diagnostic_schema()
    assert validate_error_repair_diagnostic_schema(schema)
    assert get_required_error_repair_diagnostic_fields() == ERROR_REPAIR_DIAGNOSTIC_FIELDS


def test_repair_and_action_fallbacks_are_safe():
    values = {field.name: field.fallback_value for field in build_error_repair_diagnostic_schema().fields}
    assert values["display_only"] is True and values["read_only"] is True
    assert values["can_recommend_manual_repair"] is True and values["manual_repair_allowed"] is True
    for name in ("can_execute_repair", "can_auto_repair", "can_restore_recovery", "can_write_file", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "auto_repair_allowed", "repair_execution_allowed", "recovery_restore_allowed"):
        assert values[name] is False
    assert values["system_mode"] == "PAPER"
    assert values["diagnostic_provider_status"] == values["repair_provider_status"] == values["error_event_provider_status"] == "PENDING"
    assert values["health_state"] == values["error_state"] == values["severity"] == "UNKNOWN"
    assert values["overall_diagnostic_status"] == "BLOCKED"
    assert values["fail_closed_reason"] == values["blocked_by"] == "DIAGNOSTIC_NOT_PROVEN"
    assert values["next_allowed_action"] == "DISPLAY_ONLY_REVIEW"
    assert values["operator_message"] == "MANUAL_REVIEW_REQUIRED"


def test_schema_has_no_external_clients_or_mutating_runtime():
    source = (Path(__file__).parents[1] / "src/ui/control_center/error_repair_diagnostic_schema.py").read_text(encoding="utf-8").lower()
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi")
    assert not any(item in source for item in forbidden)
