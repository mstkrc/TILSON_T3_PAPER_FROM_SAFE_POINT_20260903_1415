from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_connected_render_is_authoritative_and_hides_static_demo():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    for token in ("tilson-authoritative-state", "OPEN POSITIONS", "LEDGER FILLS", "CHART RENDERER NOT IMPLEMENTED"):
        assert token in bridge
    assert "app.style.visibility = \"hidden\"" in bridge


def test_real_safety_remains_fail_closed():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    assert "LIVE: <b>OFF_LOCKED</b>" in bridge
    assert "REAL ORDER: <b>false</b>" in bridge
