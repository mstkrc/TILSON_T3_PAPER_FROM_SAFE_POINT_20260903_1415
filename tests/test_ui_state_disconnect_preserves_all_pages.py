from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIDGE = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
PAGES = [ROOT / "outputs/faz21_control_center.html"] + sorted((ROOT / "outputs/control_center").glob("*.html"))

def test_disconnect_is_non_destructive_banner_only():
    assert "showStateDisconnectedBanner" in BRIDGE
    assert "hideStateDisconnectedBanner" in BRIDGE
    assert "tilson-state-connection-banner" in BRIDGE
    assert "document.body.innerHTML" not in BRIDGE
    assert "document.documentElement.innerHTML" not in BRIDGE
    assert "replaceChildren" not in BRIDGE
    assert "function disconnected()" in BRIDGE
    assert "showStateDisconnectedBanner();" in BRIDGE

def test_all_control_center_page_shells_remain_present():
    assert len(PAGES) >= 17
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        assert "control_center_state_bridge.js" in text
        assert "data-screen=" in text
        assert "data-bind=" in text
        assert "data-action=" in text
        assert "<body" in text and "</html>" in text

def test_bridge_has_no_live_or_real_order_safety_bypass():
    for token in ("/api/live/start", "/api/order/send-real", "/api/binance/private", "API_KEY"):
        assert token not in BRIDGE
