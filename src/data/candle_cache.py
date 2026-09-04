"""In-memory cache that accepts closed candles only and records candle authority."""

from dataclasses import dataclass
from datetime import datetime

from .candle_authority import CandleRecord, require_closed_candle


@dataclass(frozen=True)
class CandleUsage:
    symbol: str
    candle_open_time_utc: datetime
    candle_close_time_utc: datetime
    source: str = "closed_candle_cache"


class ClosedCandleCache:
    def __init__(self):
        self._items: dict[tuple[str, datetime], CandleRecord] = {}

    def put(self, candle: CandleRecord, now_utc: datetime) -> CandleUsage:
        require_closed_candle(candle, now_utc)
        self._items[(candle.symbol, candle.open_time_utc)] = candle
        return CandleUsage(candle.symbol, candle.open_time_utc, candle.close_time_utc)

    def get(self, symbol: str, open_time_utc: datetime) -> CandleRecord | None:
        return self._items.get((symbol, open_time_utc))

