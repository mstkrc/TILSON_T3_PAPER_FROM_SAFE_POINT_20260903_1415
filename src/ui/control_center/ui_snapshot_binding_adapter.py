"""Read-only binding of runtime status snapshots to Control Center screens."""

from typing import Any, Mapping

from .binding_registry import get_binding_registry, validate_binding_registry
from .runtime_sources import get_runtime_source_registry
from .runtime_status_adapter import build_runtime_status_snapshot


_SOURCE_TO_DOMAIN = {
    "scheduler_status": "scheduler",
    "closed_candle_authority": "candle",
    "strategy_signal_snapshot": "strategy",
    "candidate_pipeline_snapshot": "candidate",
    "risk_permission_snapshot": "risk",
    "execution_state_snapshot": "execution",
    "paper_ledger_snapshot": "ledger",
    "position_snapshot": "positions",
    "portfolio_pnl_snapshot": "portfolio",
    "health_error_repair_snapshot": "health",
    "report_registry_snapshot": "reports",
    "notification_event_stream": "notifications",
}


def _source_state(source_name: str, runtime_snapshot: Mapping[str, Any]) -> str:
    domain = _SOURCE_TO_DOMAIN[source_name]
    value = runtime_snapshot.get(domain)
    if isinstance(value, Mapping):
        return str(value.get("state", "UNKNOWN"))
    return "UNKNOWN"


def _screen_state(binding: Mapping[str, Any], source_states: Mapping[str, str], runtime_state: str) -> str:
    if runtime_state == "BLOCKED" or "BLOCKED" in source_states.values():
        return "BLOCKED"
    if "STALE" in source_states.values():
        return "STALE"
    if all(state == "READY" for state in source_states.values()):
        return "READY"
    return binding["fallback_state"] if all(state == "UNKNOWN" for state in source_states.values()) else "UNKNOWN"


def build_bound_ui_snapshot(
    *,
    runtime_snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Combine passive runtime status, source, and screen binding contracts."""
    snapshot = dict(runtime_snapshot or build_runtime_status_snapshot())
    source_registry = get_runtime_source_registry()
    binding_registry = get_binding_registry()
    validate_binding_registry(source_registry=source_registry)
    screens: dict[str, dict[str, Any]] = {}
    runtime_state = str(snapshot.get("failure_state", "UNKNOWN"))
    for screen_name, binding in binding_registry.items():
        source_states = {
            source: _source_state(source, snapshot)
            for source in binding["source_names"]
        }
        screens[screen_name] = {
            "screen_name": screen_name,
            "sources": list(binding["source_names"]),
            "source_states": source_states,
            "fallback_state": _screen_state(binding, source_states, runtime_state),
            "display_only": True,
            "read_only": True,
            "decision_allowed": False,
            "execution_triggered": False,
            "paper_start_triggered": False,
            "live_order_sent": False,
        }
    return {
        "generated_at": snapshot.get("generated_at"),
        "paper": snapshot.get("paper", "OFF"),
        "live": snapshot.get("live", "OFF_LOCKED"),
        "LIVE_TRADING": snapshot.get("LIVE_TRADING", False),
        "live_order_sending_allowed": snapshot.get("live_order_sending_allowed", False),
        "failure_state": runtime_state,
        "screens": screens,
    }


def get_screen_bound_snapshot(screen_name: str, *, runtime_snapshot: Mapping[str, Any] | None = None) -> dict[str, Any]:
    bound = build_bound_ui_snapshot(runtime_snapshot=runtime_snapshot)
    if screen_name not in bound["screens"]:
        raise KeyError(screen_name)
    return bound["screens"][screen_name]


def validate_bound_ui_snapshot(bound_snapshot: Mapping[str, Any]) -> bool:
    screens = bound_snapshot.get("screens")
    if not isinstance(screens, Mapping) or len(screens) != 17:
        raise ValueError("INVALID_BOUND_SCREEN_COUNT")
    if bound_snapshot.get("LIVE_TRADING") is not False or bound_snapshot.get("live_order_sending_allowed") is not False:
        raise ValueError("LIVE_LOCK_NOT_PRESERVED")
    for screen in screens.values():
        if not screen.get("read_only") or not screen.get("display_only"):
            raise ValueError("SCREEN_NOT_DISPLAY_ONLY")
        if any(screen.get(key) is not False for key in ("decision_allowed", "execution_triggered", "paper_start_triggered", "live_order_sent")):
            raise ValueError("SCREEN_HAS_ACTIVE_RESULT")
    return True
