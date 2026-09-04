import json
from pathlib import Path

from src.ui.control_center.binding_registry import build_binding_registry
from src.ui.control_center.decision_explanation_builder import build_safe_decision_explanation_payload
from src.ui.control_center.model import UIIntent, build_control_center
from src.ui.control_center.runtime_sources import build_runtime_source_registry
from src.ui.control_center.runtime_status_adapter import build_runtime_status_snapshot


ROOT = Path(__file__).parents[1]


def _lock():
    return json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))


def test_live_lock_flags_are_closed():
    lock = _lock()
    assert lock["LIVE_TRADING"] is False
    assert lock["live_order_sending_allowed"] is False
    assert lock["ui_can_enable_live"] is False
    assert lock["telegram_can_enable_live"] is False
    assert lock["codex_can_enable_live"] is False
    assert lock["requires_separate_live_gate"] is True


def test_trade_mode_is_paper():
    config = json.loads((ROOT / "config/trade_config.json").read_text(encoding="utf-8"))
    assert config["mode"] == "PAPER"


def test_builder_has_no_action_authority():
    values = build_safe_decision_explanation_payload().to_dict()
    assert values["can_execute"] is False
    assert values["can_start_paper"] is False
    assert values["can_start_live"] is False
    assert values["can_send_order"] is False
    assert values["live_lock_state"] == "OFF_LOCKED"
    assert values["paper_execution_readiness"] == "NOT_ALLOWED_YET"


def test_ready_injection_remains_non_executable():
    values = build_safe_decision_explanation_payload(runtime_snapshot={"candle_closed": True, "risk_permission": "ALLOWED", "final_decision": "READY"}).to_dict()
    assert values["final_decision"] == "READY"
    assert values["can_execute"] is False


def test_fail_closed_reasons():
    assert build_safe_decision_explanation_payload().to_dict()["no_trade_reason"] == "PENDING_PROVIDER"
    assert build_safe_decision_explanation_payload(runtime_snapshot={"failure_state": "STALE", "health": {"state": "STALE"}}).to_dict()["no_trade_reason"] == "STALE_DATA"
    assert build_safe_decision_explanation_payload(runtime_snapshot={"health": {"state": "READY"}}).to_dict()["no_trade_reason"] == "CLOSED_CANDLE_REQUIRED"
    assert build_safe_decision_explanation_payload(runtime_snapshot={"candle_closed": True, "risk_permission": "BLOCKED", "health": {"state": "READY"}}).to_dict()["no_trade_reason"] == "RISK_NOT_ALLOWED"


def test_runtime_adapter_is_locked_and_passive():
    snapshot = build_runtime_status_snapshot(config_path=ROOT / "config/live_lock_config.json")
    assert snapshot["LIVE_TRADING"] is False
    assert snapshot["live_order_sending_allowed"] is False
    assert snapshot["live"] == "OFF_LOCKED"
    assert snapshot["execution_triggered"] is False
    assert snapshot["paper_start_triggered"] is False
    assert snapshot["live_order_sent"] is False


def test_binding_registry_is_passive():
    bindings = build_binding_registry()
    assert len(bindings) == 17
    assert all(item.read_only and item.display_only for item in bindings)
    assert all(not item.can_execute and not item.can_start_paper and not item.can_start_live and not item.can_call_network and not item.can_send_order for item in bindings)


def test_source_registry_has_no_active_capability_or_scheduler_start():
    sources = build_runtime_source_registry()
    assert all(item.read_only for item in sources)
    assert all(not item.can_execute and not item.can_start_paper and not item.can_start_live and not item.can_call_network and not item.can_send_order for item in sources)


def test_ui_intent_is_paper_only_and_not_live_order():
    intent = UIIntent("START")
    assert intent.paper_only is True
    assert intent.live_order_sent is False
    assert build_control_center().live_controls_passive is True
    assert build_control_center().live_controls_locked is True


def test_guard_sources_contain_no_forbidden_client_or_process_imports():
    files = [ROOT / "src/ui/control_center/runtime_status_adapter.py", ROOT / "src/ui/control_center/runtime_sources.py", ROOT / "src/ui/control_center/binding_registry.py", ROOT / "src/ui/control_center/ui_snapshot_binding_adapter.py"]
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi")
    for path in files:
        source = path.read_text(encoding="utf-8").lower()
        assert not any(token in source for token in forbidden)
