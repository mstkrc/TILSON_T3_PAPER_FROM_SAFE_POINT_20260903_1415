import json
from pathlib import Path

from tools.ui_paper_local_server import read_state, view_model

ROOT = Path(__file__).resolve().parents[1]

def test_default_state_is_safe_and_config_bound():
    config = json.loads((ROOT / "config/trade_config.json").read_text())
    runtime = read_state("runtime")
    wallet = read_state("wallet")
    assert runtime["paper_runtime"] == "OFF"
    assert runtime["paper_start_allowed"] is False
    assert runtime["live_trading"] is False
    assert wallet["initial_wallet_usd"] == config["initial_wallet_usd"] == 1000

def test_view_model_is_empty_local_paper_state():
    vm = view_model()
    assert vm["positions"]["positions"] == []
    assert vm["open_orders"]["open_orders"] == []
    assert vm["ledger"]["summary"] == {"fill_count": 0, "closed_trade_count": 0}
    assert vm["safety_flags"]["real_order_allowed"] is False

def test_start_policy_is_fail_closed_without_permission():
    runtime = read_state("runtime")
    assert runtime["paper_permission"] == "NOT_GRANTED_YET"
    assert runtime["paper_start_allowed"] is False

def test_stop_policy_cannot_enable_orders_or_live():
    runtime = read_state("runtime")
    live = json.loads((ROOT / "config/live_lock_config.json").read_text())
    assert runtime["real_order_allowed"] is False
    assert live["LIVE_TRADING"] is False
    assert live["live_order_sending_allowed"] is False

def test_html_contains_state_bridge_and_safe_actions():
    html = (ROOT / "outputs/faz21_control_center.html").read_text(encoding="utf-8")
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    assert "control_center_state_bridge.js" in html
    assert "api/paper" in bridge and "view-model" in bridge
    assert "START_BLOCKED_PERMISSION_REQUIRED" in (ROOT / "tools/ui_paper_local_server.py").read_text()
