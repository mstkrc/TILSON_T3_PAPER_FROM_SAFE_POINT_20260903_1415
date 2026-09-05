from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_server_exposes_paper_loop_routes_only():
    text = (ROOT / "tools/ui_paper_local_server.py").read_text(encoding="utf-8")
    for route in ("/api/paper/trade-loop/start", "/api/paper/trade-loop/stop", "/api/paper/trade-loop/status", "/api/paper/trade-loop/run-once"):
        assert route in text
    assert "PAPER_TRADE_LOOP_BACKGROUND_RUNNER_NOT_IMPLEMENTED" in text
