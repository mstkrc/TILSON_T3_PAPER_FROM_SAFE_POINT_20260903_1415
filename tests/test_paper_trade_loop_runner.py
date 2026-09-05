import json
from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_runner_is_paper_only_and_fail_closed():
    text = (ROOT / "tools/paper_trade_loop_runner.py").read_text(encoding="utf-8")
    assert "MODE_NOT_PAPER" in text
    assert "LIVE_OR_ORDER_RISK" in text
    assert "PAPER_LOOP_NO_DECISION_ENGINE_AVAILABLE" in text
    assert "private" not in text.lower()
    assert "real_order_allowed" in text


def test_loop_state_is_closed_candle_only_and_safe_after_cycle():
    state = json.loads((ROOT / "state/paper/trade_loop_state.json").read_text(encoding="utf-8"))
    assert state["paper_trade_loop_status"] in {"OFF", "SAFE_NOOP"}
    assert state["closed_candle_only"] is True
    assert state["public_market_data_only"] is True
    assert state["real_order_allowed"] is False
