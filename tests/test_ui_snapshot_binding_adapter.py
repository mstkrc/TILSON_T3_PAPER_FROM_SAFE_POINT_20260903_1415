import pytest

from src.ui.control_center.ui_snapshot_binding_adapter import (
    build_bound_ui_snapshot,
    get_screen_bound_snapshot,
    validate_bound_ui_snapshot,
)


def _runtime_state(failure_state="UNKNOWN", **domains):
    snapshot = {
        "generated_at": "2026-09-04T00:00:00+00:00",
        "paper": "OFF",
        "live": "OFF_LOCKED",
        "LIVE_TRADING": False,
        "live_order_sending_allowed": False,
        "failure_state": failure_state,
    }
    snapshot.update({key: {"state": value} for key, value in domains.items()})
    return snapshot


def test_bound_snapshot_has_seventeen_safe_screens():
    bound = build_bound_ui_snapshot()
    assert len(bound["screens"]) == 17
    assert validate_bound_ui_snapshot(bound)
    for screen in bound["screens"].values():
        assert screen["read_only"] is True
        assert screen["display_only"] is True
        assert screen["decision_allowed"] is False
        assert screen["execution_triggered"] is False
        assert screen["paper_start_triggered"] is False
        assert screen["live_order_sent"] is False


def test_blocked_runtime_failure_blocks_every_screen():
    bound = build_bound_ui_snapshot(runtime_snapshot=_runtime_state("BLOCKED"))
    assert all(screen["fallback_state"] == "BLOCKED" for screen in bound["screens"].values())


def test_stale_source_is_visible_on_related_screen():
    bound = build_bound_ui_snapshot(runtime_snapshot=_runtime_state("STALE", health="STALE"))
    assert bound["screens"]["09 Health"]["fallback_state"] == "STALE"


def test_unknown_sources_use_safe_binding_fallback_and_ready_is_display_only():
    unknown = build_bound_ui_snapshot(runtime_snapshot=_runtime_state())
    assert unknown["screens"]["08 Risk"]["fallback_state"] == "BLOCKED"
    ready = build_bound_ui_snapshot(runtime_snapshot=_runtime_state(
        "READY", scheduler="READY", candle="READY", strategy="READY", candidate="READY", risk="READY",
        execution="READY", ledger="READY", positions="READY", health="READY",
    ))
    assert ready["screens"]["01 Overview"]["fallback_state"] == "READY"
    assert ready["screens"]["01 Overview"]["decision_allowed"] is False


def test_get_screen_bound_snapshot_and_invalid_snapshot_validation():
    screen = get_screen_bound_snapshot("17 Notifications")
    assert screen["screen_name"] == "17 Notifications"
    with pytest.raises(KeyError):
        get_screen_bound_snapshot("99 Missing")
    with pytest.raises(ValueError):
        validate_bound_ui_snapshot({"screens": {}})
