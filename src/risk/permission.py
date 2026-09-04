"""Risk permission decision model; it does not place or manage trades."""

from dataclasses import dataclass
from typing import Optional

from src.paper.position import PositionDirection, PositionState, same_symbol_conflict


@dataclass(frozen=True)
class PermissionResult:
    symbol: str
    direction: str
    candidate_status: str
    sizing_status: str
    current_open_positions_count: int
    max_coin_count: int
    free_balance_usd: float
    required_margin_usd: float
    same_symbol_position_exists: bool
    opposite_direction_position_exists: bool
    concurrency_lock_status: str
    stop_loss_enabled: bool
    stop_loss_percent: float
    config_snapshot_id: str
    permission_status: str
    blocked_reason: Optional[str]


def evaluate_permission(*, symbol: str, direction: PositionDirection, candidate_status: str,
                        sizing_status: str, open_positions: list[PositionState], max_coin_count: int,
                        free_balance_usd: float, required_margin_usd: float, lock_available: bool,
                        stop_loss_enabled: bool, stop_loss_percent: float,
                        config_snapshot_id: str) -> PermissionResult:
    position = next((p for p in open_positions if p.symbol == symbol and p.is_open), None)
    conflict = same_symbol_conflict(position, symbol, direction)
    same = conflict == "SAME_DIRECTION_POSITION_EXISTS"
    opposite = conflict == "OPPOSITE_DIRECTION_POSITION_EXISTS"
    reason = None
    if candidate_status != "VALID": reason = "INVALID_CANDIDATE"
    elif sizing_status != "VALID": reason = "INVALID_SIZING"
    elif len(open_positions) >= max_coin_count: reason = "MAX_COIN_SLOT_FULL"
    elif required_margin_usd > free_balance_usd: reason = "INSUFFICIENT_FREE_BALANCE"
    elif conflict: reason = conflict
    elif not lock_available: reason = "CONCURRENCY_LOCK_ACTIVE"
    return PermissionResult(symbol, direction.value, candidate_status, sizing_status, len(open_positions),
        max_coin_count, free_balance_usd, required_margin_usd, same, opposite,
        "FREE" if lock_available else "LOCKED", stop_loss_enabled, stop_loss_percent,
        config_snapshot_id, "ALLOW" if reason is None else "BLOCK", reason)
