"""Phase-8 sizing validation only; no risk or execution behavior."""

from decimal import Decimal
import json
from pathlib import Path
import pytest

from src.paper.sizing import allocation, calculate_sizing

ROOT = Path(__file__).parents[1]


def sized(**overrides):
    args = dict(symbol="BTCUSDT", current_equity=Decimal("1000"), max_coin_count=10,
                leverage=1, entry_price=Decimal("123"), step_size=Decimal("0.1"),
                min_notional=Decimal("10"))
    args.update(overrides)
    return calculate_sizing(**args)


def test_wallet_allocation():
    assert allocation(Decimal("1000"), 10) == Decimal("100")
    assert allocation(Decimal("1500"), 10) == Decimal("150")


def test_leverage_and_raw_quantity():
    result = sized(leverage=3)
    assert result.allocation_usd == Decimal("100")
    assert result.nominal_position_usd == Decimal("300")
    assert result.raw_quantity == Decimal("300") / Decimal("123")


def test_step_size_downward_rounding_and_no_upward_rounding():
    result = sized(entry_price=Decimal("100"), step_size=Decimal("0.3"))
    assert result.normalized_quantity == Decimal("0.9")
    assert result.normalized_quantity <= result.raw_quantity


def test_min_notional_fail_and_allocation_not_exceeded():
    result = sized(entry_price=Decimal("100"), step_size=Decimal("1"), min_notional=Decimal("150"))
    assert result.sizing_status == "INVALID"
    assert result.blocked_reason == "MIN_NOTIONAL_NOT_MET"
    valid = sized(entry_price=Decimal("100"), step_size=Decimal("0.1"))
    assert valid.used_margin_usd <= valid.allocation_usd


def test_invalid_inputs_and_live_lock():
    with pytest.raises(ValueError):
        sized(leverage=6)
    with pytest.raises(ValueError):
        sized(entry_price=Decimal("0"))
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/paper").glob("*order*"))
