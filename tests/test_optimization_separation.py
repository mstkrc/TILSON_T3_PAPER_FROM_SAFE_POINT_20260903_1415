import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from src.optimization.separation import (OptimizationScanInput, load_optimization_config,
    validate_scan, validate_backtest_config, separation_guard)

ROOT = Path(__file__).parents[1]

@dataclass
class Candle:
    is_closed: bool

def scan(closed=True):
    config = load_optimization_config(ROOT / "config" / "optimization_config.json")
    return OptimizationScanInput("BTCUSDT", Candle(closed), {}, config,
        datetime.now(timezone.utc), datetime.now(timezone.utc))

def test_optimization_config_separate_and_trade_unchanged():
    trade = json.loads((ROOT / "config/trade_config.json").read_text(encoding="utf-8"))
    before = dict(trade)
    config = load_optimization_config(ROOT / "config/optimization_config.json")
    assert config["separate_from_trade_config"] is True
    assert trade == before

def test_direct_apply_and_one_click_forbidden():
    assert load_optimization_config(ROOT / "config/optimization_config.json")["direct_apply_to_trade_config_allowed"] is False
    assert separation_guard()["direct_apply_allowed"] is False

def test_closed_candle_only_and_open_blocked():
    assert validate_scan(scan())[0] == "PASS"
    assert validate_scan(scan(False)) == ("BLOCKING_ERROR", "OPEN_CANDLE_FORBIDDEN")

def test_backtests_blocked():
    assert validate_backtest_config(load_optimization_config(ROOT / "config/optimization_config.json"))[0] == "PASS"
    assert validate_backtest_config({"historical_backtest_enabled": True})[0] == "BLOCKING_ERROR"

def test_optimization_does_not_trigger_execution_or_ledger():
    assert separation_guard() == {"execution_triggered": False, "ledger_trade_created": False,
        "trade_config_mutated": False, "direct_apply_allowed": False}

def test_live_lock():
    assert json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))["LIVE_TRADING"] is False
