"""Phase-5 indicator-only validation."""

import json
from datetime import datetime, timezone
from pathlib import Path

from src.data.candle_authority import CandleRecord, require_closed_candle
from src.indicators.dmi_adx import adx_slope_state, calculate_dmi_adx
from src.indicators.t3 import calculate_t3, t3_colors

ROOT = Path(__file__).parents[1]


def test_t3_formula_and_colors():
    values = calculate_t3([1, 2, 3, 4, 5], factor=0.7, period=4)
    assert len(values) == 5 and all(isinstance(value, float) for value in values)
    assert t3_colors(values)[0] == "RED"


def test_dmi_adx_formula_output():
    highs, lows, closes = [10, 11, 12, 13], [8, 9, 10, 11], [9, 10, 11, 12]
    plus, minus, adx = calculate_dmi_adx(highs, lows, closes, 24, 24)
    assert len(plus) == len(minus) == len(adx) == 4


def test_adx_slope_n():
    assert adx_slope_state([1, 1, 1, 2, 3], 2)[4] == "RISING"


def test_closed_candle_only():
    start = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
    candle = CandleRecord("BTCUSDT", start, datetime(2026, 1, 1, 11, tzinfo=timezone.utc), (1,))
    require_closed_candle(candle, datetime(2026, 1, 1, 11, tzinfo=timezone.utc))


def test_live_lock_and_no_signal_files():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/indicators").glob("*strategy*"))
