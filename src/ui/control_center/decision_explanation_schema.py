"""Frozen, read-only decision explanation contract metadata."""

from dataclasses import dataclass
from typing import Iterable


DECISION_EXPLANATION_FIELDS = (
    "explanation_id", "generated_at", "symbol", "timeframe", "candle_closed",
    "system_mode", "scheduler_state", "candidate_state", "behavior_label",
    "direction_label", "active_mod", "rule_decision", "ai_decision",
    "compare_decision", "hybrid_decision", "final_decision", "confidence_score",
    "ranking_score", "risk_permission", "risk_block_reason", "no_trade_reason",
    "position_state", "ledger_consistency", "health_state", "live_lock_state",
    "paper_execution_readiness", "next_allowed_action", "blocked_by",
    "source_freshness", "display_only", "read_only", "can_execute",
    "can_start_paper", "can_start_live", "can_send_order",
)

SAFE_DECISION_FALLBACKS = frozenset({"UNKNOWN", "OFF", "STALE", "BLOCKED", "READY", "NO_DECISION", "NO_TRADE", "NOT_ALLOWED_YET", "PAPER", False, True})


@dataclass(frozen=True)
class DecisionExplanationField:
    name: str
    required: bool
    source: str
    allowed_values: str
    fallback_value: object
    blocking_if_missing: bool
    ui_display_rule: str
    safety_rule: str


@dataclass(frozen=True)
class DecisionExplanationSchema:
    fields: tuple[DecisionExplanationField, ...]


def build_decision_explanation_schema() -> DecisionExplanationSchema:
    fields = (
    DecisionExplanationField("explanation_id", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("generated_at", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("symbol", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("timeframe", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("candle_closed", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("system_mode", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("scheduler_state", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("candidate_state", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("behavior_label", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("direction_label", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("active_mod", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("rule_decision", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("ai_decision", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("compare_decision", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("hybrid_decision", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("final_decision", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("confidence_score", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("ranking_score", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("risk_permission", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("risk_block_reason", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("no_trade_reason", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("position_state", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("ledger_consistency", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("health_state", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("live_lock_state", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("paper_execution_readiness", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("next_allowed_action", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("blocked_by", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("source_freshness", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("display_only", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("read_only", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("can_execute", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("can_start_paper", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("can_start_live", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    DecisionExplanationField("can_send_order", True, "decision_explanation_source", "UNKNOWN", "UNKNOWN", True, "display value only", "read-only; no execution authority"),
    )
    fields = tuple(
        DecisionExplanationField(
            field.name,
            field.required,
            field.source,
            field.allowed_values,
            {"candle_closed": False, "system_mode": "PAPER", "final_decision": "BLOCKED", "live_lock_state": "OFF_LOCKED", "paper_execution_readiness": "NOT_ALLOWED_YET", "display_only": True, "read_only": True, "can_execute": False, "can_start_paper": False, "can_start_live": False, "can_send_order": False}.get(field.name, field.fallback_value),
            field.blocking_if_missing,
            field.ui_display_rule,
            field.safety_rule,
        ) for field in fields
    )
    return DecisionExplanationSchema(fields)


def validate_decision_explanation_schema(schema: DecisionExplanationSchema) -> bool:
    fields = schema.fields
    names = tuple(field.name for field in fields)
    if len(fields) != 35 or names != DECISION_EXPLANATION_FIELDS or len(set(names)) != 35:
        raise ValueError("INVALID_DECISION_EXPLANATION_FIELDS")
    for field in fields:
        if not field.required:
            raise ValueError("DECISION_EXPLANATION_FIELD_NOT_REQUIRED")
        if "read-only" not in field.safety_rule.lower() or "execution" not in field.safety_rule.lower():
            raise ValueError("UNSAFE_EXPLANATION_FIELD")
    expected = {"display_only": True, "read_only": True, "can_execute": False, "can_start_paper": False, "can_start_live": False, "can_send_order": False}
    for name, value in expected.items():
        field = next(item for item in fields if item.name == name)
        if field.fallback_value is not value:
            raise ValueError("UNSAFE_ACTION_FALLBACK")
    expected_values = {"candle_closed": False, "system_mode": "PAPER", "final_decision": "BLOCKED", "live_lock_state": "OFF_LOCKED", "paper_execution_readiness": "NOT_ALLOWED_YET"}
    for name, value in expected_values.items():
        if next(item for item in fields if item.name == name).fallback_value != value:
            raise ValueError("INVALID_REQUIRED_FALLBACK")
    return True


def get_required_decision_explanation_fields() -> tuple[str, ...]:
    return DECISION_EXPLANATION_FIELDS
