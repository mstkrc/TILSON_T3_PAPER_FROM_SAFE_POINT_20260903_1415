"""Safe route shell for 12_PERFORMANS_ANALIZI; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_performance_report_screen(model=None) -> str:
    return render_placeholder_screen("Performans Analizi", "12_PERFORMANS_ANALIZI.png", "Raporlar")
