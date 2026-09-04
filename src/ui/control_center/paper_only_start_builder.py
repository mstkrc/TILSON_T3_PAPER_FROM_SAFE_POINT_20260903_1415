"""Frozen, fail-closed builder for a paper-only start request payload."""

from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any

from .paper_only_start_schema import PAPER_ONLY_START_FIELDS, SAFE_PAPER_ONLY_START_FALLBACKS

PAPER_ONLY_START_FORCED_FALSE_FIELDS = (
    "live_trading_flag", "live_order_sending_allowed", "ui_can_enable_live",
    "telegram_can_enable_live", "codex_can_enable_live", "scheduler_start_allowed",
    "server_start_allowed", "runtime_start_allowed", "paper_start_allowed",
    "live_start_allowed", "order_send_allowed", "config_write_allowed",
    "ledger_write_allowed", "position_mutation_allowed",
)
PAPER_ONLY_START_REQUIRED_TRUE_FIELDS = (
    "requires_separate_live_gate", "audit_event_required", "report_required",
    "snapshot_required", "rollback_reference_required",
)

_PRIORITY = (
    ("live_lock_violation", "LIVE_LOCK_VIOLATION"),
    ("real_endpoint", "REAL_ORDER_ENDPOINT_DETECTED"),
    ("non_paper", "NON_PAPER_MODE_REQUESTED"),
    ("permission", "PAPER_START_NOT_GRANTED_YET"),
    ("candle", "OPEN_CANDLE_OR_UNKNOWN_CANDLE"),
    ("risk", "RISK_GATE_NOT_PASS"),
    ("diagnostic", "DIAGNOSTIC_NOT_PASS"),
    ("ledger", "LEDGER_NOT_CONSISTENT"),
    ("position", "POSITION_NOT_CONSISTENT"),
    ("pnl", "PNL_NOT_CONSISTENT"),
    ("runtime", "RUNTIME_PROVIDER_PENDING"),
    ("paper", "PAPER_ORCHESTRATION_PENDING"),
)

@dataclass(frozen=True)
class PaperOnlyStartPayload:
    values: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)

    def __getitem__(self, name: str) -> Any:
        return self.values[name]


def _truthy(value: Any) -> bool:
    return value is True


def _blocking_reason(values: Mapping[str, Any], request: Mapping[str, Any], runtime: Mapping[str, Any], gate: Mapping[str, Any]) -> str:
    if any(_truthy(request.get(name)) or _truthy(runtime.get(name)) or _truthy(gate.get(name)) for name in PAPER_ONLY_START_FORCED_FALSE_FIELDS[:5]):
        return "LIVE_LOCK_VIOLATION"
    if any(request.get(name) not in (None, "NONE") or runtime.get(name) not in (None, "NONE") or gate.get(name) not in (None, "NONE") for name in ("real_order_capability", "order_endpoint_status")):
        return "REAL_ORDER_ENDPOINT_DETECTED"
    if request.get("requested_mode", "PAPER") != "PAPER":
        return "NON_PAPER_MODE_REQUESTED"
    if values["paper_start_permission"] != "NOT_GRANTED_YET":
        return "PAPER_START_NOT_GRANTED_YET"
    if values["current_candle_state"] in ("OPEN", "UNKNOWN") or values["candle_wait_state"] != "CLOSED_CANDLE_READY":
        return "OPEN_CANDLE_OR_UNKNOWN_CANDLE"
    checks = (("risk_gate_status", "RISK_GATE_NOT_PASS"), ("diagnostic_status", "DIAGNOSTIC_NOT_PASS"), ("ledger_consistency_status", "LEDGER_NOT_CONSISTENT"), ("position_consistency_status", "POSITION_NOT_CONSISTENT"), ("pnl_consistency_status", "PNL_NOT_CONSISTENT"))
    for name, reason in checks:
        if values[name] != "PASS":
            return reason
    if any(values[name] == "PENDING" for name in ("diagnostic_status", "risk_gate_status")) or runtime.get("runtime_provider_status") == "PENDING":
        return "RUNTIME_PROVIDER_PENDING"
    if runtime.get("paper_orchestration_status") == "PENDING":
        return "PAPER_ORCHESTRATION_PENDING"
    return "PAPER_START_NOT_GRANTED_YET"


def build_safe_paper_only_start_payload(request=None, runtime_snapshot=None, gate_snapshot=None) -> PaperOnlyStartPayload:
    req = dict(request or {})
    runtime = dict(runtime_snapshot or {})
    gate = dict(gate_snapshot or {})
    merged = {}
    merged.update(runtime)
    merged.update(gate)
    merged.update(req)
    values = {name: merged.get(name, SAFE_PAPER_ONLY_START_FALLBACKS[name]) for name in PAPER_ONLY_START_FIELDS}
    values.update({"requested_mode": "PAPER", "effective_mode": "PAPER", "paper_start_permission": "NOT_GRANTED_YET", "paper_engine_target": "PAPER_ONLY_SIMULATION", "live_lock_status": "OFF_LOCKED", "real_order_capability": "NONE", "execution_network_status": "NONE", "order_endpoint_status": "NONE", "closed_candle_rule": "REQUIRED", "required_timeframe": "1H_CLOSED_CANDLE", "candle_wait_state": "CLOSED_CANDLE_READY" if merged.get("candle_wait_state") == "CLOSED_CANDLE_READY" else "WAITING_FOR_CLOSED_CANDLE", "paper_start_allowed": False, "operator_message": "GATED_BUILDER_READY_NO_START", "next_allowed_action": "REVIEW_GATED_BUILDER_BEFORE_CONTROLLED_START"})
    for name in PAPER_ONLY_START_FORCED_FALSE_FIELDS:
        values[name] = False
    for name in PAPER_ONLY_START_REQUIRED_TRUE_FIELDS:
        values[name] = True
    values["blocking_reason"] = _blocking_reason(values, req, runtime, gate)
    values["carried_forward_gaps"] = list(values.get("carried_forward_gaps") or [])
    return PaperOnlyStartPayload(values)


def validate_paper_only_start_payload(payload: PaperOnlyStartPayload) -> bool:
    values = payload.to_dict()
    if tuple(values) != PAPER_ONLY_START_FIELDS or len(values) != 45:
        raise ValueError("INVALID_PAPER_ONLY_START_PAYLOAD_FIELDS")
    if any(values[name] is not False for name in PAPER_ONLY_START_FORCED_FALSE_FIELDS):
        raise ValueError("UNSAFE_PAPER_ONLY_START_PAYLOAD")
    if any(values[name] is not True for name in PAPER_ONLY_START_REQUIRED_TRUE_FIELDS):
        raise ValueError("REQUIRED_PAPER_ONLY_START_GATE_MISSING")
    if values["paper_start_permission"] != "NOT_GRANTED_YET" or values["paper_start_allowed"] is not False:
        raise ValueError("PAPER_START_PERMISSION_NOT_FAIL_CLOSED")
    if values["effective_mode"] != "PAPER" or values["live_lock_status"] != "OFF_LOCKED":
        raise ValueError("UNSAFE_PAPER_ONLY_START_MODE")
    if values["operator_message"] != "GATED_BUILDER_READY_NO_START":
        raise ValueError("UNSAFE_PAPER_ONLY_START_MESSAGE")
    return True


def get_paper_only_start_blocking_reason(payload: PaperOnlyStartPayload) -> str:
    return payload["blocking_reason"]


def get_paper_only_start_next_allowed_action(payload: PaperOnlyStartPayload) -> str:
    return payload["next_allowed_action"]

