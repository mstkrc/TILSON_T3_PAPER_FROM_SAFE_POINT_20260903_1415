"""Closed-candle authority for raw 1H market data only."""

from dataclasses import dataclass
from datetime import datetime, timezone


TIMEFRAME_HOURS = 1


@dataclass(frozen=True)
class CandleRecord:
    symbol: str
    open_time_utc: datetime
    close_time_utc: datetime
    ohlcv: tuple

    def __post_init__(self):
        if self.open_time_utc.tzinfo is None or self.close_time_utc.tzinfo is None:
            raise ValueError("Candle times must be timezone-aware")


def is_closed_candle(candle: CandleRecord, now_utc: datetime) -> bool:
    if now_utc.tzinfo is None:
        raise ValueError("now_utc must be timezone-aware")
    return candle.close_time_utc <= now_utc.astimezone(timezone.utc)


def require_closed_candle(candle: CandleRecord, now_utc: datetime) -> CandleRecord:
    if not is_closed_candle(candle, now_utc):
        raise ValueError("Open candle rejected by Candle Authority")
    return candle

