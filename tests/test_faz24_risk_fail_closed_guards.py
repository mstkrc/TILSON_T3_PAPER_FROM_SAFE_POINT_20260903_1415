import json
from pathlib import Path

from src.ui.control_center.decision_explanation_builder import build_safe_decision_explanation_payload
from src.ui.control_center.decision_explanation_schema import build_decision_explanation_schema


ROOT = Path(__file__).parents[1]


def _values(snapshot=None):
    return build_safe_decision_explanation_payload(runtime_snapshot=snapshot).to_dict()


def test_missing_runtime_is_pending_provider():
    assert _values()["no_trade_reason"] == "PENDING_PROVIDER"


def test_stale_runtime_is_stale_data():
    assert _values({"failure_state": "STALE", "health": {"state": "STALE"}})["no_trade_reason"] == "STALE_DATA"


def test_open_candle_is_blocked():
    assert _values({"health": {"state": "READY"}})["no_trade_reason"] == "CLOSED_CANDLE_REQUIRED"


def test_blocked_risk_is_blocked():
    assert _values({"candle_closed": True, "risk_permission": "BLOCKED", "health": {"state": "READY"}})["no_trade_reason"] == "RISK_NOT_ALLOWED"


def test_unknown_risk_is_blocked():
    assert _values({"candle_closed": True, "risk_permission": "UNKNOWN", "health": {"state": "READY"}})["no_trade_reason"] == "RISK_NOT_ALLOWED"


def test_ledger_blocked_is_not_ready():
    values = _values({"candle_closed": True, "risk_permission": "ALLOWED", "ledger_consistency": "BLOCKED", "health": {"state": "READY"}})
    assert values["final_decision"] == "BLOCKED" or values["blocked_by"]


def test_health_critical_is_not_ready():
    values = _values({"candle_closed": True, "risk_permission": "ALLOWED", "health_state": "CRITICAL", "health": {"state": "CRITICAL"}})
    assert values["final_decision"] == "BLOCKED" or values["blocked_by"]


def test_ready_cannot_execute():
    assert _values({"candle_closed": True, "risk_permission": "ALLOWED", "final_decision": "READY"})["can_execute"] is False


def test_ready_cannot_send():
    assert _values({"candle_closed": True, "risk_permission": "ALLOWED", "final_decision": "READY"})["can_send_order"] is False


def test_ready_cannot_start_paper():
    assert _values({"candle_closed": True, "risk_permission": "ALLOWED", "final_decision": "READY"})["can_start_paper"] is False


def test_ready_cannot_start_live():
    assert _values({"candle_closed": True, "risk_permission": "ALLOWED", "final_decision": "READY"})["can_start_live"] is False


def test_locked_action_is_display_only():
    values = _values({"live_lock_state": "OFF_LOCKED"})
    assert values["next_allowed_action"] == "DISPLAY_ONLY_REVIEW"


def test_no_action_authority_implies_no_real_capability():
    values = _values()
    assert not any(values[key] for key in ("can_execute", "can_send_order", "can_start_live"))


def test_schema_fallbacks_are_fail_closed():
    values = {field.name: field.fallback_value for field in build_decision_explanation_schema().fields}
    assert values["final_decision"] == "BLOCKED"
    assert values["candle_closed"] is False
    assert values["live_lock_state"] == "OFF_LOCKED"
    assert values["paper_execution_readiness"] == "NOT_ALLOWED_YET"


def test_reason_priority_is_deterministic():
    assert _values()["no_trade_reason"] == "PENDING_PROVIDER"
    assert _values({"failure_state": "STALE", "health": {"state": "STALE"}})["no_trade_reason"] == "STALE_DATA"
    assert _values({"health": {"state": "READY"}})["no_trade_reason"] == "CLOSED_CANDLE_REQUIRED"
    assert _values({"candle_closed": True, "risk_permission": "BLOCKED", "health": {"state": "READY"}})["no_trade_reason"] == "RISK_NOT_ALLOWED"


def test_live_lock_config_remains_closed():
    lock = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert lock["LIVE_TRADING"] is False
    assert lock["live_order_sending_allowed"] is False


def test_trade_config_remains_paper():
    config = json.loads((ROOT / "config/trade_config.json").read_text(encoding="utf-8"))
    assert config["mode"] == "PAPER"


def test_guard_sources_have_no_external_clients_or_processes():
    paths = [ROOT / "src/ui/control_center/decision_explanation_builder.py", ROOT / "src/ui/control_center/decision_explanation_schema.py", ROOT / "src/ui/control_center/runtime_status_adapter.py"]
    forbidden = ("binance", "requests", "httpx", "websocket", "ccxt", "subprocess", "os.system", "start_server", "uvicorn", "flask", "fastapi")
    for path in paths:
        text = path.read_text(encoding="utf-8").lower()
        assert not any(item in text for item in forbidden)
