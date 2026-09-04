import json
from datetime import datetime, timezone
from pathlib import Path

from src.ui.control_center.model import ControlCenterModel
from src.ui.control_center.runtime_status_adapter import build_runtime_status_snapshot


ROOT = Path(__file__).parents[1]


def test_snapshot_is_read_only_and_live_locked():
    snapshot = build_runtime_status_snapshot(now=datetime(2026, 9, 4, tzinfo=timezone.utc))

    assert snapshot["LIVE_TRADING"] is False
    assert snapshot["live_order_sending_allowed"] is False
    assert snapshot["paper"] == "OFF"
    assert snapshot["live"] == "OFF_LOCKED"
    assert snapshot["data_binding"] == "DESIGN_READY_NOT_IMPLEMENTED"
    assert snapshot["failure_state"] == "UNKNOWN"
    assert snapshot["decision_allowed"] is False
    assert snapshot["execution_triggered"] is False
    assert snapshot["live_order_sent"] is False
    assert snapshot["paper_start_triggered"] is False


def test_missing_sources_are_unknown_and_stale_or_blocked_are_explicit():
    snapshot = build_runtime_status_snapshot(
        stale_domains=("health",),
        blocked_domains=("risk",),
    )

    assert snapshot["health"]["state"] == "STALE"
    assert snapshot["risk"]["state"] == "BLOCKED"
    assert snapshot["scheduler"]["state"] == "UNKNOWN"
    assert snapshot["failure_state"] == "BLOCKED"


def test_runtime_sources_are_values_only_and_bind_snapshot_compatible():
    snapshot = build_runtime_status_snapshot(runtime_sources={"health": {"healthy": True}})
    bound = ControlCenterModel(top_status={}).bind_snapshot(snapshot)

    assert bound["snapshot"] is snapshot
    assert bound["decision_allowed"] is False
    assert snapshot["health"]["state"] == "READY"
    assert snapshot["health"]["value"] == {"healthy": True}


def test_live_lock_config_is_read_only_and_has_no_order_authority():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    snapshot = build_runtime_status_snapshot()

    assert config["LIVE_TRADING"] is False
    assert config["live_order_sending_allowed"] is False
    assert snapshot["live_order_sent"] is False
    assert snapshot["execution_triggered"] is False
