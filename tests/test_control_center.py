"""Phase-13 Control Center model validation; no UI screen, export, or live action."""

import json
from datetime import timedelta
from pathlib import Path

from src.ui.control_center import (CONTROL_BUTTONS, INTELLIGENCE_FIELDS, MARKET_COLUMNS, RISK_FIELDS,
                                   STATE_LIFECYCLE, SUMMARY_CARDS, LAYOUT_SECTIONS, build_control_center)
from src.ui.control_center_render import render_control_center

ROOT = Path(__file__).parents[1]

def test_html_render_contains_reference_sections_and_paper_lock():
    html = render_control_center(build_control_center())
    assert "GRAF" in html
    assert "PAPER EXECUTION / LEDGER" in html
    assert "LIVE" in html
    assert "LIVE_TRADING=false" in html
    assert "disabled" in html


def test_main_model_and_top_status_bar():
    model = build_control_center()
    assert all(field in model.top_status for field in ("algorithm", "mode", "market", "data", "engine", "scheduler", "health", "clock"))
    assert model.top_status["mode"] == "PAPER"


def test_panels_columns_and_lifecycle():
    model = build_control_center()
    assert set(MARKET_COLUMNS) <= set(model.market_columns)
    assert set(STATE_LIFECYCLE) == set(model.state_lifecycle)
    assert set(INTELLIGENCE_FIELDS) <= set(model.intelligence_fields)
    assert set(RISK_FIELDS) <= set(model.risk_fields)
    assert "paper_only" in model.execution_fields


def test_buttons_live_locked_and_main_page_separation():
    model = build_control_center()
    assert set(CONTROL_BUTTONS) == set(model.control_buttons)
    assert model.live_controls_locked
    assert not model.optimization_on_main_page
    assert not model.report_excel_on_main_page
    assert not model.telegram_commands_enabled
    assert model.live_controls_visible and model.live_controls_passive


def test_reference_layout_sections_and_summary_cards():
    model = build_control_center()
    assert set(LAYOUT_SECTIONS) <= set(model.layout_sections)
    assert set(SUMMARY_CARDS) <= set(model.summary_cards)
    assert "Dashboard / Ana Sayfa" in model.sidebar_items
    assert model.paper_mode_label == "PAPER MODE"


def test_refresh_is_two_minutes_and_no_decision():
    model = build_control_center()
    assert model.refresh_interval == timedelta(minutes=2)
    result = model.display_refresh({"health": "GREEN"})
    assert not result["decision_allowed"] and not result["execution_triggered"]


def test_operational_pipeline_readiness_and_safe_intent():
    model = build_control_center()
    assert "CANDIDATE" in model.pipeline_stages
    assert "STOP_AND_REPORT" in model.health_fields
    assert not model.readiness({item: False for item in model.readiness_checks})["paper_start_intent_allowed"]
    assert model.intent("PANIC").requires_confirmation
    assert not model.bind_snapshot({"net_pnl": 1})["decision_allowed"]


def test_live_lock_and_no_external_endpoints():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/ui").glob("*telegram*"))
    assert not list((ROOT / "src/ui").glob("*excel*"))
    assert not list((ROOT / "src/ui").glob("*order*"))


def test_narrow_ui_simulation_refresh_and_route_navigation_are_display_only():
    model = build_control_center()
    refreshed = model.display_refresh({"failure_state": "UNKNOWN"})

    assert refreshed["decision_allowed"] is False
    assert refreshed["execution_triggered"] is False
    assert model.active_screen in model.screens
    assert len(model.screens) >= 11


def test_narrow_ui_simulation_buttons_do_not_execute():
    model = build_control_center()

    for action in model.control_buttons:
        intent = model.intent(action)
        assert intent.paper_only is True
        assert intent.live_order_sent is False


def test_narrow_ui_simulation_unknown_stale_and_blocked_snapshots_are_safe():
    model = build_control_center()
    snapshots = (
        {"failure_state": "UNKNOWN"},
        {"failure_state": "STALE", "stale_domains": ["health"]},
        {"failure_state": "BLOCKED"},
    )

    for snapshot in snapshots:
        bound = model.bind_snapshot(snapshot)
        assert bound["snapshot"]["failure_state"] in {"UNKNOWN", "STALE", "BLOCKED"}
        assert bound["decision_allowed"] is False


def test_narrow_ui_simulation_never_starts_paper_or_live():
    model = build_control_center()
    bound = model.bind_snapshot({
        "paper": "OFF",
        "live": "OFF_LOCKED",
        "LIVE_TRADING": False,
        "live_order_sending_allowed": False,
        "paper_start_triggered": False,
        "live_order_sent": False,
        "execution_triggered": False,
    })

    assert bound["snapshot"]["paper"] == "OFF"
    assert bound["snapshot"]["live"] == "OFF_LOCKED"
    assert bound["snapshot"]["paper_start_triggered"] is False
    assert bound["snapshot"]["live_order_sent"] is False
    assert bound["snapshot"]["execution_triggered"] is False
