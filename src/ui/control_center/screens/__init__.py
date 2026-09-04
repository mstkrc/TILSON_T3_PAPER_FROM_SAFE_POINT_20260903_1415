"""Screen registry for the modular, paper-only Control Center."""

from __future__ import annotations

from ..data import REPORT_TAB_KEYS, SCREEN_KEYS
from ..model import ControlCenterModel, build_control_center
from .charts import render_charts_screen
from .custom_reports import render_custom_reports_screen
from .live_scan import render_live_scan_screen
from .notifications import render_notifications_screen
from .overview import render_overview_screen
from .performance_report import render_performance_report_screen
from .portfolio_report import render_portfolio_report_screen
from .positions import render_positions_screen
from .report_center import render_report_center_screen
from .risk import render_risk_screen
from .risk_center import render_risk_center_screen
from .signals import render_signals_screen
from .strategy import render_strategy_screen
from .strategy_reports import render_strategy_reports_screen
from .system_health import render_system_health_screen
from .trade_analysis import render_trade_analysis_screen
from .trade_history import render_trade_history_screen

SCREEN_RENDERERS = {
    "overview": render_overview_screen,
    "live_scan": render_live_scan_screen,
    "signals": render_signals_screen,
    "positions": render_positions_screen,
    "trade_history": render_trade_history_screen,
    "charts": render_charts_screen,
    "strategy": render_strategy_screen,
    "risk": render_risk_screen,
    "system_health": render_system_health_screen,
    "report_center": render_report_center_screen,
    "portfolio_report": render_portfolio_report_screen,
    "performance_report": render_performance_report_screen,
    "trade_analysis": render_trade_analysis_screen,
    "risk_center": render_risk_center_screen,
    "strategy_reports": render_strategy_reports_screen,
    "custom_reports": render_custom_reports_screen,
    "notifications": render_notifications_screen,
}


def render_screen(
    screen: str,
    model: ControlCenterModel | None = None,
    report_tab: str | None = None,
) -> str:
    """Render an approved route without creating decision or execution side effects."""
    model = model or build_control_center()
    if screen not in model.screens:
        raise ValueError(f"Unknown Control Center screen: {screen}")

    if screen == "Raporlar":
        tab = report_tab or model.active_report_tab
        if tab not in model.report_tabs:
            raise ValueError(f"Unknown report tab: {tab}")
        key = REPORT_TAB_KEYS[tab]
    else:
        key = SCREEN_KEYS[screen]

    return SCREEN_RENDERERS[key](model)


__all__ = [
    "SCREEN_RENDERERS",
    "render_screen",
    "render_overview_screen",
    "render_live_scan_screen",
    "render_signals_screen",
    "render_positions_screen",
    "render_trade_history_screen",
    "render_charts_screen",
    "render_strategy_screen",
    "render_risk_screen",
    "render_system_health_screen",
    "render_report_center_screen",
    "render_portfolio_report_screen",
    "render_performance_report_screen",
    "render_trade_analysis_screen",
    "render_risk_center_screen",
    "render_strategy_reports_screen",
    "render_custom_reports_screen",
    "render_notifications_screen",
]
