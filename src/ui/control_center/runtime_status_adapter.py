"""Read-only runtime status snapshot adapter for the Control Center."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from src.health.live_lock import load_and_validate


_DOMAINS = (
    "scheduler",
    "candle",
    "strategy",
    "risk",
    "execution",
    "ledger",
    "positions",
    "health",
)


def _domain_states(
    runtime_sources: Mapping[str, Any] | None,
    stale_domains: set[str],
    blocked_domains: set[str],
) -> dict[str, Any]:
    sources = runtime_sources or {}
    result: dict[str, Any] = {}
    for domain in _DOMAINS:
        if domain in blocked_domains:
            result[domain] = {"state": "BLOCKED"}
        elif domain in stale_domains:
            result[domain] = {"state": "STALE"}
        elif domain in sources:
            result[domain] = {"state": "READY", "value": sources[domain]}
        else:
            result[domain] = {"state": "UNKNOWN"}
    return result


def build_runtime_status_snapshot(
    *,
    config_path: str | Path = "config/live_lock_config.json",
    runtime_sources: Mapping[str, Any] | None = None,
    stale_domains: tuple[str, ...] = (),
    blocked_domains: tuple[str, ...] = (),
    now: datetime | None = None,
) -> dict[str, Any]:
    """Build a passive status snapshot without starting or calling any runtime."""
    config, violation = load_and_validate(config_path)
    stale = set(stale_domains)
    blocked = set(blocked_domains)
    domains = _domain_states(runtime_sources, stale, blocked)

    if violation is not None:
        failure_state = "BLOCKED"
    elif blocked:
        failure_state = "BLOCKED"
    elif stale:
        failure_state = "STALE"
    elif not runtime_sources:
        failure_state = "UNKNOWN"
    else:
        failure_state = "READY"

    generated_at = (now or datetime.now(timezone.utc)).isoformat()
    return {
        "generated_at": generated_at,
        "paper": "OFF",
        "live": "OFF_LOCKED",
        "LIVE_TRADING": config["LIVE_TRADING"],
        "live_order_sending_allowed": config["live_order_sending_allowed"],
        "data_binding": "DESIGN_READY_NOT_IMPLEMENTED",
        **domains,
        "failure_state": failure_state,
        "stale_domains": sorted(stale),
        "decision_allowed": False,
        "execution_triggered": False,
        "live_order_sent": False,
        "paper_start_triggered": False,
    }
