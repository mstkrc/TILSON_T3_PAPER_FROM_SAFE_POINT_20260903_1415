"""Paper-only fill simulation; no exchange or order endpoint integration."""

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import IntEnum
from uuid import uuid4


class ExitPriority(IntEnum):
    NORMAL = 1
    T3_EXIT = 2
    STOP_LOSS = 3
    MANUAL_CLOSE = 4
    PANIC = 5


@dataclass(frozen=True)
class PaperExecutionInput:
    symbol: str
    direction: str
    permission_status: str
    sizing_result: object
    intended_entry_price: Decimal
    last_price: Decimal
    candle_timestamp_utc: datetime
    candle_timestamp_tr: datetime
    leverage: int
    margin_mode: str
    config_snapshot: dict


@dataclass(frozen=True)
class PaperExecutionOutput:
    execution_id: str
    symbol: str
    direction: str
    action: str
    exit_reason: str | None
    requested_price: Decimal
    fill_price: Decimal | None
    quantity: Decimal
    leverage: int
    margin_mode: str
    slippage_amount: Decimal
    taker_fee_estimate: Decimal
    paper_only: bool
    live_order_sent: bool
    timestamp_utc: datetime
    timestamp_tr: datetime
    config_snapshot: dict
    execution_status: str
    blocked_reason: str | None


def _price(direction: str, requested: Decimal, slippage: Decimal, action: str) -> Decimal:
    adverse = (direction == "LONG" and action == "ENTRY") or (direction == "SHORT" and action == "EXIT")
    return requested * (Decimal(1) + slippage if adverse else Decimal(1) - slippage)


def simulate_entry(request: PaperExecutionInput, *, slippage_percent: Decimal = Decimal("0"), lock_available: bool = True) -> PaperExecutionOutput:
    quantity = Decimal(str(getattr(request.sizing_result, "normalized_quantity", 0)))
    now = datetime.now(timezone.utc)
    blocked = None if request.permission_status == "ALLOW" and lock_available else ("CONCURRENCY_LOCK_ACTIVE" if not lock_available else "PERMISSION_BLOCKED")
    fill = None if blocked else _price(request.direction, request.intended_entry_price, slippage_percent / 100, "ENTRY")
    slip_amount = Decimal(0) if fill is None else abs(fill - request.intended_entry_price)
    fee = Decimal(0) if fill is None else fill * quantity * Decimal("0.0004")
    return PaperExecutionOutput(str(uuid4()), request.symbol, request.direction, "ENTRY", None, request.intended_entry_price, fill, quantity, request.leverage, request.margin_mode, slip_amount, fee, True, False, now, request.candle_timestamp_tr, request.config_snapshot, "FILLED" if fill is not None else "BLOCKED", blocked)


def simulate_exit(*, symbol: str, direction: str, requested_price: Decimal, quantity: Decimal, leverage: int, margin_mode: str, reason: str, config_snapshot: dict, timestamp_tr: datetime, slippage_percent: Decimal = Decimal("0"), lock_available: bool = True) -> PaperExecutionOutput:
    now = datetime.now(timezone.utc)
    blocked = None if lock_available else "CONCURRENCY_LOCK_ACTIVE"
    fill = None if blocked else _price(direction, requested_price, slippage_percent / 100, "EXIT")
    slip_amount = Decimal(0) if fill is None else abs(fill - requested_price)
    fee = Decimal(0) if fill is None else fill * quantity * Decimal("0.0004")
    return PaperExecutionOutput(str(uuid4()), symbol, direction, "EXIT", reason, requested_price, fill, quantity, leverage, margin_mode, slip_amount, fee, True, False, now, timestamp_tr, config_snapshot, "FILLED" if fill is not None else "BLOCKED", blocked)


def highest_priority(*reasons: str) -> str:
    return max(reasons, key=lambda value: ExitPriority[value]).upper()
