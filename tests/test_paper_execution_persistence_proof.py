from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import json

from src.paper.execution import PaperExecutionInput, simulate_entry
from src.paper.state_store import persist_entry

from tests.helpers.test_state_sandbox import create_project_test_state_dir

def _run(direction: str):
    tmp_path = create_project_test_state_dir(direction.lower())
    for name, value in (("positions.json", {"positions": [], "source": "PAPER_LOCAL_STATE"}), ("ledger.json", {"fills": [], "closed_trades": [], "source": "PAPER_LOCAL_LEDGER"}), ("events.json", {"events": []})):
        (tmp_path / name).write_text(json.dumps(value), encoding="utf-8")
    now = datetime.now(timezone.utc)
    result = simulate_entry(PaperExecutionInput("TESTUSDT", direction, "ALLOW", SimpleNamespace(normalized_quantity=Decimal("0.001")), Decimal("100"), Decimal("100"), now, now, 1, "ISOLATED", {"mode": "PAPER"}))
    persist_entry(tmp_path, result)
    return tmp_path, result

def test_long_paper_execution_persists_position_ledger_event():
    tmp_path, result = _run("LONG")
    assert result.paper_only is True and result.live_order_sent is False
    assert json.loads((tmp_path / "positions.json").read_text())["positions"][0]["direction"] == "LONG"
    assert json.loads((tmp_path / "ledger.json").read_text())["fills"][0]["paper_only"] is True
    assert json.loads((tmp_path / "events.json").read_text())["events"][0]["type"] == "PAPER_ORDER_CREATED"

def test_short_paper_execution_persists_sell_fill():
    tmp_path, result = _run("SHORT")
    fill = json.loads((tmp_path / "ledger.json").read_text())["fills"][0]
    assert result.paper_only is True and result.live_order_sent is False
    assert fill["direction"] == "SHORT" and fill["side"] == "SELL"

def test_duplicate_execution_id_is_blocked():
    tmp_path, result = _run("LONG")
    import pytest
    with pytest.raises(ValueError, match="DUPLICATE_EXECUTION_ID"):
        persist_entry(tmp_path, result)
    assert len(json.loads((tmp_path / "ledger.json").read_text())["fills"]) == 1
