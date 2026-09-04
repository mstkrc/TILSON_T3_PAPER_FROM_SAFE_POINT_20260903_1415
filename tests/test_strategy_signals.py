"""Phase-6 signal-only validation; no order, position, or execution behavior."""

import json
from datetime import datetime, timezone
from pathlib import Path

from src.indicators.models import IndicatorOutput
from src.strategy.signals import SignalType, evaluate_direction

ROOT = Path(__file__).parents[1]
TIME = datetime(2026, 1, 1, 11, tzinfo=timezone.utc)


def out(color, plus, minus, adx=40, slope="RISING"):
    return IndicatorOutput(1.0, color, plus, minus, adx, slope, TIME)


def test_long_color_change_signal():
    assert evaluate_direction(out("RED", 10, 5), out("GREEN", 11, 5), candle_is_closed=True).signal_type == SignalType.LONG_CANDIDATE


def test_short_color_change_signal():
    assert evaluate_direction(out("GREEN", 5, 10), out("RED", 5, 11), candle_is_closed=True).signal_type == SignalType.SHORT_CANDIDATE


def test_continuation_modes():
    previous, current = out("GREEN", 10, 5), out("GREEN", 11, 5)
    assert evaluate_direction(previous, current, candle_is_closed=True).signal_type == SignalType.NO_SIGNAL
    assert evaluate_direction(previous, current, candle_is_closed=True, continuation_enabled=True).signal_type == SignalType.LONG_CANDIDATE
    previous, current = out("RED", 5, 10), out("RED", 5, 11)
    assert evaluate_direction(previous, current, candle_is_closed=True).signal_type == SignalType.NO_SIGNAL
    assert evaluate_direction(previous, current, candle_is_closed=True, continuation_enabled=True).signal_type == SignalType.SHORT_CANDIDATE


def test_di_equality_threshold_slope_and_open_candle():
    result = evaluate_direction(out("RED", 5, 5), out("GREEN", 5, 5), candle_is_closed=True)
    assert result.signal_type == SignalType.NO_SIGNAL and result.blocked_reason == "DI_EQUALITY"
    assert evaluate_direction(out("RED", 10, 5), out("GREEN", 11, 5, 29), candle_is_closed=True).blocked_reason == "ADX_BELOW_THRESHOLD"
    assert evaluate_direction(out("RED", 10, 5), out("GREEN", 11, 5, 40, "FALLING"), candle_is_closed=True).blocked_reason == "ADX_SLOPE_FALLING"
    assert evaluate_direction(out("RED", 10, 5), out("GREEN", 11, 5), candle_is_closed=False).blocked_reason == "OPEN_CANDLE"


def test_live_lock_and_signal_scope():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/strategy").glob("*execution*"))
