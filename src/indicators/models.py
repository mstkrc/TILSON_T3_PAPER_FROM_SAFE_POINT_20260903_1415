"""Indicator output model; it carries no signal or execution decision."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class IndicatorOutput:
    t3_value: float
    t3_color: str
    plus_di: float
    minus_di: float
    adx: float
    adx_slope_state: str
    candle_close_time_utc: datetime
