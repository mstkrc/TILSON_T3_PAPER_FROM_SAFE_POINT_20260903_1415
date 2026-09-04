"""Read-only UI adapter for the frozen paper-only start request contract."""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .paper_only_start_builder import (PaperOnlyStartPayload,
    build_safe_paper_only_start_payload, get_paper_only_start_blocking_reason,
    validate_paper_only_start_payload)

@dataclass(frozen=True)
class PaperStartRequestAdapterResult:
    status: str
    payload: dict[str, Any]
    blocking_reason: str
    operator_message: str
    next_allowed_action: str

def normalize_ui_paper_start_request(ui_request=None) -> dict[str, Any]:
    return dict(ui_request) if isinstance(ui_request, Mapping) else {}

def build_ui_paper_start_request_payload(ui_request=None, runtime_snapshot=None, gate_snapshot=None):
    request = normalize_ui_paper_start_request(ui_request)
    runtime = dict(runtime_snapshot or {})
    gate = dict(gate_snapshot or {})
    built = build_safe_paper_only_start_payload(request, runtime, gate)
    reason = get_paper_only_start_blocking_reason(built)
    strong = {"LIVE_LOCK_VIOLATION", "REAL_ORDER_ENDPOINT_DETECTED", "NON_PAPER_MODE_REQUESTED"}
    if reason not in strong:
        reason = "PAPER_START_NOT_GRANTED_YET"
    payload = built.to_dict()
    payload["blocking_reason"] = reason
    return PaperStartRequestAdapterResult("BLOCKED", payload, reason,
        "UI_PAPER_START_REQUEST_ADAPTER_READY_NO_START", "REVIEW_ADAPTER_BEFORE_CONTROLLED_START")

def validate_ui_paper_start_request_payload(payload) -> bool:
    values = payload.payload if isinstance(payload, PaperStartRequestAdapterResult) else payload
    validate_paper_only_start_payload(PaperOnlyStartPayload(values))
    return True

def get_ui_paper_start_blocking_reason(payload) -> str:
    return payload.blocking_reason if isinstance(payload, PaperStartRequestAdapterResult) else payload["blocking_reason"]

def get_ui_paper_start_operator_message(payload) -> str:
    return payload.operator_message if isinstance(payload, PaperStartRequestAdapterResult) else payload["operator_message"]

def get_ui_paper_start_next_allowed_action(payload) -> str:
    return payload.next_allowed_action if isinstance(payload, PaperStartRequestAdapterResult) else payload["next_allowed_action"]
