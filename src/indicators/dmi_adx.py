"""TradingView-aligned DMI, ADX, and slope state calculation."""

from .math_utils import rma


def calculate_dmi_adx(highs: list[float], lows: list[float], closes: list[float], di_length: int = 24, adx_smoothing: int = 24):
    if not closes or not (len(highs) == len(lows) == len(closes)):
        raise ValueError("OHLC series must be non-empty and equal length")
    true_range = [highs[0] - lows[0]]
    plus_dm, minus_dm = [0.0], [0.0]
    for i in range(1, len(closes)):
        up, down = highs[i] - highs[i - 1], lows[i - 1] - lows[i]
        true_range.append(max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])))
        plus_dm.append(up if up > down and up > 0 else 0.0)
        minus_dm.append(down if down > up and down > 0 else 0.0)
    trur = rma(true_range, di_length)
    plus_di = [100 * rma(plus_dm, di_length)[i] / trur[i] if trur[i] else 0.0 for i in range(len(closes))]
    minus_di = [100 * rma(minus_dm, di_length)[i] / trur[i] if trur[i] else 0.0 for i in range(len(closes))]
    dx = [100 * abs(plus_di[i] - minus_di[i]) / (plus_di[i] + minus_di[i] if plus_di[i] + minus_di[i] else 1) for i in range(len(closes))]
    return plus_di, minus_di, rma(dx, adx_smoothing)


def adx_slope_state(adx: list[float], slope_n: int = 6, near_flat_tolerance: float = 1e-12) -> list[str]:
    if slope_n <= 0:
        raise ValueError("slope_n must be positive")
    states = ["NEAR_FLAT"] * len(adx)
    for i in range(slope_n, len(adx)):
        delta = adx[i] - adx[i - slope_n]
        states[i] = "RISING" if delta > near_flat_tolerance else "FALLING" if delta < -near_flat_tolerance else "NEAR_FLAT"
    return states
