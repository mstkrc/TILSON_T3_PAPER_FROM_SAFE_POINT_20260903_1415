"""Static, read-only contracts for Control Center runtime data sources."""

from dataclasses import asdict, dataclass
from typing import Any


_SAFE_FALLBACKS = frozenset({"UNKNOWN", "OFF", "STALE", "BLOCKED"})


@dataclass(frozen=True)
class RuntimeSource:
    name: str
    provider: str
    refresh_cadence: str
    stale_threshold: str
    fallback_state: str
    blocking_rule: str
    read_only: bool = True
    can_execute: bool = False
    can_start_paper: bool = False
    can_start_live: bool = False
    can_call_network: bool = False
    can_send_order: bool = False

    def __post_init__(self) -> None:
        if self.fallback_state not in _SAFE_FALLBACKS:
            raise ValueError("UNSAFE_FALLBACK_STATE")
        if not self.read_only or any((self.can_execute, self.can_start_paper, self.can_start_live, self.can_call_network, self.can_send_order)):
            raise ValueError("RUNTIME_SOURCE_MUST_BE_READ_ONLY")


_SOURCE_DEFINITIONS = (
    ("scheduler_status", "src.scheduler.orchestration", "2m", "5m", "UNKNOWN", "recovery gate and fresh scheduler status"),
    ("closed_candle_authority", "src.data.candle_authority", "1h", "1 candle", "BLOCKED", "closed candle required for decisions"),
    ("strategy_signal_snapshot", "src.strategy.signals", "closed candle", "1 candle", "STALE", "strategy snapshot must be fresh"),
    ("candidate_pipeline_snapshot", "src.strategy.candidates", "closed candle", "1 candle", "STALE", "candidate pipeline must be fresh"),
    ("risk_permission_snapshot", "src.risk.permission", "per evaluation", "1 candle", "BLOCKED", "risk permission required"),
    ("execution_state_snapshot", "src.paper.execution", "event plus 2m", "5m", "UNKNOWN", "paper state only and fresh"),
    ("paper_ledger_snapshot", "src.paper.ledger", "ledger event", "10m", "UNKNOWN", "ledger integrity required"),
    ("position_snapshot", "src.paper.position", "event plus 2m", "5m", "STALE", "position source must be fresh"),
    ("portfolio_pnl_snapshot", "ledger derived calculator", "ledger event plus 2m", "5m", "STALE", "ledger is single accounting source"),
    ("health_error_repair_snapshot", "src.health.monitoring", "heartbeat", "2m", "UNKNOWN", "health and recovery gate"),
    ("report_registry_snapshot", "report artifact registry", "artifact event", "10m", "UNKNOWN", "artifact must be available"),
    ("notification_event_stream", "health risk execution events", "event driven", "5m", "UNKNOWN", "event stream is informational"),
)


def build_runtime_source_registry() -> tuple[RuntimeSource, ...]:
    """Return immutable source contracts; no source is resolved or started."""
    return tuple(RuntimeSource(*definition) for definition in _SOURCE_DEFINITIONS)


def get_runtime_source_registry() -> dict[str, dict[str, Any]]:
    """Return a serializable copy of the read-only source contract."""
    return {source.name: asdict(source) for source in build_runtime_source_registry()}


_SCREEN_SOURCE_MAP = {
    "01 Overview": ("scheduler_status", "closed_candle_authority", "health_error_repair_snapshot", "paper_ledger_snapshot", "position_snapshot"),
    "02 Live Scan": ("closed_candle_authority", "candidate_pipeline_snapshot"),
    "03 Signals": ("closed_candle_authority", "strategy_signal_snapshot"),
    "04 Positions": ("position_snapshot", "paper_ledger_snapshot"),
    "05 Trade History": ("paper_ledger_snapshot",),
    "06 Charts": ("closed_candle_authority", "paper_ledger_snapshot", "portfolio_pnl_snapshot"),
    "07 Strategy": ("strategy_signal_snapshot", "closed_candle_authority"),
    "08 Risk": ("risk_permission_snapshot", "position_snapshot"),
    "09 Health": ("health_error_repair_snapshot", "scheduler_status"),
    "10 Reports": ("report_registry_snapshot", "paper_ledger_snapshot"),
    "11 Portfolio": ("portfolio_pnl_snapshot", "paper_ledger_snapshot", "position_snapshot"),
    "12 Performance": ("portfolio_pnl_snapshot", "paper_ledger_snapshot"),
    "13 Trade Analysis": ("paper_ledger_snapshot",),
    "14 Risk Center": ("risk_permission_snapshot", "health_error_repair_snapshot"),
    "15 Strategy Reports": ("strategy_signal_snapshot", "paper_ledger_snapshot"),
    "16 Custom Reports": ("report_registry_snapshot", "paper_ledger_snapshot"),
    "17 Notifications": ("notification_event_stream", "health_error_repair_snapshot"),
}


def get_screen_source_map() -> dict[str, tuple[str, ...]]:
    """Return the static 01-17 screen-to-source mapping."""
    return {screen: tuple(sources) for screen, sources in _SCREEN_SOURCE_MAP.items()}
