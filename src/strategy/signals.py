"""Long/short candidate evaluation from closed-candle indicator outputs."""

from dataclasses import dataclass
from enum import Enum

from src.indicators.models import IndicatorOutput


class SignalType(str, Enum):
    LONG_CANDIDATE = "LONG_CANDIDATE"
    SHORT_CANDIDATE = "SHORT_CANDIDATE"
    NO_SIGNAL = "NO_SIGNAL"


@dataclass(frozen=True)
class SignalResult:
    signal_type: SignalType
    blocked_reason: str | None
    candle_close_time_utc: object


def _result(kind: SignalType, reason: str | None, current: IndicatorOutput) -> SignalResult:
    return SignalResult(kind, reason, current.candle_close_time_utc)


def evaluate_direction(previous: IndicatorOutput, current: IndicatorOutput,
                       *, candle_is_closed: bool, adx_threshold: float = 30,
                       continuation_enabled: bool = False) -> SignalResult:
    """Return only a direction candidate, never an entry/exit or execution action."""
    if not candle_is_closed:
        return _result(SignalType.NO_SIGNAL, "OPEN_CANDLE", current)
    if current.plus_di == current.minus_di:
        return _result(SignalType.NO_SIGNAL, "DI_EQUALITY", current)
    if current.adx < adx_threshold:
        return _result(SignalType.NO_SIGNAL, "ADX_BELOW_THRESHOLD", current)
    if current.adx_slope_state == "FALLING":
        return _result(SignalType.NO_SIGNAL, "ADX_SLOPE_FALLING", current)

    long_change = previous.t3_color == "RED" and current.t3_color == "GREEN"
    short_change = previous.t3_color == "GREEN" and current.t3_color == "RED"
    long_cont = continuation_enabled and previous.t3_color == current.t3_color == "GREEN"
    short_cont = continuation_enabled and previous.t3_color == current.t3_color == "RED"
    if (long_change or long_cont) and current.plus_di > current.minus_di:
        return _result(SignalType.LONG_CANDIDATE, None, current)
    if (short_change or short_cont) and current.minus_di > current.plus_di:
        return _result(SignalType.SHORT_CANDIDATE, None, current)
    return _result(SignalType.NO_SIGNAL, "T3_DIRECTION_RULE_NOT_MET", current)
