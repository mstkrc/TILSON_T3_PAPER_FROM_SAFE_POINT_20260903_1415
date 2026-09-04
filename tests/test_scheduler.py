"""Phase-12 orchestration validation; no service, UI, command, or order execution."""

import json
from datetime import timedelta
from pathlib import Path

from src.scheduler.orchestration import LoopName, SchedulerGate, decision_allowed, loop_intervals

ROOT = Path(__file__).parents[1]


def test_closed_candle_trade_loop_and_open_candle_block():
    gate = SchedulerGate(recovery_valid=True)
    assert decision_allowed(LoopName.CLOSED_CANDLE_TRADE_LOOP, candle_is_closed=True, gate=gate) == (True, None)
    assert decision_allowed(LoopName.CLOSED_CANDLE_TRADE_LOOP, candle_is_closed=False, gate=gate)[0] is False


def test_ui_refresh_is_two_minutes_and_no_decision():
    gate = SchedulerGate(recovery_valid=True)
    assert loop_intervals()[LoopName.UI_REFRESH_LOOP] == timedelta(minutes=2)
    assert decision_allowed(LoopName.UI_REFRESH_LOOP, candle_is_closed=True, gate=gate)[0] is False


def test_stop_loss_is_independent_of_one_hour_close():
    gate = SchedulerGate(recovery_valid=True)
    assert decision_allowed(LoopName.STOP_LOSS_MONITOR_LOOP, candle_is_closed=False, gate=gate)[0] is True


def test_placeholders_are_separate_and_do_not_decide():
    gate = SchedulerGate(recovery_valid=True)
    for loop in (LoopName.OPTIMIZATION_LOOP_PLACEHOLDER, LoopName.TELEGRAM_EVENT_LOOP_PLACEHOLDER):
        assert decision_allowed(loop, candle_is_closed=True, gate=gate)[0] is False


def test_recovery_gate_and_live_lock():
    assert not SchedulerGate(recovery_valid=False).can_start()
    assert not SchedulerGate(recovery_valid=True, live_trading=True).can_start()
    config = json.loads((ROOT / "config/live_lock_config.json").read_text(encoding="utf-8"))
    assert config["LIVE_TRADING"] is False


def test_no_external_order_or_ui_implementation():
    assert not list((ROOT / "src/scheduler").glob("*order*"))
    assert not list((ROOT / "src/scheduler").glob("*ui*"))
