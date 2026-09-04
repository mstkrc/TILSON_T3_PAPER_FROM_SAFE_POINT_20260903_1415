"""Phase-4 validation: closed candles, time standard, cache, and safety locks."""

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

import pytest

from src.data.candle_authority import CandleRecord, is_closed_candle, require_closed_candle
from src.data.candle_cache import ClosedCandleCache
from src.data.time_standard import to_turkey_time, to_utc

ROOT = Path(__file__).parents[1]


def candle(close_offset_minutes=0):
    start = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
    return CandleRecord("BTCUSDT", start, start + timedelta(hours=1), (1, 2, 3, 4, 5, 6))


def test_closed_candle_detection():
    c = candle()
    assert is_closed_candle(c, datetime(2026, 1, 1, 11, tzinfo=timezone.utc))


def test_open_candle_rejected():
    c = candle()
    with pytest.raises(ValueError):
        require_closed_candle(c, datetime(2026, 1, 1, 10, 59, tzinfo=timezone.utc))


def test_utc_turkey_conversion():
    value = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    assert to_utc(to_turkey_time(value)) == value


def test_cache_stores_only_closed_candles():
    cache = ClosedCandleCache()
    c = candle()
    now = datetime(2026, 1, 1, 11, tzinfo=timezone.utc)
    usage = cache.put(c, now)
    assert cache.get(c.symbol, c.open_time_utc) == c
    assert usage.candle_close_time_utc == c.close_time_utc


def test_live_trading_remains_locked():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False


def test_ui_refresh_is_not_a_decision_source():
    config = json.loads((ROOT / "config/trade_config.json").read_text(encoding="utf-8"))
    assert config["ui_refresh_minutes"] == 2
    assert "signal" not in config
