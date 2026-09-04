"""Read-only construction of decision explanation payloads."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .decision_explanation_schema import DECISION_EXPLANATION_FIELDS


@dataclass(frozen=True)
class DecisionExplanationPayload:
    values: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)


def _value(snapshot: Mapping[str, Any], name: str, fallback: Any = "UNKNOWN") -> Any:
    value = snapshot.get(name, fallback)
    return fallback if value is None else value


def _source_states(snapshot: Mapping[str, Any]) -> list[str]:
    states = []
    for value in snapshot.values():
        if isinstance(value, Mapping) and "state" in value:
            states.append(str(value["state"]))
    return states


def build_safe_decision_explanation_payload(
    runtime_snapshot: Mapping[str, Any] | None = None,
    bound_snapshot: Mapping[str, Any] | None = None,
    symbol: str = "UNKNOWN",
    timeframe: str = "UNKNOWN",
) -> DecisionExplanationPayload:
    """Build a passive explanation from supplied snapshots and safe fallbacks."""
    snapshot = dict(runtime_snapshot or {})
    bound = dict(bound_snapshot or {})
    states = _source_states(snapshot)
    failure_state = str(snapshot.get("failure_state", bound.get("failure_state", "UNKNOWN")))
    candle_closed = bool(snapshot.get("candle_closed", False))
    risk_permission = str(snapshot.get("risk_permission", "UNKNOWN"))
    stale = failure_state == "STALE" or "STALE" in states
    missing_provider = not runtime_snapshot or not states

    if missing_provider:
        no_trade_reason = "PENDING_PROVIDER"
    elif stale:
        no_trade_reason = "STALE_DATA"
    elif not candle_closed:
        no_trade_reason = "CLOSED_CANDLE_REQUIRED"
    elif risk_permission != "ALLOWED":
        no_trade_reason = "RISK_NOT_ALLOWED"
    else:
        no_trade_reason = _value(snapshot, "no_trade_reason", "NONE")

    blocked_by = [no_trade_reason] if no_trade_reason != "NONE" else []
    values: dict[str, Any] = {name: "UNKNOWN" for name in DECISION_EXPLANATION_FIELDS}
    values.update({
        "explanation_id": _value(snapshot, "explanation_id", "READ_ONLY_EXPLANATION"),
        "generated_at": _value(snapshot, "generated_at", datetime.now(timezone.utc).isoformat()),
        "symbol": symbol,
        "timeframe": timeframe,
        "candle_closed": candle_closed,
        "system_mode": _value(snapshot, "system_mode", "PAPER"),
        "scheduler_state": _value(snapshot, "scheduler_state"),
        "candidate_state": _value(snapshot, "candidate_state"),
        "behavior_label": _value(snapshot, "behavior_label"),
        "direction_label": _value(snapshot, "direction_label"),
        "active_mod": _value(snapshot, "active_mod"),
        "rule_decision": _value(snapshot, "rule_decision", "NO_DECISION"),
        "ai_decision": _value(snapshot, "ai_decision", "NO_DECISION"),
        "compare_decision": _value(snapshot, "compare_decision", "NO_DECISION"),
        "hybrid_decision": _value(snapshot, "hybrid_decision", "NO_DECISION"),
        "final_decision": _value(snapshot, "final_decision", "BLOCKED"),
        "confidence_score": _value(snapshot, "confidence_score"),
        "ranking_score": _value(snapshot, "ranking_score"),
        "risk_permission": risk_permission,
        "risk_block_reason": _value(snapshot, "risk_block_reason", no_trade_reason),
        "no_trade_reason": no_trade_reason,
        "position_state": _value(snapshot, "position_state"),
        "ledger_consistency": _value(snapshot, "ledger_consistency"),
        "health_state": _value(snapshot, "health_state"),
        "live_lock_state": _value(snapshot, "live_lock_state", "OFF_LOCKED"),
        "paper_execution_readiness": _value(snapshot, "paper_execution_readiness", "NOT_ALLOWED_YET"),
        "next_allowed_action": _value(snapshot, "next_allowed_action", "DISPLAY_ONLY_REVIEW"),
        "blocked_by": blocked_by,
        "source_freshness": "STALE" if stale else ("UNKNOWN" if missing_provider else "fresh"),
        "display_only": True,
        "read_only": True,
        "can_execute": False,
        "can_start_paper": False,
        "can_start_live": False,
        "can_send_order": False,
    })
    if values["live_lock_state"] == "OFF_LOCKED":
        values["next_allowed_action"] = "DISPLAY_ONLY_REVIEW"
    return DecisionExplanationPayload(values)


def validate_decision_explanation_payload(payload: DecisionExplanationPayload) -> bool:
    values = payload.to_dict()
    if tuple(values) != DECISION_EXPLANATION_FIELDS:
        raise ValueError("INVALID_PAYLOAD_FIELDS")
    if values["display_only"] is not True or values["read_only"] is not True:
        raise ValueError("PAYLOAD_NOT_READ_ONLY")
    for name in ("can_execute", "can_start_paper", "can_start_live", "can_send_order"):
        if values[name] is not False:
            raise ValueError("PAYLOAD_HAS_ACTION_AUTHORITY")
    if values["candle_closed"] is False and values["final_decision"] not in {"BLOCKED", "NO_DECISION"}:
        raise ValueError("OPEN_CANDLE_DECISION")
    if values["risk_permission"] != "ALLOWED" and values["final_decision"] == "READY":
        raise ValueError("RISK_NOT_ALLOWED_DECISION")
    return True


def get_no_trade_reason(payload: DecisionExplanationPayload) -> str:
    return str(payload.to_dict()["no_trade_reason"])


def get_blocked_by(payload: DecisionExplanationPayload) -> list[str]:
    blocked = payload.to_dict().get("blocked_by", [])
    return list(blocked) if blocked else ["READ_ONLY_OR_MISSING_PROVIDER"]
