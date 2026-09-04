"""Pure, fail-closed UI paper-start action-binding dry run."""

from dataclasses import dataclass
from typing import Any

from .paper_only_start_request_adapter import (
    build_ui_paper_start_request_payload,
    get_ui_paper_start_blocking_reason,
    get_ui_paper_start_next_allowed_action,
    get_ui_paper_start_operator_message,
    validate_ui_paper_start_request_payload,
)


@dataclass(frozen=True)
class PaperStartActionBindingDryRunResult:
    status: str
    payload: dict[str, Any]
    blocking_reason: str
    operator_message: str
    next_allowed_action: str
    dry_run: bool = True
    action_bound: bool = True
    paper_start_triggered: bool = False
    runtime_start_triggered: bool = False
    server_start_triggered: bool = False
    scheduler_loop_triggered: bool = False
    live_start_triggered: bool = False
    execution_call: str = "NONE"
    network_order_endpoint: str = "NONE"


def bind_ui_paper_start_action_dry_run(ui_request=None, runtime_snapshot=None, gate_snapshot=None):
    """Bind the UI intent to the request adapter without exposing start authority."""
    adapted = build_ui_paper_start_request_payload(ui_request, runtime_snapshot, gate_snapshot)
    return PaperStartActionBindingDryRunResult(
        status="DRY_RUN_BLOCKED",
        payload=adapted.payload,
        blocking_reason=get_ui_paper_start_blocking_reason(adapted),
        operator_message="UI_PAPER_START_ACTION_BINDING_DRY_RUN_READY_NO_START",
        next_allowed_action="REVIEW_DRY_RUN_BEFORE_CONTROLLED_START",
    )


def validate_ui_paper_start_action_binding_result(result) -> bool:
    if not isinstance(result, PaperStartActionBindingDryRunResult):
        raise ValueError("INVALID_UI_PAPER_START_ACTION_BINDING_RESULT")
    if result.status != "DRY_RUN_BLOCKED" or not result.dry_run or not result.action_bound:
        raise ValueError("UNSAFE_UI_PAPER_START_ACTION_BINDING_RESULT")
    if any(getattr(result, name) for name in (
        "paper_start_triggered", "runtime_start_triggered", "server_start_triggered",
        "scheduler_loop_triggered", "live_start_triggered")):
        raise ValueError("UI_PAPER_START_ACTION_BINDING_TRIGGERED_START")
    if result.execution_call != "NONE" or result.network_order_endpoint != "NONE":
        raise ValueError("UI_PAPER_START_ACTION_BINDING_EXECUTION_EXPOSED")
    validate_ui_paper_start_request_payload(result.payload)
    return True


def get_ui_paper_start_action_binding_status(result):
    return result.status


def get_ui_paper_start_action_binding_blocking_reason(result):
    return result.blocking_reason


def get_ui_paper_start_action_binding_operator_message(result):
    return result.operator_message


def get_ui_paper_start_action_binding_next_allowed_action(result):
    return result.next_allowed_action
