"""Frozen read-only error, repair, and diagnostic contract schema."""

from dataclasses import dataclass


ERROR_REPAIR_DIAGNOSTIC_FIELDS = (
    "diagnostic_snapshot_id",
    "generated_at",
    "system_mode",
    "source_freshness",
    "health_state",
    "error_state",
    "diagnostic_provider_status",
    "repair_provider_status",
    "error_event_provider_status",
    "active_error_count",
    "critical_error_count",
    "warning_count",
    "stale_data_detected",
    "missing_provider_detected",
    "config_mismatch_detected",
    "ledger_mismatch_detected",
    "position_mismatch_detected",
    "pnl_mismatch_detected",
    "live_lock_violation_detected",
    "runtime_exception_detected",
    "scheduler_stopped_detected",
    "paper_engine_stopped_detected",
    "ui_render_failure_detected",
    "recovery_snapshot_available",
    "recovery_restore_required",
    "repair_recommendation",
    "repair_action_required",
    "auto_repair_allowed",
    "manual_repair_allowed",
    "repair_execution_allowed",
    "recovery_restore_allowed",
    "diagnostic_consistency",
    "repair_consistency",
    "overall_diagnostic_status",
    "fail_closed_reason",
    "severity",
    "display_only",
    "read_only",
    "can_recommend_manual_repair",
    "can_execute_repair",
    "can_auto_repair",
    "can_restore_recovery",
    "can_write_file",
    "can_execute",
    "can_start_paper",
    "can_start_live",
    "can_send_order",
    "next_allowed_action",
    "blocked_by",
    "operator_message",
)

SAFE_ERROR_REPAIR_DIAGNOSTIC_FALLBACKS = frozenset({
    "UNKNOWN", "PENDING", "BLOCKED", "DIAGNOSTIC_NOT_PROVEN",
    "DISPLAY_ONLY_REVIEW", "MANUAL_REVIEW_REQUIRED", "PAPER", False, True,
})


@dataclass(frozen=True)
class ErrorRepairDiagnosticField:
    name: str
    required: bool
    source: str
    allowed_values: str
    fallback_value: object
    blocking_if_missing: bool
    ui_display_rule: str
    safety_rule: str


@dataclass(frozen=True)
class ErrorRepairDiagnosticSchema:
    fields: tuple[ErrorRepairDiagnosticField, ...]


def build_error_repair_diagnostic_schema() -> ErrorRepairDiagnosticSchema:
    fallbacks = {
        "system_mode": "PAPER",
        "diagnostic_provider_status": "PENDING",
        "repair_provider_status": "PENDING",
        "error_event_provider_status": "PENDING",
        "health_state": "UNKNOWN",
        "error_state": "UNKNOWN",
        "overall_diagnostic_status": "BLOCKED",
        "severity": "UNKNOWN",
        "fail_closed_reason": "DIAGNOSTIC_NOT_PROVEN",
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
        "blocked_by": "DIAGNOSTIC_NOT_PROVEN",
        "operator_message": "MANUAL_REVIEW_REQUIRED",
    }
    fields = tuple(
        ErrorRepairDiagnosticField(
            name, True, "diagnostic/error/repair source", "safe contract value",
            fallbacks.get(name, "UNKNOWN"), True, "display only",
            "read-only; no execution; no repair; no file write",
        )
        for name in ERROR_REPAIR_DIAGNOSTIC_FIELDS
    )
    return ErrorRepairDiagnosticSchema(fields)


def validate_error_repair_diagnostic_schema(schema: ErrorRepairDiagnosticSchema) -> bool:
    fields = schema.fields
    names = tuple(field.name for field in fields)
    if len(fields) != 50 or names != ERROR_REPAIR_DIAGNOSTIC_FIELDS or len(set(names)) != 50:
        raise ValueError("INVALID_ERROR_REPAIR_DIAGNOSTIC_FIELDS")
    for field in fields:
        if not field.required:
            raise ValueError("ERROR_REPAIR_DIAGNOSTIC_FIELD_NOT_REQUIRED")
        rule = field.safety_rule.lower()
        if any(token not in rule for token in ("read-only", "no execution", "no repair", "no file write")):
            raise ValueError("UNSAFE_ERROR_REPAIR_DIAGNOSTIC_FIELD")
    expected = {
        "display_only": True, "read_only": True, "can_recommend_manual_repair": True,
        "manual_repair_allowed": True, "can_execute_repair": False,
        "can_auto_repair": False, "can_restore_recovery": False, "can_write_file": False,
        "can_execute": False, "can_start_paper": False, "can_start_live": False,
        "can_send_order": False, "auto_repair_allowed": False,
        "repair_execution_allowed": False, "recovery_restore_allowed": False,
        "system_mode": "PAPER", "diagnostic_provider_status": "PENDING",
        "repair_provider_status": "PENDING", "error_event_provider_status": "PENDING",
        "health_state": "UNKNOWN", "error_state": "UNKNOWN",
        "overall_diagnostic_status": "BLOCKED", "severity": "UNKNOWN",
        "fail_closed_reason": "DIAGNOSTIC_NOT_PROVEN",
        "next_allowed_action": "DISPLAY_ONLY_REVIEW",
        "blocked_by": "DIAGNOSTIC_NOT_PROVEN", "operator_message": "MANUAL_REVIEW_REQUIRED",
    }
    values = {field.name: field.fallback_value for field in fields}
    if any(values[name] != value for name, value in expected.items()):
        raise ValueError("UNSAFE_ERROR_REPAIR_DIAGNOSTIC_FALLBACK")
    return True


def get_required_error_repair_diagnostic_fields() -> tuple[str, ...]:
    return ERROR_REPAIR_DIAGNOSTIC_FIELDS
