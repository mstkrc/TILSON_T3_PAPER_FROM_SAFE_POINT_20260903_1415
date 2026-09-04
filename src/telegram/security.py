"""Whitelist authorization and safe Telegram command guards."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

TR = ZoneInfo("Europe/Istanbul")
READ_ONLY_COMMANDS = {"/status", "/pnl", "/positions", "/health"}

@dataclass(frozen=True)
class AuthorizationEvent:
    user_id: int
    is_authorized: bool
    rejection_reason: str | None
    timestamp_utc: datetime
    timestamp_tr: datetime

@dataclass(frozen=True)
class TelegramOutput:
    command: str
    user_id: int
    authorization_status: str
    command_status: str
    response_type: str
    panic_confirmation_required: bool
    live_action_allowed: bool
    blocked_reason: str | None
    timestamp_utc: datetime
    timestamp_tr: datetime

class TelegramSecurity:
    def __init__(self, authorized_user_ids, confirmation_timeout_seconds=60):
        self._authorized = frozenset(authorized_user_ids)
        self._timeout = timedelta(seconds=confirmation_timeout_seconds)
        self._pending_panic = {}

    def authorize(self, user_id, now=None):
        now = now or datetime.now(timezone.utc)
        allowed = user_id in self._authorized
        return AuthorizationEvent(user_id, allowed, None if allowed else "UNAUTHORIZED_USER", now, now.astimezone(TR))

    def handle(self, command, user_id, now=None):
        now = now or datetime.now(timezone.utc)
        auth = self.authorize(user_id, now)
        if not auth.is_authorized:
            return TelegramOutput(command, user_id, "REJECTED", "BLOCKED", "AUDIT", False, False, auth.rejection_reason, now, now.astimezone(TR))
        if command in READ_ONLY_COMMANDS:
            return TelegramOutput(command, user_id, "AUTHORIZED", "ALLOWED", "READ_ONLY", False, False, None, now, now.astimezone(TR))
        if command == "/panic":
            pending = self._pending_panic.get(user_id)
            if pending and now - pending <= self._timeout:
                del self._pending_panic[user_id]
                return TelegramOutput(command, user_id, "AUTHORIZED", "ACCEPTED", "PANIC_CONFIRMATION", False, False, "NO_EXECUTION_IN_PHASE_16", now, now.astimezone(TR))
            self._pending_panic[user_id] = now
            return TelegramOutput(command, user_id, "AUTHORIZED", "PENDING_CONFIRMATION", "PANIC_CONFIRMATION", True, False, "DOUBLE_CONFIRMATION_REQUIRED", now, now.astimezone(TR))
        reason = {"manual_close": "MANUAL_CLOSE_DISABLED", "/manual_close": "MANUAL_CLOSE_DISABLED",
                  "settings_change": "SETTINGS_CHANGE_DISABLED", "/settings_change": "SETTINGS_CHANGE_DISABLED",
                  "live_enable": "LIVE_ENABLE_DISABLED", "/live_enable": "LIVE_ENABLE_DISABLED"}.get(command, "COMMAND_NOT_ALLOWED")
        return TelegramOutput(command, user_id, "AUTHORIZED", "BLOCKED", "SECURITY", False, False, reason, now, now.astimezone(TR))
