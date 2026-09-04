"""Data-only models. They do not create signals, orders, or positions."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ExchangeSymbol:
    symbol: str
    status: str
    base_asset: str
    quote_asset: str
    contract_type: str
    margin_asset: str
    price_precision: int
    quantity_precision: int
    tick_size: Decimal
    step_size: Decimal
    min_qty: Decimal
    min_notional: Decimal

    def is_active_usdt_m(self) -> bool:
        return (self.status == "TRADING" and self.quote_asset == "USDT" and
                self.margin_asset == "USDT" and self.contract_type == "PERPETUAL")


@dataclass(frozen=True)
class MarketDataSnapshot:
    symbol: str
    ohlcv: tuple
    volume_24h: Decimal
    last_price: Decimal
    is_closed_candle: bool = False
