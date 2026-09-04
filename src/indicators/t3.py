"""Tilson T3 calculation using the locked TradingView parameters."""

from .math_utils import ema


def calculate_t3(closes: list[float], factor: float = 0.7, period: int = 4) -> list[float]:
    if not closes:
        return []
    e1 = ema(closes, period)
    e2 = ema(e1, period)
    e3 = ema(e2, period)
    e4 = ema(e3, period)
    e5 = ema(e4, period)
    e6 = ema(e5, period)
    b = factor
    c1 = -b**3
    c2 = 3 * b**2 + 3 * b**3
    c3 = -6 * b**2 - 3 * b - 3 * b**3
    c4 = 1 + 3 * b + 3 * b**2 + b**3
    return [c1 * e6[i] + c2 * e5[i] + c3 * e4[i] + c4 * e3[i] for i in range(len(closes))]


def t3_colors(values: list[float]) -> list[str]:
    if not values:
        return []
    return ["RED"] + ["GREEN" if value > values[i - 1] else "RED" for i, value in enumerate(values[1:], 1)]
