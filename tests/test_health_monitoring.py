from datetime import datetime, timezone
from src.health.monitoring import *

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)

def test_health_status_model():
    health = HealthStatus(*(["PASS"] * 13), NOW, NOW, None)
    assert health.live_lock_status == "PASS"

def test_coin_error_does_not_stop_system_and_tracks_positions():
    result = handle_error(ErrorClass.COIN_LEVEL, "BAD_DATA", ["BTCUSDT"])
    assert result["stop_new_entries"] is False and result["open_positions_tracking"] is True

def test_system_error_safe_mode_stop_report():
    assert safe_mode("BINANCE_API_WIDE").stop_new_entries is True
    assert stop_and_report("LEDGER_FAILURE").safe_mode_active is True

def test_repair_colors():
    assert [RepairColor.RED.value, RepairColor.YELLOW.value, RepairColor.GREEN.value] == ["RED", "YELLOW", "GREEN"]

def test_secret_masking():
    masked = mask_secrets({"api_key": "key", "nested": {"telegram_token": "tok"}, "safe": "ok"})
    assert masked["api_key"] == "***MASKED***" and masked["nested"]["telegram_token"] == "***MASKED***" and masked["safe"] == "ok"
