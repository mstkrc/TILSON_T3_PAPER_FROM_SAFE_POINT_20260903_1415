"""Position state representation only; no open/close execution."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PositionDirection(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


@dataclass(frozen=True)
class PositionState:
    symbol: str
    direction: PositionDirection
    quantity: float
    entry_price: float
    config_snapshot_id: str
    stop_loss_enabled: bool
    stop_loss_percent: float
    is_open: bool = True


def same_symbol_conflict(position: Optional[PositionState], symbol: str, direction: PositionDirection) -> Optional[str]:
    if position is None or not position.is_open or position.symbol != symbol:
        return None
    return "SAME_DIRECTION_POSITION_EXISTS" if position.direction == direction else "OPPOSITE_DIRECTION_POSITION_EXISTS"
