from datetime import datetime, timezone, timedelta
from src.telegram.security import TelegramSecurity

NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)

def test_authorized_read_only_commands():
    security = TelegramSecurity([42])
    for command in ("/status", "/pnl", "/positions", "/health"):
        result = security.handle(command, 42, NOW)
        assert result.command_status == "ALLOWED"
        assert result.live_action_allowed is False

def test_unauthorized_rejected_and_logged_format():
    result = TelegramSecurity([42]).handle("/status", 99, NOW)
    assert result.command_status == "BLOCKED"
    assert result.authorization_status == "REJECTED"
    assert result.blocked_reason == "UNAUTHORIZED_USER"

def test_panic_requires_two_confirmations():
    security = TelegramSecurity([42])
    assert security.handle("/panic", 42, NOW).command_status == "PENDING_CONFIRMATION"
    assert security.handle("/panic", 42, NOW + timedelta(seconds=1)).command_status == "ACCEPTED"
    assert security.handle("/panic", 42, NOW + timedelta(seconds=2)).command_status == "PENDING_CONFIRMATION"

def test_disabled_commands_and_live_lock():
    security = TelegramSecurity([42])
    for command in ("/manual_close", "/settings_change", "/live_enable"):
        result = security.handle(command, 42, NOW)
        assert result.command_status == "BLOCKED"
        assert result.live_action_allowed is False
