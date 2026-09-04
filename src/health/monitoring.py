from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from zoneinfo import ZoneInfo

TR = ZoneInfo("Europe/Istanbul")

class ErrorClass(str, Enum):
    COIN_LEVEL = "COIN_LEVEL"
    SYSTEM_WIDE = "SYSTEM_WIDE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    BLOCKING = "BLOCKING"

class RepairColor(str, Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

@dataclass(frozen=True)
class HealthStatus:
    binance_api_status: str
    market_data_status: str
    candle_cache_status: str
    indicator_status: str
    strategy_status: str
    risk_status: str
    paper_execution_status: str
    ledger_status: str
    scheduler_status: str
    telegram_security_status: str
    live_lock_status: str
    utf8_status: str
    recovery_status: str
    last_successful_closed_candle_scan_utc: datetime | None = None
    last_successful_closed_candle_scan_tr: datetime | None = None
    latest_error: str | None = None

@dataclass(frozen=True)
class SafeMode:
    safe_mode_active: bool
    stop_new_entries: bool
    reason: str
    triggered_at_utc: datetime
    triggered_at_tr: datetime

@dataclass(frozen=True)
class RepairMode:
    color: RepairColor
    repair_status: str
    affected_area: str
    affected_symbols: tuple[str, ...] = ()
    blocking_reason: str | None = None

@dataclass(frozen=True)
class StopAndReport:
    stop_required: bool
    stop_reason: str
    severity: str
    safe_mode_active: bool
    diagnostic_package_ready: bool
    next_required_action: str

def safe_mode(reason, now=None):
    now = now or datetime.now(timezone.utc)
    return SafeMode(True, True, reason, now, now.astimezone(TR))

def handle_error(error_class, reason, affected_symbols=()):
    coin_level = error_class == ErrorClass.COIN_LEVEL
    return {"scope": error_class.value, "stop_new_entries": not coin_level,
            "affected_symbols": tuple(affected_symbols), "reason": reason,
            "open_positions_tracking": True}

def stop_and_report(reason, severity="CRITICAL"):
    return StopAndReport(True, reason, severity, True, True, "STOP_AND_REPORT")

def mask_secrets(value):
    sensitive = ("api_key", "api_secret", "telegram_token", "auth_token", "private_key", "password", "token", "secret")
    if isinstance(value, dict):
        return {key: "***MASKED***" if any(part in key.lower() for part in sensitive) else mask_secrets(item) for key, item in value.items()}
    if isinstance(value, list): return [mask_secrets(item) for item in value]
    return value
