from pathlib import Path


ROOT = Path(__file__).parents[1]
BRIDGE = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
SERVER = (ROOT / "tools/ui_paper_local_server.py").read_text(encoding="utf-8")


def test_authoritative_action_map_and_server_routes_exist():
    for action in ("paper_start", "paper_stop", "refresh_view_model", "manual_close_position", "cancel_order", "panic_request", "panic_confirm", "strategy_config_change_request", "open_report", "export_report", "mark_notification_read", "select_chart_symbol", "select_row", "open_detail", "request_edit"):
        assert action in BRIDGE
    for route in ("/api/paper/panic-request", "/api/paper/panic-confirm", "/api/strategy/config-change-request", "/api/reports/open", "/api/reports/export", "/api/ui/selection", "/api/ui/detail", "/api/ui/change-request"):
        assert route in SERVER


def test_unknown_actions_fail_and_export_is_explicit():
    assert "UNKNOWN_UI_ACTION" in BRIDGE
    assert "EXPORT_NOT_IMPLEMENTED" in SERVER
    assert "UI_ACTION_REJECTED_UNKNOWN_CONTRACT_ACTION" in SERVER


def test_real_trading_paths_remain_absent_or_blocked():
    for text in (BRIDGE, SERVER):
        assert "live_start" not in text
        assert "send_real_order" not in text
        assert "real_order_allowed=true" not in text
