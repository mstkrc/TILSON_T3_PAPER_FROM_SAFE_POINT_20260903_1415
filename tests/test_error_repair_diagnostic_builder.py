from pathlib import Path

import pytest

from src.ui.control_center.error_repair_diagnostic_builder import (
    build_safe_error_repair_diagnostic_payload,
    get_error_repair_blocked_by,
    get_error_repair_fail_closed_reason,
    validate_error_repair_diagnostic_payload,
)
from src.ui.control_center.error_repair_diagnostic_schema import ERROR_REPAIR_DIAGNOSTIC_FIELDS


def _ready(**extra):
    value = {"overall_diagnostic_status": "PASS", "health_state": "READY", "error_state": "NONE", "source_freshness": "FRESH"}
    value.update(extra)
    return value


def test_default_payload_has_50_fields_and_validates():
    payload = build_safe_error_repair_diagnostic_payload()
    assert len(payload.to_dict()) == 50
    assert tuple(payload.to_dict()) == ERROR_REPAIR_DIAGNOSTIC_FIELDS
    assert validate_error_repair_diagnostic_payload(payload)


def test_defaults_are_read_only_and_safe():
    values = build_safe_error_repair_diagnostic_payload().to_dict()
    assert values["display_only"] is True and values["read_only"] is True
    assert values["can_recommend_manual_repair"] is True and values["manual_repair_allowed"] is True
    for name in ("can_execute_repair", "can_auto_repair", "can_restore_recovery", "can_write_file", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "auto_repair_allowed", "repair_execution_allowed", "recovery_restore_allowed"):
        assert values[name] is False
    assert values["operator_message"] == "MANUAL_REVIEW_REQUIRED"


@pytest.mark.parametrize("extra,expected", [
    ({"health_state": "CRITICAL"}, "CRITICAL_HEALTH"),
    ({"live_lock_violation_detected": True}, "LIVE_LOCK_VIOLATION"),
    ({"config_mismatch_detected": True}, "CONFIG_MISMATCH"),
    ({"runtime_exception_detected": True}, "RUNTIME_EXCEPTION"),
    ({"missing_provider_detected": True}, "MISSING_PROVIDER"),
    ({"source_freshness": "STALE"}, "STALE_DATA"),
    ({"ledger_mismatch_detected": True}, "LEDGER_MISMATCH"),
    ({"position_mismatch_detected": True}, "POSITION_MISMATCH"),
    ({"pnl_mismatch_detected": True}, "PNL_MISMATCH"),
    ({"scheduler_stopped_detected": True}, "SCHEDULER_STOPPED"),
    ({"paper_engine_stopped_detected": True}, "PAPER_ENGINE_STOPPED"),
    ({"ui_render_failure_detected": True}, "UI_RENDER_FAILURE"),
])
def test_fail_closed_reasons(extra, expected):
    value = _ready(**extra)
    payload = build_safe_error_repair_diagnostic_payload(value, value, value, value)
    assert get_error_repair_fail_closed_reason(payload) == expected


def test_provider_pending_and_unknown_are_safe():
    pending = build_safe_error_repair_diagnostic_payload({}, {}, {}, {})
    assert get_error_repair_fail_closed_reason(pending) == "MISSING_PROVIDER"
    unknown = build_safe_error_repair_diagnostic_payload(_ready(overall_diagnostic_status="BLOCKED"), _ready(overall_diagnostic_status="BLOCKED"), _ready(overall_diagnostic_status="BLOCKED"), _ready(overall_diagnostic_status="BLOCKED"))
    assert get_error_repair_fail_closed_reason(unknown) == "DIAGNOSTIC_NOT_PROVEN"


def test_priority_is_deterministic():
    value = _ready(health_state="CRITICAL", live_lock_violation_detected=True, config_mismatch_detected=True, source_freshness="STALE")
    assert get_error_repair_fail_closed_reason(build_safe_error_repair_diagnostic_payload(value, value, value, value)) == "CRITICAL_HEALTH"


def test_injected_authority_is_overridden_and_blocked_by_is_list():
    value = _ready(can_execute_repair=True, can_auto_repair=True, can_restore_recovery=True, can_write_file=True, can_execute=True, can_start_paper=True, can_start_live=True, can_send_order=True, auto_repair_allowed=True, repair_execution_allowed=True, recovery_restore_allowed=True)
    payload = build_safe_error_repair_diagnostic_payload(value, value, value, value)
    values = payload.to_dict()
    assert all(values[name] is False for name in ("can_execute_repair", "can_auto_repair", "can_restore_recovery", "can_write_file", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "auto_repair_allowed", "repair_execution_allowed", "recovery_restore_allowed"))
    assert get_error_repair_blocked_by(payload) == []
    assert validate_error_repair_diagnostic_payload(payload)


def test_builder_source_has_no_external_clients_or_writes():
    source = (Path(__file__).parents[1] / "src/ui/control_center/error_repair_diagnostic_builder.py").read_text(encoding="utf-8").lower()
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi", "write_text", "write_bytes")
    assert not any(item in source for item in forbidden)
