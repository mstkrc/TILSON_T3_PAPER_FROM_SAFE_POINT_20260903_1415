"""12_PERFORMANS_ANALIZI display-only report."""

from ..components import bar_chart, donut, line_chart, metric_card, panel, table
from .report_common import render_report_page


def render_performance_report_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-6 top-band">' + ''.join((metric_card("Net PnL", "+$486.20"), metric_card("Win Rate", "%64.1"), metric_card("Profit Factor", "1.84"), metric_card("Sharpe", "1.62"), metric_card("Max DD", "-%4.8"), metric_card("İşlem", "128"))) + '</div>'
    primary = panel("PERFORMANS GÖRÜNÜMÜ", '<div class="screen-grid grid-3">' + panel("KÜMÜLATİF PNL", line_chart(((2, 8, 6, 15, 21, 18, 31, 39, 47),), ("#42c981",), ("Net PnL",)), "fill") + panel("GÜNLÜK SONUÇ", bar_chart((18, -7, 24, 14, -11, 31, 22), labels=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")), "fill") + panel("KÂR / ZARAR", donut((("KÂR", 82, "#38c67b"), ("ZARAR", 41, "#df5e5e"), ("BE", 5, "#76859a")), "128"), "fill") + '</div>', "fill")
    secondary = panel("PERFORMANS KIRILIMI", table(("Dönem", "İşlem", "Win %", "Net PnL", "DD"), (("Bugün", "12", "%66.7", "+48.20", "-%0.8"), ("7 Gün", "54", "%63.0", "+184.50", "-%2.1"), ("30 Gün", "128", "%64.1", "+486.20", "-%4.8")), "dense"), "event-panel")
    return render_report_page("PERFORMANS ANALİZİ", "performance_report", metrics, primary, secondary, "Ledger tabanlı performans metrikleri")
