from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_bridge_skips_shell_containers_and_uses_leaf_targets():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    assert "function isShellContainer" in bridge
    assert "data-bind-status" in bridge
    assert "isSafeTextBindingTarget" in bridge
    assert "x.textContent =" in bridge


def test_pages_keep_shell_and_bridge_contract():
    pages = [ROOT / "outputs/faz21_control_center.html", *sorted((ROOT / "outputs/control_center").glob("*.html"))]
    assert len(pages) >= 17
    for page in pages:
        text = page.read_text(encoding="utf-8")
        assert "data-screen=" in text
        assert "data-action=" in text
        assert "control_center_state_bridge.js" in text


def test_safety_literals_remain_blocked():
    source = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "outputs").rglob("*.html"))
    assert "LIVE_TRADING=true" not in source
    assert "real_order_allowed=true" not in source
    assert "live_order_sending_allowed=true" not in source
