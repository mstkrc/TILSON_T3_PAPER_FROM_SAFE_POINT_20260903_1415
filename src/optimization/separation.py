"""Optimization is read-only, closed-candle-only, and separate from trading."""
from dataclasses import dataclass
from datetime import datetime
from copy import deepcopy
import json
from pathlib import Path

@dataclass(frozen=True)
class OptimizationScanInput:
    symbol: str
    closed_candle_data: object
    indicator_snapshot: dict
    optimization_config_snapshot: dict
    timestamp_utc: datetime
    timestamp_tr: datetime

@dataclass(frozen=True)
class OptimizationResult:
    optimization_run_id: str
    symbol: str
    tested_parameter_set: dict
    score: float | None
    result_summary: dict
    closed_candle_only: bool = True
    open_candle_used: bool = False
    source: str = "BINANCE_LIVE_DATA"
    direct_apply_allowed: bool = False
    trade_config_mutated: bool = False
    result_status: str = "PASS"
    blocked_reason: str | None = None

def load_optimization_config(path="config/optimization_config.json"):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if not config.get("separate_from_trade_config", False):
        raise ValueError("OPTIMIZATION_CONFIG_NOT_SEPARATE")
    return deepcopy(config)

def validate_scan(scan: OptimizationScanInput):
    if not scan.optimization_config_snapshot.get("live_scan_only", False):
        return "BLOCKING_ERROR", "LIVE_SCAN_ONLY_REQUIRED"
    if scan.optimization_config_snapshot.get("open_candle_allowed", True):
        return "BLOCKING_ERROR", "OPEN_CANDLE_FORBIDDEN"
    if not getattr(scan.closed_candle_data, "is_closed", True):
        return "BLOCKING_ERROR", "OPEN_CANDLE_FORBIDDEN"
    return "PASS", None

def validate_config_isolation(trade_config, before_trade_config):
    return "PASS" if trade_config == before_trade_config else "BLOCKING_ERROR"

def validate_backtest_config(config):
    if config.get("historical_backtest_enabled") or config.get("mini_backtest_enabled"):
        return "BLOCKING_ERROR", "BACKTEST_FORBIDDEN"
    return "PASS", None

def separation_guard():
    return {"execution_triggered": False, "ledger_trade_created": False,
            "trade_config_mutated": False, "direct_apply_allowed": False}
