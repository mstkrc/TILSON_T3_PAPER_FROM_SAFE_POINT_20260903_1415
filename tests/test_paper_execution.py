"""Phase-10 paper fill validation; no real orders, ledger, UI, or Telegram."""

from datetime import datetime, timezone
from decimal import Decimal
import json
from pathlib import Path
from types import SimpleNamespace

from src.paper.execution import highest_priority, simulate_entry, simulate_exit, PaperExecutionInput

ROOT = Path(__file__).parents[1]
UTC = datetime(2026, 1, 1, 11, tzinfo=timezone.utc)


def request(permission="ALLOW"):
    return PaperExecutionInput("BTCUSDT", "LONG", permission, SimpleNamespace(normalized_quantity=Decimal("2")), Decimal("100"), Decimal("100"), UTC, UTC, 1, "ISOLATED", {"id": "snap"})


def test_allow_entry_market_taker_and_slippage():
    result = simulate_entry(request(), slippage_percent=Decimal("1"))
    assert result.execution_status == "FILLED" and result.fill_price == Decimal("101")
    assert result.paper_only and not result.live_order_sent


def test_block_permission_and_lock_no_fill():
    assert simulate_entry(request("BLOCKED")).fill_price is None
    assert simulate_entry(request(), lock_available=False).fill_price is None


def test_long_short_entry_slippage_and_exits():
    short = request(); short = PaperExecutionInput(short.symbol, "SHORT", short.permission_status, short.sizing_result, short.intended_entry_price, short.last_price, short.candle_timestamp_utc, short.candle_timestamp_tr, short.leverage, short.margin_mode, short.config_snapshot)
    assert simulate_entry(short, slippage_percent=Decimal("1")).fill_price == Decimal("99")
    assert simulate_exit(symbol="BTCUSDT", direction="LONG", requested_price=Decimal("100"), quantity=Decimal("2"), leverage=1, margin_mode="ISOLATED", reason="STOP_LOSS", config_snapshot={}, timestamp_tr=UTC, slippage_percent=Decimal("1")).execution_status == "FILLED"
    assert simulate_exit(symbol="BTCUSDT", direction="SHORT", requested_price=Decimal("100"), quantity=Decimal("2"), leverage=1, margin_mode="ISOLATED", reason="T3_EXIT", config_snapshot={}, timestamp_tr=UTC, slippage_percent=Decimal("1")).fill_price == Decimal("101")


def test_exit_reasons_and_priority():
    for reason in ("STOP_LOSS", "T3_EXIT", "MANUAL_CLOSE", "PANIC", "RISK_SYSTEM"):
        assert simulate_exit(symbol="X", direction="LONG", requested_price=Decimal("1"), quantity=Decimal("1"), leverage=1, margin_mode="ISOLATED", reason=reason, config_snapshot={}, timestamp_tr=UTC).exit_reason == reason
    assert highest_priority("T3_EXIT", "PANIC", "STOP_LOSS") == "PANIC"


def test_live_lock_and_no_external_authority():
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False
    assert not list((ROOT / "src/paper").glob("*order*"))
