"""Safe route shell for 15_STRATEJI_RAPORLARI; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_strategy_reports_screen(model=None) -> str:
    return render_placeholder_screen("Strateji Raporları", "15_STRATEJI_RAPORLARI.png", "Raporlar")
