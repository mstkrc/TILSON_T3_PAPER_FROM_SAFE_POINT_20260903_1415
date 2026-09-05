from pathlib import Path
from uuid import uuid4
import json

ROOT = Path(__file__).resolve().parents[2]

def create_project_test_state_dir(test_name: str) -> Path:
    path = ROOT / ".tmp_test_state" / "paper_persistence" / f"{test_name}_{uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    for name, value in (("wallet.json", {"cash_usd": 1000, "available_usd": 1000}), ("positions.json", {"positions": []}), ("ledger.json", {"fills": [], "closed_trades": []}), ("events.json", {"events": []}), ("scan_results.json", {}), ("open_orders.json", {"open_orders": []})):
        (path / name).write_text(json.dumps(value), encoding="utf-8")
    return path
