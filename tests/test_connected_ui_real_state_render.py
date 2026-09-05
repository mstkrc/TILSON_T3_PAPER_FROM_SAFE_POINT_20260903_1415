from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_connected_render_is_authoritative_and_hides_static_demo():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    for token in ("tilson-authoritative-state", "POSITIONS:", "FILLS:", "MARKET DATA:"):
        assert token in bridge


def test_real_safety_remains_fail_closed():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    assert "LIVE: OFF_LOCKED" in bridge
    assert "REAL ORDER: false" in bridge
