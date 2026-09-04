"""Deterministic validation for the project's live lock."""
from dataclasses import dataclass
import json
from pathlib import Path

REQUIRED_FALSE = ("LIVE_TRADING", "live_order_sending_allowed", "ui_can_enable_live",
                  "telegram_can_enable_live", "codex_can_enable_live")

@dataclass(frozen=True)
class LiveLockViolation:
    violation_detected: bool
    violation_source: str
    severity: str
    safe_mode_active: bool
    stop_new_entries: bool
    stop_and_report: bool
    blocked_reason: str

def validate_live_lock(config):
    for key in REQUIRED_FALSE:
        if config.get(key) is not False:
            return LiveLockViolation(True, key, "CRITICAL", True, True, True, "LIVE_LOCK_VIOLATION")
    if config.get("requires_separate_live_gate") is not True:
        return LiveLockViolation(True, "requires_separate_live_gate", "CRITICAL", True, True, True, "SEPARATE_LIVE_GATE_REQUIRED")
    return None

def load_and_validate(path="config/live_lock_config.json"):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    return config, validate_live_lock(config)

def paper_execution_status():
    return {"paper_only": True, "live_order_sent": False}
