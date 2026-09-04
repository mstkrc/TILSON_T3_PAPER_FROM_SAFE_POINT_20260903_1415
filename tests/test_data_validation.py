"""Phase-3 validation checks only; no strategy, indicator, or execution tests."""

import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_config_json_files_are_valid():
    for path in (ROOT / "config").glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def test_live_trading_is_locked():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False


def test_no_forbidden_phase_files_exist():
    forbidden = ("strategy", "indicator", "execution", "ui", "telegram")
    names = [p.name.lower() for p in (ROOT / "src/data").glob("*")]
    assert not any(any(word in name for word in forbidden) for name in names)
