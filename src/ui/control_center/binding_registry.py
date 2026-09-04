"""Read-only bindings between Control Center screens and runtime sources."""

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from .runtime_sources import get_runtime_source_registry, get_screen_source_map


_FALLBACK_STATES = frozenset({"UNKNOWN", "OFF", "STALE", "BLOCKED", "READY"})


@dataclass(frozen=True)
class ScreenBinding:
    screen_name: str
    source_names: tuple[str, ...]
    refresh_cadence: str
    stale_threshold: str
    fallback_state: str
    blocking_rule: str
    read_only: bool = True
    display_only: bool = True
    can_execute: bool = False
    can_start_paper: bool = False
    can_start_live: bool = False
    can_call_network: bool = False
    can_send_order: bool = False


_POLICY = {
    "01 Overview": ("2m", "5m", "UNKNOWN", "fresh status and recovery gate required"),
    "02 Live Scan": ("closed candle", "1 candle", "STALE", "closed candle required"),
    "03 Signals": ("closed candle", "1 candle", "STALE", "fresh strategy snapshot required"),
    "04 Positions": ("event plus 2m", "5m", "STALE", "fresh position state required"),
    "05 Trade History": ("ledger event", "10m", "UNKNOWN", "ledger integrity required"),
    "06 Charts": ("closed candle plus ledger event", "1 candle", "STALE", "display only; no decision"),
    "07 Strategy": ("evaluation event", "1 candle", "UNKNOWN", "config and strategy state are read-only"),
    "08 Risk": ("per evaluation", "1 candle", "BLOCKED", "risk permission required"),
    "09 Health": ("heartbeat", "2m", "STALE", "health and recovery gate required"),
    "10 Reports": ("artifact event", "10m", "UNKNOWN", "artifact availability required"),
    "11 Portfolio": ("ledger event plus 2m", "5m", "STALE", "ledger is single accounting source"),
    "12 Performance": ("ledger event", "10m", "UNKNOWN", "valid ledger required"),
    "13 Trade Analysis": ("ledger event", "10m", "UNKNOWN", "valid trade records required"),
    "14 Risk Center": ("risk event plus 2m", "5m", "BLOCKED", "risk and recovery gates required"),
    "15 Strategy Reports": ("evaluation event", "10m", "STALE", "fresh strategy evaluation required"),
    "16 Custom Reports": ("on query", "10m", "UNKNOWN", "bounded read-only query required"),
    "17 Notifications": ("event driven", "5m", "UNKNOWN", "informational event stream only"),
}


def build_binding_registry() -> tuple[ScreenBinding, ...]:
    source_map = get_screen_source_map()
    return tuple(
        ScreenBinding(screen, tuple(source_map[screen]), *policy)
        for screen, policy in _POLICY.items()
    )


def get_binding_registry() -> dict[str, dict[str, Any]]:
    return {binding.screen_name: asdict(binding) for binding in build_binding_registry()}


def get_binding_for_screen(screen_name: str) -> dict[str, Any]:
    registry = get_binding_registry()
    if screen_name not in registry:
        raise KeyError(screen_name)
    return registry[screen_name]


def validate_binding_registry(
    bindings: Iterable[ScreenBinding] | None = None,
    source_registry: Mapping[str, Any] | None = None,
) -> bool:
    items = tuple(bindings or build_binding_registry())
    sources = source_registry or get_runtime_source_registry()
    if len(items) != 17 or {item.screen_name for item in items} != set(_POLICY):
        raise ValueError("INCOMPLETE_SCREEN_BINDING_REGISTRY")
    for item in items:
        if not item.source_names or not set(item.source_names) <= set(sources):
            raise ValueError("UNKNOWN_RUNTIME_SOURCE")
        if item.fallback_state not in _FALLBACK_STATES:
            raise ValueError("UNSAFE_FALLBACK_STATE")
        if not item.read_only or not item.display_only:
            raise ValueError("BINDING_MUST_BE_DISPLAY_ONLY")
        if any((item.can_execute, item.can_start_paper, item.can_start_live, item.can_call_network, item.can_send_order)):
            raise ValueError("BINDING_HAS_ACTIVE_CAPABILITY")
    return True
