"""Read-only construction of Ledger/PnL/Position consistency payloads."""

from dataclasses import dataclass
from typing import Any, Mapping

from .ledger_pnl_position_schema import LEDGER_PNL_POSITION_FIELDS


@dataclass(frozen=True)
class LedgerPnlPositionPayload:
    values: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.values)


def _first(source: Mapping[str, Any], name: str, fallback: Any = "UNKNOWN") -> Any:
    value = source.get(name, fallback)
    return fallback if value is None else value


def _reason(snapshot: Mapping[str, Any], ledger: Mapping[str, Any], pnl: Mapping[str, Any], position: Mapping[str, Any]) -> str:
    merged = {**snapshot, **ledger, **pnl, **position}
    providers_missing = not ledger or not pnl or not position
    if providers_missing:
        return "PROVIDER_PENDING"
    if merged.get("source_freshness") == "STALE":
        return "STALE_DATA"
    checks = (
        ("duplicate_trade_ids_detected", True, "DUPLICATE_LEDGER_ID"),
        ("missing_trade_ids_detected", True, "MISSING_LEDGER_ID"),
        ("orphan_fills_detected", True, "ORPHAN_FILL"),
        ("orphan_positions_detected", True, "ORPHAN_POSITION"),
        ("position_ledger_mismatch_detected", True, "POSITION_LEDGER_MISMATCH"),
        ("pnl_ledger_mismatch_detected", True, "PNL_LEDGER_MISMATCH"),
    )
    for name, expected, reason in checks:
        if merged.get(name) is expected:
            return reason
    consistency_names = ("ledger_consistency", "pnl_consistency", "position_consistency", "overall_consistency")
    if any(merged.get(name, "UNKNOWN") in {"UNKNOWN", "BLOCKED"} for name in consistency_names):
        return "CONSISTENCY_NOT_PROVEN"
    return "NONE"


def build_safe_ledger_pnl_position_payload(
    runtime_snapshot: Mapping[str, Any] | None = None,
    ledger_snapshot: Mapping[str, Any] | None = None,
    pnl_snapshot: Mapping[str, Any] | None = None,
    position_snapshot: Mapping[str, Any] | None = None,
) -> LedgerPnlPositionPayload:
    runtime = dict(runtime_snapshot or {})
    ledger = dict(ledger_snapshot or {})
    pnl = dict(pnl_snapshot or {})
    position = dict(position_snapshot or {})
    merged = {**runtime, **ledger, **pnl, **position}
    reason = _reason(runtime, ledger, pnl, position)
    values: dict[str, Any] = {name: "UNKNOWN" for name in LEDGER_PNL_POSITION_FIELDS}
    values.update(merged)
    values.update({
        "system_mode": "PAPER",
        "ledger_provider_status": "PENDING" if not ledger else _first(ledger, "ledger_provider_status", "READY"),
        "pnl_provider_status": "PENDING" if not pnl else _first(pnl, "pnl_provider_status", "READY"),
        "position_provider_status": "PENDING" if not position else _first(position, "position_provider_status", "READY"),
        "paper_ledger_write_allowed": False,
        "live_ledger_write_allowed": False,
        "ledger_consistency": _first(merged, "ledger_consistency"),
        "pnl_consistency": _first(merged, "pnl_consistency"),
        "position_consistency": _first(merged, "position_consistency"),
        "overall_consistency": _first(merged, "overall_consistency", "BLOCKED"),
        "fail_closed_reason": reason,
        "display_only": True,
        "read_only": True,
        "can_write_ledger": False,
        "can_mutate_position": False,
        "can_recalculate_authoritatively": False,
        "can_execute": False,
        "can_start_paper": False,
        "can_start_live": False,
        "can_send_order": False,
        "next_allowed_action": "DISPLAY_ONLY_REVIEW" if reason in {"NONE", "CONSISTENCY_NOT_PROVEN"} else "WAIT_FOR_RUNTIME_PROVIDER",
        "blocked_by": [] if reason == "NONE" else [reason],
    })
    return LedgerPnlPositionPayload({name: values[name] for name in LEDGER_PNL_POSITION_FIELDS})


def validate_ledger_pnl_position_payload(payload: LedgerPnlPositionPayload) -> bool:
    values = payload.to_dict()
    if tuple(values) != LEDGER_PNL_POSITION_FIELDS or len(values) != 45:
        raise ValueError("INVALID_LEDGER_PNL_POSITION_PAYLOAD")
    for name in ("display_only", "read_only"):
        if values[name] is not True:
            raise ValueError("PAYLOAD_NOT_READ_ONLY")
    for name in ("can_write_ledger", "can_mutate_position", "can_recalculate_authoritatively", "can_execute", "can_start_paper", "can_start_live", "can_send_order", "paper_ledger_write_allowed", "live_ledger_write_allowed"):
        if values[name] is not False:
            raise ValueError("PAYLOAD_HAS_MUTATION_OR_ACTION_AUTHORITY")
    forbidden = {"START_PAPER", "START_LIVE", "SEND_ORDER", "WRITE_LEDGER"}
    if values["next_allowed_action"] in forbidden:
        raise ValueError("UNSAFE_NEXT_ACTION")
    if values["overall_consistency"] != "PASS" and not values["blocked_by"]:
        raise ValueError("BLOCKED_PAYLOAD_WITHOUT_REASON")
    return True


def get_ledger_fail_closed_reason(payload: LedgerPnlPositionPayload) -> str:
    return str(payload.to_dict()["fail_closed_reason"])


def get_ledger_blocked_by(payload: LedgerPnlPositionPayload) -> list[str]:
    blocked = payload.to_dict().get("blocked_by", [])
    return list(blocked) if blocked else []
