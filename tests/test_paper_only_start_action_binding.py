from src.ui.control_center.paper_only_start_action_binding import (
    bind_ui_paper_start_action_dry_run,
    validate_ui_paper_start_action_binding_result,
)


def test_default_action_binding_is_blocked_dry_run():
    result = bind_ui_paper_start_action_dry_run()
    assert result.status == "DRY_RUN_BLOCKED"
    assert result.blocking_reason == "PAPER_START_NOT_GRANTED_YET"
    assert result.operator_message == "UI_PAPER_START_ACTION_BINDING_DRY_RUN_READY_NO_START"
    assert result.next_allowed_action == "REVIEW_DRY_RUN_BEFORE_CONTROLLED_START"
    assert result.dry_run is True
    assert result.action_bound is True
    assert len(result.payload) == 45
    assert result.payload["requested_mode"] == "PAPER"
    assert result.payload["effective_mode"] == "PAPER"
    assert result.payload["closed_candle_rule"] == "REQUIRED"
    assert result.payload["required_timeframe"] == "1H_CLOSED_CANDLE"
    assert validate_ui_paper_start_action_binding_result(result) is True


def test_action_binding_never_triggers_start_or_execution():
    result = bind_ui_paper_start_action_dry_run()
    assert not result.paper_start_triggered
    assert not result.runtime_start_triggered
    assert not result.server_start_triggered
    assert not result.scheduler_loop_triggered
    assert not result.live_start_triggered
    assert result.execution_call == "NONE"
    assert result.network_order_endpoint == "NONE"
