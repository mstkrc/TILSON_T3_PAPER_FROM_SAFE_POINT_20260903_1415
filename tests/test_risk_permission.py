"""Phase-9 risk/position/lock validation; no execution or ledger behavior."""

import json
from pathlib import Path

from src.paper.position import PositionDirection, PositionState
from src.risk.concurrency import SymbolLockRegistry
from src.risk.permission import evaluate_permission

ROOT = Path(__file__).parents[1]


def position(symbol="BTCUSDT", direction=PositionDirection.LONG):
    return PositionState(symbol, direction, 1, 100, "snap-old", True, 2)


def allowed(**kwargs):
    base = dict(symbol="ETHUSDT", direction=PositionDirection.LONG, candidate_status="VALID", sizing_status="VALID", open_positions=[], max_coin_count=10, free_balance_usd=500, required_margin_usd=100, lock_available=True, stop_loss_enabled=True, stop_loss_percent=2, config_snapshot_id="snap-new")
    base.update(kwargs)
    return evaluate_permission(**base)


def test_slot_and_balance_blocks():
    assert allowed(open_positions=[position(str(i)) for i in range(10)]).blocked_reason == "MAX_COIN_SLOT_FULL"
    assert allowed(free_balance_usd=50).blocked_reason == "INSUFFICIENT_FREE_BALANCE"


def test_same_and_opposite_direction_and_auto_reversal():
    assert allowed(open_positions=[position("ETHUSDT")]).blocked_reason == "SAME_DIRECTION_POSITION_EXISTS"
    assert allowed(open_positions=[position("ETHUSDT", PositionDirection.SHORT)]).blocked_reason == "OPPOSITE_DIRECTION_POSITION_EXISTS"


def test_valid_allow_and_stop_snapshot():
    result = allowed()
    assert result.permission_status == "ALLOW"
    assert result.stop_loss_enabled and result.stop_loss_percent == 2
    assert result.config_snapshot_id == "snap-new"


def test_lock_active_blocks_and_free_allows():
    registry = SymbolLockRegistry()
    assert registry.acquire("BTCUSDT")
    assert allowed(symbol="BTCUSDT", lock_available=False).blocked_reason == "CONCURRENCY_LOCK_ACTIVE"
    registry.release("BTCUSDT")
    assert allowed(symbol="BTCUSDT", lock_available=True).permission_status == "ALLOW"


def test_live_lock_and_no_execution_files():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/risk").glob("*execution*"))
    assert not list((ROOT / "src/risk").glob("*ledger*"))
