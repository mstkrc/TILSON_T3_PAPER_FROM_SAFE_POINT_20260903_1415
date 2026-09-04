from pathlib import Path

import pytest

from src.ui.control_center.binding_registry import build_binding_registry
from src.ui.control_center.decision_explanation_builder import build_safe_decision_explanation_payload
from src.ui.control_center.model import UIIntent, build_control_center
from src.ui.control_center.runtime_sources import build_runtime_source_registry


ROOT = Path(__file__).parents[1]


def test_start_intent_is_paper_only_and_never_sends():
    intent = UIIntent("START")
    assert intent.paper_only is True
    assert intent.live_order_sent is False


def test_live_start_like_input_cannot_create_live_action():
    with pytest.raises(ValueError):
        build_control_center().intent("LIVE_START")


def test_control_center_live_controls_are_passive_and_locked():
    model = build_control_center()
    assert model.live_controls_passive is True
    assert model.live_controls_locked is True


def test_control_center_readiness_is_blocked_without_all_checks():
    model = build_control_center()
    result = model.readiness({})
    assert result["passed"] is False
    assert result["paper_start_intent_allowed"] is False


def test_all_screen_bindings_have_no_action_authority():
    bindings = build_binding_registry()
    assert len(bindings) == 17
    assert all(not item.can_execute for item in bindings)
    assert all(not item.can_start_paper for item in bindings)
    assert all(not item.can_start_live for item in bindings)
    assert all(not item.can_send_order for item in bindings)


def test_all_runtime_sources_have_no_action_authority():
    sources = build_runtime_source_registry()
    assert all(not item.can_execute for item in sources)
    assert all(not item.can_start_paper for item in sources)
    assert all(not item.can_start_live for item in sources)
    assert all(not item.can_send_order for item in sources)


def test_payload_has_no_action_authority():
    values = build_safe_decision_explanation_payload().to_dict()
    assert values["can_execute"] is False
    assert values["can_start_paper"] is False
    assert values["can_start_live"] is False
    assert values["can_send_order"] is False


def test_ready_injection_cannot_grant_execution():
    values = build_safe_decision_explanation_payload(runtime_snapshot={"final_decision": "READY", "candle_closed": True, "risk_permission": "ALLOWED"}).to_dict()
    assert values["can_execute"] is False


def test_live_lock_injection_cannot_grant_live_start():
    values = build_safe_decision_explanation_payload(runtime_snapshot={"live_lock_state": "ON", "candle_closed": True, "risk_permission": "ALLOWED"}).to_dict()
    assert values["can_start_live"] is False


def test_paper_ready_injection_cannot_grant_paper_start():
    values = build_safe_decision_explanation_payload(runtime_snapshot={"paper_execution_readiness": "READY", "candle_closed": True, "risk_permission": "ALLOWED"}).to_dict()
    assert values["can_start_paper"] is False


@pytest.mark.parametrize("field", ("can_execute", "can_send_order", "can_start_live", "can_start_paper"))
def test_injected_action_flags_are_overridden(field):
    values = build_safe_decision_explanation_payload(runtime_snapshot={field: True}).to_dict()
    assert values[field] is False


def test_tested_action_files_have_no_external_execution_clients():
    paths = [
        ROOT / "src/ui/control_center/binding_registry.py",
        ROOT / "src/ui/control_center/runtime_sources.py",
        ROOT / "src/ui/control_center/runtime_status_adapter.py",
        ROOT / "src/ui/control_center/ui_snapshot_binding_adapter.py",
        ROOT / "src/ui/control_center/decision_explanation_builder.py",
        ROOT / "src/ui/control_center/decision_explanation_schema.py",
    ]
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi")
    for path in paths:
        source = path.read_text(encoding="utf-8").lower()
        assert not any(item in source for item in forbidden)
