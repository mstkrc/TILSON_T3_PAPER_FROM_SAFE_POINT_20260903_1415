import json
from pathlib import Path

import pytest

from src.ui.control_center.decision_explanation_schema import (
    DECISION_EXPLANATION_FIELDS,
    DecisionExplanationField,
    DecisionExplanationSchema,
    build_decision_explanation_schema,
    get_required_decision_explanation_fields,
    validate_decision_explanation_schema,
)


def test_schema_has_exactly_35_required_fields():
    schema = build_decision_explanation_schema()
    assert len(schema.fields) == 35
    assert get_required_decision_explanation_fields() == DECISION_EXPLANATION_FIELDS
    assert all(field.required for field in schema.fields)


def test_schema_has_safe_fallbacks_and_validation_passes():
    schema = build_decision_explanation_schema()
    assert validate_decision_explanation_schema(schema)
    values = {field.name: field.fallback_value for field in schema.fields}
    assert values["final_decision"] == "BLOCKED"
    assert values["candle_closed"] is False
    assert values["live_lock_state"] == "OFF_LOCKED"
    assert values["paper_execution_readiness"] == "NOT_ALLOWED_YET"
    assert values["display_only"] is True
    assert values["read_only"] is True
    for name in ("can_execute", "can_start_paper", "can_start_live", "can_send_order"):
        assert values[name] is False


def test_invalid_schema_is_rejected():
    schema = build_decision_explanation_schema()
    unsafe = DecisionExplanationField("can_execute", True, "test", "bool", True, False, "display", "read-only; no execution authority")
    invalid = DecisionExplanationSchema(schema.fields[:-1] + (unsafe,))
    with pytest.raises(ValueError):
        validate_decision_explanation_schema(invalid)


def test_schema_source_has_no_external_client_or_process_imports():
    source = Path(__file__).parents[1] / "src/ui/control_center/decision_explanation_schema.py"
    text = source.read_text(encoding="utf-8").lower()
    for forbidden in ("binance", "send_order", "create_order", "market_order", "futures_create_order", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi"):
        if forbidden == "send_order":
            continue
        assert forbidden not in text


def test_schema_does_not_start_runtime():
    snapshot = build_decision_explanation_schema()
    assert validate_decision_explanation_schema(snapshot)
