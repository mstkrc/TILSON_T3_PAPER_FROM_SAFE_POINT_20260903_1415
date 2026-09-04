"""Frozen read-only Ledger/PnL/Position consistency schema."""

from dataclasses import dataclass


LEDGER_PNL_POSITION_FIELDS = (
    "consistency_snapshot_id",
    "generated_at",
    "system_mode",
    "source_freshness",
    "ledger_source_status",
    "pnl_source_status",
    "position_source_status",
    "ledger_provider_status",
    "pnl_provider_status",
    "position_provider_status",
    "paper_ledger_write_allowed",
    "live_ledger_write_allowed",
    "open_position_count",
    "closed_trade_count",
    "ledger_trade_count",
    "duplicate_trade_ids_detected",
    "missing_trade_ids_detected",
    "orphan_fills_detected",
    "orphan_positions_detected",
    "position_ledger_mismatch_detected",
    "pnl_ledger_mismatch_detected",
    "realized_pnl_total",
    "unrealized_pnl_total",
    "fees_total",
    "slippage_total",
    "cash_balance",
    "equity",
    "exposure_total",
    "risk_reserved_amount",
    "ledger_consistency",
    "pnl_consistency",
    "position_consistency",
    "overall_consistency",
    "fail_closed_reason",
    "display_only",
    "read_only",
    "can_write_ledger",
    "can_mutate_position",
    "can_recalculate_authoritatively",
    "can_execute",
    "can_start_paper",
    "can_start_live",
    "can_send_order",
    "next_allowed_action",
    "blocked_by",
)

SAFE_LEDGER_PNL_POSITION_FALLBACKS = frozenset({
    "UNKNOWN", "PENDING", "BLOCKED", "CONSISTENCY_NOT_PROVEN",
    "DISPLAY_ONLY_REVIEW", "PAPER", False, True,
})


@dataclass(frozen=True)
class LedgerPnlPositionField:
    name: str
    required: bool
    source: str
    allowed_values: str
    fallback_value: object
    blocking_if_missing: bool
    ui_display_rule: str
    safety_rule: str


@dataclass(frozen=True)
class LedgerPnlPositionSchema:
    fields: tuple[LedgerPnlPositionField, ...]


def build_ledger_pnl_position_schema() -> LedgerPnlPositionSchema:
    fallbacks = {
        "system_mode": "PAPER",
        "ledger_provider_status": "PENDING",
        "pnl_provider_status": "PENDING",
        "position_provider_status": "PENDING",
        "ledger_consistency": "UNKNOWN",
        "pnl_consistency": "UNKNOWN",
        "position_consistency": "UNKNOWN",
        "overall_consistency": "BLOCKED",
        "fail_closed_reason": "CONSISTENCY_NOT_PROVEN",
        "display_only": True,
        "read_only": True,
        "can_write_ledger": False,
        "can_mutate_position": False,
        "can_recalculate_authoritatively": False,
        "can_execute": False,
        "can_start_paper": False,
        "can_start_live": False,
        "can_send_order": False,
        "paper_ledger_write_allowed": False,
        "live_ledger_write_allowed": False,
        "next_allowed_action": "DISPLAY_ONLY_REVIEW",
        "blocked_by": "CONSISTENCY_NOT_PROVEN",
    }
    fields = tuple(
        LedgerPnlPositionField(
            name, True, "consistency/runtime source", "safe contract value",
            fallbacks.get(name, "UNKNOWN"), True, "display only",
            "read-only; no execution; no ledger write",
        )
        for name in LEDGER_PNL_POSITION_FIELDS
    )
    return LedgerPnlPositionSchema(fields)


def validate_ledger_pnl_position_schema(schema: LedgerPnlPositionSchema) -> bool:
    fields = schema.fields
    names = tuple(field.name for field in fields)
    if len(fields) != 45 or names != LEDGER_PNL_POSITION_FIELDS or len(set(names)) != 45:
        raise ValueError("INVALID_LEDGER_PNL_POSITION_FIELDS")
    for field in fields:
        if not field.required:
            raise ValueError("LEDGER_PNL_POSITION_FIELD_NOT_REQUIRED")
        rule = field.safety_rule.lower()
        if "read-only" not in rule or "no execution" not in rule or "no ledger write" not in rule:
            raise ValueError("UNSAFE_LEDGER_PNL_POSITION_FIELD")
    expected = {
        "display_only": True, "read_only": True, "can_write_ledger": False,
        "can_mutate_position": False, "can_recalculate_authoritatively": False,
        "can_execute": False, "can_start_paper": False, "can_start_live": False,
        "can_send_order": False, "paper_ledger_write_allowed": False,
        "live_ledger_write_allowed": False, "system_mode": "PAPER",
        "ledger_provider_status": "PENDING", "pnl_provider_status": "PENDING",
        "position_provider_status": "PENDING", "ledger_consistency": "UNKNOWN",
        "pnl_consistency": "UNKNOWN", "position_consistency": "UNKNOWN",
        "overall_consistency": "BLOCKED", "fail_closed_reason": "CONSISTENCY_NOT_PROVEN",
        "next_allowed_action": "DISPLAY_ONLY_REVIEW", "blocked_by": "CONSISTENCY_NOT_PROVEN",
    }
    values = {field.name: field.fallback_value for field in fields}
    if any(values[name] != value for name, value in expected.items()):
        raise ValueError("UNSAFE_LEDGER_PNL_POSITION_FALLBACK")
    return True


def get_required_ledger_pnl_position_fields() -> tuple[str, ...]:
    return LEDGER_PNL_POSITION_FIELDS
