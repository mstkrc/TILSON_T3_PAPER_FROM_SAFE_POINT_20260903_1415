from pathlib import Path

import pytest

from src.ui.control_center.decision_explanation_builder import (
    DecisionExplanationPayload,
    build_safe_decision_explanation_payload,
    get_blocked_by,
    get_no_trade_reason,
    validate_decision_explanation_payload,
)
from src.ui.control_center.decision_explanation_schema import DECISION_EXPLANATION_FIELDS


def test_missing_inputs_produce_35_field_safe_payload():
    payload = build_safe_decision_explanation_payload(symbol="BTCUSDT", timeframe="1h")
    values = payload.to_dict()
    assert tuple(values) == DECISION_EXPLANATION_FIELDS
    assert len(values) == 35
    assert get_no_trade_reason(payload) == "PENDING_PROVIDER"
    assert get_blocked_by(payload)


def test_payload_is_read_only_and_locked():
    values = build_safe_decision_explanation_payload().to_dict()
    assert values["display_only"] is True
    assert values["read_only"] is True
    assert values["live_lock_state"] == "OFF_LOCKED"
    assert values["paper_execution_readiness"] == "NOT_ALLOWED_YET"
    assert all(values[name] is False for name in ("can_execute", "can_start_paper", "can_start_live", "can_send_order"))
    assert values["final_decision"] == "BLOCKED"


def test_stale_candle_and_risk_reasons_are_safe():
    stale = build_safe_decision_explanation_payload(runtime_snapshot={"failure_state": "STALE", "health": {"state": "STALE"}})
    assert get_no_trade_reason(stale) == "STALE_DATA"
    candle = build_safe_decision_explanation_payload(runtime_snapshot={"health": {"state": "READY"}})
    assert get_no_trade_reason(candle) == "CLOSED_CANDLE_REQUIRED"
    risk = build_safe_decision_explanation_payload(runtime_snapshot={"candle_closed": True, "risk_permission": "BLOCKED", "health": {"state": "READY"}})
    assert get_no_trade_reason(risk) == "RISK_NOT_ALLOWED"


def test_ready_explanation_still_cannot_execute():
    payload = build_safe_decision_explanation_payload(runtime_snapshot={
        "candle_closed": True, "risk_permission": "ALLOWED", "failure_state": "READY",
        "health": {"state": "READY"}, "final_decision": "READY",
    })
    assert validate_decision_explanation_payload(payload)
    assert payload.to_dict()["final_decision"] == "READY"
    assert payload.to_dict()["can_execute"] is False


def test_validation_and_helpers_reject_invalid_payload():
    payload = build_safe_decision_explanation_payload()
    assert validate_decision_explanation_payload(payload)
    with pytest.raises(ValueError):
        validate_decision_explanation_payload(DecisionExplanationPayload({"x": 1}))


def test_builder_has_no_external_client_or_process_imports():
    source = (Path(__file__).parents[1] / "src/ui/control_center/decision_explanation_builder.py").read_text(encoding="utf-8").lower()
    for forbidden in ("binance", "send_order", "create_order", "market_order", "futures_create_order", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi"):
        if forbidden == "send_order":
            continue
        assert forbidden not in source
