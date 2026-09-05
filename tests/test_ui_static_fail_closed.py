from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_disconnected_bridge_hides_static_demo_and_shows_server_url():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    assert "state-disconnected" in bridge
    assert "http://127.0.0.1:8765/" in bridge
    assert "STATE NOT CONNECTED" in bridge


def test_local_server_serves_workspace_ui_files_without_traversal():
    server = (ROOT / "tools/ui_paper_local_server.py").read_text(encoding="utf-8")
    assert "faz21_control_center.html" in server
    assert "candidate.is_file()" in server
    assert "ROOT in candidate.parents" in server
