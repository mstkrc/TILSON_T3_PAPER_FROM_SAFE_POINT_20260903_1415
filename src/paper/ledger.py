"""Paper ledger and accounting integrity; the single accounting source of truth."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional
from uuid import uuid4


class LedgerIntegrityStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    BLOCKING_ERROR = "BLOCKING_ERROR"


@dataclass(frozen=True)
class EntryLedgerRecord:
    ledger_id: str
    execution_id: str
    symbol: str
    direction: str
    action: str
    entry_price: Decimal
    quantity: Decimal
    leverage: int
    margin_mode: str
    used_margin_usd: Decimal
    nominal_position_usd: Decimal
    taker_fee: Decimal
    slippage_amount: Decimal
    funding_fee: Decimal
    gross_pnl: Decimal
    net_pnl: Decimal
    config_snapshot: dict
    decision_candle_utc: object
    decision_candle_tr: object
    timestamp_utc: object
    timestamp_tr: object


@dataclass(frozen=True)
class ExitLedgerRecord:
    ledger_id: str
    linked_entry_ledger_id: str
    execution_id: str
    symbol: str
    direction: str
    action: str
    exit_reason: str
    entry_price: Decimal
    exit_price: Decimal
    quantity: Decimal
    leverage: int
    gross_pnl: Decimal
    taker_fee: Decimal
    funding_fee: Decimal
    slippage_amount: Decimal
    net_pnl: Decimal
    config_snapshot: dict
    decision_candle_utc: object
    decision_candle_tr: object
    timestamp_utc: object
    timestamp_tr: object


def gross_pnl(direction: str, entry_price: Decimal, exit_price: Decimal, quantity: Decimal) -> Decimal:
    return ((exit_price - entry_price) if direction == "LONG" else (entry_price - exit_price)) * quantity


def net_pnl(gross: Decimal, commission: Decimal, funding_fee: Decimal, slippage_cost: Decimal) -> Decimal:
    return gross - commission - funding_fee - slippage_cost


class PaperLedger:
    def __init__(self):
        self._records: list[EntryLedgerRecord | ExitLedgerRecord] = []

    @property
    def records(self):
        return tuple(self._records)

    def append(self, record: EntryLedgerRecord | ExitLedgerRecord) -> LedgerIntegrityStatus:
        if any(item.execution_id == record.execution_id for item in self._records):
            raise ValueError("DUPLICATE_EXECUTION_ID")
        if record.action == "ENTRY":
            if record.quantity <= 0 or record.entry_price <= 0 or not record.config_snapshot:
                raise ValueError("INVALID_ENTRY_RECORD")
        elif record.action == "EXIT":
            if record.quantity <= 0 or record.exit_price <= 0 or not record.config_snapshot:
                raise ValueError("INVALID_EXIT_RECORD")
            if not any(item.ledger_id == record.linked_entry_ledger_id and item.action == "ENTRY" for item in self._records):
                raise ValueError("EXIT_WITHOUT_ENTRY")
        else:
            raise ValueError("INVALID_LEDGER_ACTION")
        self._records.append(record)
        return LedgerIntegrityStatus.PASS
