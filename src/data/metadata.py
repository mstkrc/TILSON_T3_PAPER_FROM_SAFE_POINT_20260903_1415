"""Exchange metadata normalization and symbol-universe selection."""

from typing import Iterable, Mapping
from .models import ExchangeSymbol


def normalize_symbol(raw: Mapping) -> ExchangeSymbol:
    filters = {item["filterType"]: item for item in raw.get("filters", [])}
    price, lot = filters.get("PRICE_FILTER", {}), filters.get("LOT_SIZE", {})
    notional = filters.get("MIN_NOTIONAL", filters.get("NOTIONAL", {}))
    return ExchangeSymbol(raw["symbol"], raw["status"], raw["baseAsset"], raw["quoteAsset"],
        raw["contractType"], raw["marginAsset"], int(raw["pricePrecision"]),
        int(raw["quantityPrecision"]), price.get("tickSize", "0"), lot.get("stepSize", "0"),
        lot.get("minQty", "0"), notional.get("notional", notional.get("minNotional", "0")))


def select_usdt_m_symbols(symbols: Iterable[ExchangeSymbol]) -> list[ExchangeSymbol]:
    return [symbol for symbol in symbols if symbol.is_active_usdt_m()]
