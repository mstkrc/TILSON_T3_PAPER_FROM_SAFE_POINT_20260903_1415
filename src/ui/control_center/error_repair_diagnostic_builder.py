"""Read-only construction of error, repair, and diagnostic payloads."""

from dataclasses import dataclass
from typing import Any, Mapping

from .error_repair_diagnostic_schema import ERROR_REPAIR_DIAGNOSTIC_FIELDS


@dataclass(frozen=True)
class ErrorRepairDiagnosticPayload:
    values: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)


def _reason(merged: Mapping[str, Any], providers_missing: bool) -> str:
    if merged.get("health_state") == "CRITICAL":
        return "CRITICAL_HEALTH"
    checks = (
        ("live_lock_violation_detected", "LIVE_LOCK_VIOLATION"),
        ("config_mismatch_detected", "CONFIG_MISMATCH"),
        ("runtime_exception_detected", "RUNTIME_EXCEPTION"),
    )
    for field, reason in checks:
        if merged.get(field) is True:
            return reason
    if providers_missing or merged.get("missing_provider_detected") is True or any(merged.get(name) == "PENDING" for name in ("diagnostic_provider_status", "repair_provider_status", "error_event_provider_status")):
        return "MISSING_PROVIDER"
    checks = (
        ("source_freshness", "STALE", "STALE_DATA"),
        ("ledger_mismatch_detected", True, "LEDGER_MISMATCH"),
        ("position_mismatch_detected", True, "POSITION_MISMATCH"),
        ("pnl_mismatch_detected", True, "PNL_MISMATCH"),
        ("scheduler_stopped_detected", True, "SCHEDULER_STOPPED"),
        ("paper_engine_stopped_detected", True, "PAPER_ENGINE_STOPPED"),
        ("ui_render_failure_detected", True, "UI_RENDER_FAILURE"),
    )
    for field, expected, reason in checks:
        if merged.get(field) == expected:
            return reason
    if merged.get("overall_diagnostic_status", "BLOCKED") in {"UNKNOWN", "BLOCKED"}:
        return "DIAGNOSTIC_NOT_PROVEN"
    return "NONE"


def build_safe_error_repair_diagnostic_payload(runtime_snapshot=None, diagnostic_snapshot=None, repair_snapshot=None, error_event_snapshot=None):
    snapshots = [dict(value or {}) for value in (runtime_snapshot, diagnostic_snapshot, repair_snapshot, error_event_snapshot)]
    merged: dict[str, Any] = {}
    for snapshot in snapshots:
        merged.update(snapshot)
    providers_missing = any(not snapshot for snapshot in snapshots)
    reason = _reason(merged, providers_missing)
    values = {name: "UNKNOWN" for name in ERROR_REPAIR_DIAGNOSTIC_FIELDS}
    values.update(merged)
    values.update({
        "system_mode": "PAPER",
        "diagnostic_provider_status": "PENDING" if not diagnostic_snapshot else merged.get("diagnostic_provider_status", "PENDING"),
        "repair_provider_status": "PENDING" if not repair_snapshot else merged.get("repair_provider_status", "PENDING"),
        "error_event_provider_status": "PENDING" if not error_event_snapshot else merged.get("error_event_provider_status", "PENDING"),
        "overall_diagnostic_status": merged.get("overall_diagnostic_status", "BLOCKED"),
        "fail_closed_reason": reason,
        "display_only": True,
        "read_only": True,
        "can_recommend_manual_repair": True,
        "manual_repair_allowed": True,
        "can_execute_repair": False,
        "can_auto_repair": False,
        "can_restore_recovery": False,
        "can_write_file": False,
        "can_execute": False,
        "can_start_paper": False,
        "can_start_live": False,
        "can_send_order": False,
        "auto_repair_allowed": False,
        "repair_execution_allowed": False,
        "recovery_restore_allowed": False,
        "next_allowed_action": "DISPLAY_ONLY_REVIEW",
        "blocked_by": [] if reason == "NONE" else [reason],
        "operator_message": "MANUAL_REVIEW_REQUIRED",
    })
    return ErrorRepairDiagnosticPayload({name: values[name] for name in ERROR_REPAIR_DIAGNOSTIC_FIELDS})


def validate_error_repair_diagnostic_payload(payload: ErrorRepairDiagnosticPayload) -> bool:
    values = payload.to_dict()
    if tuple(values) != ERROR_REPAIR_DIAGNOSTIC_FIELDS or len(values) != 50:
        raise ValueError("INVALID_ERROR_REPAIR_DIAGNOSTIC_PAYLOAD")
    if values["display_only"] is not True or values["read_only"] is not True:
        raise ValueError("PAYLOAD_NOT_READ_ONLY")
    for name in ("can_execute_repair", "can_auto_repair", "can_restore_recovery", "can_write_file", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "auto_repair_allowed", "repair_execution_allowed", "recovery_restore_allowed"):
        if values[name] is not False:
            raise ValueError("PAYLOAD_HAS_AUTHORITY")
    if values["next_allowed_action"] in {"EXECUTE_REPAIR", "AUTO_REPAIR", "RESTORE_RECOVERY", "WRITE_FILE", "START_PAPER", "START_LIVE", "SEND_ORDER"}:
        raise ValueError("UNSAFE_NEXT_ACTION")
    if values["overall_diagnostic_status"] != "PASS" and not values["blocked_by"]:
        raise ValueError("BLOCKED_WITHOUT_REASON")
    return True


def get_error_repair_fail_closed_reason(payload: ErrorRepairDiagnosticPayload) -> str:
    return str(payload.to_dict()["fail_closed_reason"])


def get_error_repair_blocked_by(payload: ErrorRepairDiagnosticPayload) -> list[str]:
    return list(payload.to_dict().get("blocked_by", []))
