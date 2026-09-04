"""Raw OHLCV, volume, and last-price data boundary; no trading behavior."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Mapping


@dataclass(frozen=True)
class RawMarketData:
    symbol: str
    ohlcv: tuple
    volume_24h: Decimal
    last_price: Decimal


def normalize_market_data(raw: Mapping) -> RawMarketData:
    return RawMarketData(raw["symbol"], tuple(raw.get("ohlcv", ())),
                         Decimal(str(raw["volume_24h"])), Decimal(str(raw["last_price"])))


def normalize_ohlcv(rows: Iterable[Mapping]) -> tuple[tuple, ...]:
    return tuple((r["open_time"], r["open"], r["high"], r["low"], r["close"],
                  r["volume"], r["close_time"]) for r in rows)
