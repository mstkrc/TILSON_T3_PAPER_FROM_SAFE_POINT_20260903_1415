"""Wallet, allocation, leverage, and quantity normalization calculations."""

from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN


@dataclass(frozen=True)
class SizingResult:
    symbol: str
    allocation_usd: Decimal
    leverage: int
    nominal_position_usd: Decimal
    entry_price: Decimal
    raw_quantity: Decimal
    normalized_quantity: Decimal
    used_margin_usd: Decimal
    rounding_difference_usd: Decimal
    min_notional_pass: bool
    sizing_status: str
    blocked_reason: str | None


def allocation(current_equity: Decimal, max_coin_count: int) -> Decimal:
    if current_equity <= 0 or max_coin_count <= 0:
        raise ValueError("equity and max_coin_count must be positive")
    return current_equity / Decimal(max_coin_count)


def calculate_sizing(*, symbol: str, current_equity: Decimal, max_coin_count: int,
                     leverage: int, entry_price: Decimal, step_size: Decimal,
                     min_notional: Decimal) -> SizingResult:
    if leverage not in (1, 2, 3, 4, 5):
        raise ValueError("leverage must be one of 1, 2, 3, 4, 5")
    if entry_price <= 0 or step_size <= 0 or min_notional < 0:
        raise ValueError("price, step_size must be positive and min_notional non-negative")
    alloc = allocation(current_equity, max_coin_count)
    nominal = alloc * Decimal(leverage)
    raw = nominal / entry_price
    units = (raw / step_size).to_integral_value(rounding=ROUND_DOWN)
    normalized = units * step_size
    used_margin = normalized * entry_price / Decimal(leverage)
    rounding_difference = (raw - normalized) * entry_price
    notional_pass = normalized * entry_price >= min_notional
    status = "VALID" if normalized > 0 and notional_pass and used_margin <= alloc else "INVALID"
    reason = None if status == "VALID" else ("MIN_NOTIONAL_NOT_MET" if not notional_pass else "ALLOCATION_EXCEEDED_OR_ZERO_QUANTITY")
    return SizingResult(symbol, alloc, leverage, nominal, entry_price, raw, normalized,
                        used_margin, rounding_difference, notional_pass, status, reason)
