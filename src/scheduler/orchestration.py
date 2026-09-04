"""Scheduler/loop contracts; no UI, command handling, or live execution."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum


class LoopName(str, Enum):
    CLOSED_CANDLE_TRADE_LOOP = "CLOSED_CANDLE_TRADE_LOOP"
    UI_REFRESH_LOOP = "UI_REFRESH_LOOP"
    STOP_LOSS_MONITOR_LOOP = "STOP_LOSS_MONITOR_LOOP"
    OPTIMIZATION_LOOP_PLACEHOLDER = "OPTIMIZATION_LOOP_PLACEHOLDER"
    TELEGRAM_EVENT_LOOP_PLACEHOLDER = "TELEGRAM_EVENT_LOOP_PLACEHOLDER"
    RECOVERY_GATE_LOOP = "RECOVERY_GATE_LOOP"


@dataclass(frozen=True)
class SchedulerEvent:
    loop_name: LoopName
    scheduled_interval: timedelta
    last_run_utc: datetime | None
    last_run_tr: datetime | None
    next_run_utc: datetime | None
    next_run_tr: datetime | None
    run_status: str
    decision_allowed: bool
    blocked_reason: str | None
    live_trading_status: bool


@dataclass(frozen=True)
class SchedulerGate:
    recovery_valid: bool
    live_trading: bool = False

    def can_start(self) -> bool:
        return self.recovery_valid and not self.live_trading


def decision_allowed(loop: LoopName, *, candle_is_closed: bool, gate: SchedulerGate) -> tuple[bool, str | None]:
    if not gate.can_start():
        return False, "RECOVERY_OR_LIVE_GATE_BLOCKED"
    if loop == LoopName.CLOSED_CANDLE_TRADE_LOOP and not candle_is_closed:
        return False, "OPEN_CANDLE"
    if loop in (LoopName.UI_REFRESH_LOOP, LoopName.OPTIMIZATION_LOOP_PLACEHOLDER, LoopName.TELEGRAM_EVENT_LOOP_PLACEHOLDER):
        return False, "LOOP_DOES_NOT_PRODUCE_TRADE_DECISIONS"
    return True, None


def loop_intervals() -> dict[LoopName, timedelta]:
    return {
        LoopName.CLOSED_CANDLE_TRADE_LOOP: timedelta(hours=1),
        LoopName.UI_REFRESH_LOOP: timedelta(minutes=2),
        LoopName.STOP_LOSS_MONITOR_LOOP: timedelta(seconds=1),
        LoopName.OPTIMIZATION_LOOP_PLACEHOLDER: timedelta(minutes=2),
        LoopName.TELEGRAM_EVENT_LOOP_PLACEHOLDER: timedelta(seconds=1),
        LoopName.RECOVERY_GATE_LOOP: timedelta(seconds=1),
    }
