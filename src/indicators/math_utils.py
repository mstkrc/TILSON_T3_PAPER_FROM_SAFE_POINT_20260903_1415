"""Small deterministic EMA/RMA helpers."""


def ema(values: list[float], length: int) -> list[float]:
    if not values or length <= 0:
        return []
    alpha = 2 / (length + 1)
    out = [float(values[0])]
    for value in values[1:]:
        out.append(alpha * float(value) + (1 - alpha) * out[-1])
    return out


def rma(values: list[float], length: int) -> list[float]:
    if not values or length <= 0:
        return []
    out = [float(values[0])]
    alpha = 1 / length
    for value in values[1:]:
        out.append(alpha * float(value) + (1 - alpha) * out[-1])
    return out
