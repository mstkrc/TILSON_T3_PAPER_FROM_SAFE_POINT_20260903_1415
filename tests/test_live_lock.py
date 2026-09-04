import json
from pathlib import Path
from src.health.live_lock import load_and_validate, paper_execution_status, validate_live_lock

ROOT = Path(__file__).parents[1]

def test_live_lock_config_is_closed():
    config, violation = load_and_validate(ROOT / "config/live_lock_config.json")
    assert violation is None
    assert config["LIVE_TRADING"] is False

def test_ui_telegram_codex_and_order_sending_cannot_enable_live():
    config, _ = load_and_validate(ROOT / "config/live_lock_config.json")
    assert all(config[key] is False for key in ("live_order_sending_allowed", "ui_can_enable_live", "telegram_can_enable_live", "codex_can_enable_live"))
    assert config["requires_separate_live_gate"] is True

def test_violation_is_blocking_safe_mode_and_stop_report():
    config, _ = load_and_validate(ROOT / "config/live_lock_config.json")
    violation = validate_live_lock({**config, "LIVE_TRADING": True})
    assert violation.severity == "CRITICAL"
    assert violation.safe_mode_active and violation.stop_new_entries and violation.stop_and_report

def test_paper_live_separation():
    assert paper_execution_status() == {"paper_only": True, "live_order_sent": False}
