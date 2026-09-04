"""Frozen paper-only start contract schema with no start authority."""

from dataclasses import dataclass

PAPER_ONLY_START_FIELDS = ("paper_start_request_id","requested_at","requested_by","source","requested_mode","effective_mode","paper_start_permission","paper_engine_target","live_lock_status","live_trading_flag","live_order_sending_allowed","ui_can_enable_live","telegram_can_enable_live","codex_can_enable_live","requires_separate_live_gate","real_order_capability","execution_network_status","order_endpoint_status","closed_candle_rule","required_timeframe","candle_wait_state","current_candle_state","scheduler_start_allowed","server_start_allowed","runtime_start_allowed","paper_start_allowed","live_start_allowed","order_send_allowed","config_write_allowed","ledger_write_allowed","position_mutation_allowed","diagnostic_status","risk_gate_status","ledger_consistency_status","position_consistency_status","pnl_consistency_status","error_repair_diagnostic_status","blocking_reason","carried_forward_gaps","audit_event_required","report_required","snapshot_required","rollback_reference_required","operator_message","next_allowed_action")

SAFE_PAPER_ONLY_START_FALLBACKS = {
    "paper_start_request_id": "UNKNOWN",
    "requested_at": "UNKNOWN",
    "requested_by": "UNKNOWN",
    "source": "UNKNOWN",
    "requested_mode": "PAPER",
    "effective_mode": "PAPER",
    "paper_start_permission": "NOT_GRANTED_YET",
    "paper_engine_target": "PAPER_ONLY_SIMULATION",
    "live_lock_status": "OFF_LOCKED",
    "live_trading_flag": False,
    "live_order_sending_allowed": False,
    "ui_can_enable_live": False,
    "telegram_can_enable_live": False,
    "codex_can_enable_live": False,
    "requires_separate_live_gate": True,
    "real_order_capability": "NONE",
    "execution_network_status": "NONE",
    "order_endpoint_status": "NONE",
    "closed_candle_rule": "REQUIRED",
    "required_timeframe": "1H_CLOSED_CANDLE",
    "candle_wait_state": "WAITING_FOR_CLOSED_CANDLE",
    "current_candle_state": "UNKNOWN",
    "scheduler_start_allowed": False,
    "server_start_allowed": False,
    "runtime_start_allowed": False,
    "paper_start_allowed": False,
    "live_start_allowed": False,
    "order_send_allowed": False,
    "config_write_allowed": False,
    "ledger_write_allowed": False,
    "position_mutation_allowed": False,
    "diagnostic_status": "UNKNOWN",
    "risk_gate_status": "UNKNOWN",
    "ledger_consistency_status": "UNKNOWN",
    "position_consistency_status": "UNKNOWN",
    "pnl_consistency_status": "UNKNOWN",
    "error_repair_diagnostic_status": "UNKNOWN",
    "blocking_reason": "PAPER_START_NOT_GRANTED_YET",
    "carried_forward_gaps": (),
    "audit_event_required": True,
    "report_required": True,
    "snapshot_required": True,
    "rollback_reference_required": True,
    "operator_message": "PAPER_ONLY_START_SCHEMA_READY_NO_START",
    "next_allowed_action": "IMPLEMENT_PAPER_ONLY_START_GATED_PATH",
}

@dataclass(frozen=True)
class PaperOnlyStartField:
    name: str
    required: bool
    fallback_value: object
    safety_rule: str

@dataclass(frozen=True)
class PaperOnlyStartSchema:
    fields: tuple[PaperOnlyStartField, ...]

def build_paper_only_start_schema() -> PaperOnlyStartSchema:
    return PaperOnlyStartSchema(tuple(PaperOnlyStartField(name, True, SAFE_PAPER_ONLY_START_FALLBACKS[name], "read-only contract; no start authority") for name in PAPER_ONLY_START_FIELDS))

def validate_paper_only_start_schema(schema: PaperOnlyStartSchema) -> bool:
    if len(schema.fields) != 45:
        raise ValueError("INVALID_PAPER_ONLY_START_FIELD_COUNT")
    names = tuple(field.name for field in schema.fields)
    if names != PAPER_ONLY_START_FIELDS or len(set(names)) != 45:
        raise ValueError("INVALID_PAPER_ONLY_START_FIELD_ORDER")
    if not all(field.required for field in schema.fields):
        raise ValueError("PAPER_ONLY_START_FIELD_NOT_REQUIRED")
    expected_false = ("live_trading_flag","live_order_sending_allowed","ui_can_enable_live","telegram_can_enable_live","codex_can_enable_live","scheduler_start_allowed","server_start_allowed","runtime_start_allowed","paper_start_allowed","live_start_allowed","order_send_allowed","config_write_allowed","ledger_write_allowed","position_mutation_allowed")
    if any(SAFE_PAPER_ONLY_START_FALLBACKS[name] is not False for name in expected_false):
        raise ValueError("UNSAFE_PAPER_ONLY_START_AUTHORITY")
    if SAFE_PAPER_ONLY_START_FALLBACKS["paper_start_permission"] != "NOT_GRANTED_YET" or SAFE_PAPER_ONLY_START_FALLBACKS["live_lock_status"] != "OFF_LOCKED":
        raise ValueError("UNSAFE_PAPER_ONLY_START_PERMISSION")
    if any("read-only" not in field.safety_rule for field in schema.fields):
        raise ValueError("UNSAFE_PAPER_ONLY_START_RULE")
    return True

def get_required_paper_only_start_fields() -> tuple[str, ...]:
    return PAPER_ONLY_START_FIELDS
