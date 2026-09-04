"""12_PERFORMANS_ANALIZI display-only report."""

from ..components import bar_chart, donut, line_chart, metric_card, panel, table
from .report_common import render_report_page


def render_performance_report_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band performance-metrics">' + ''.join((
        metric_card("Net PnL", "+$486.20"), metric_card("Win Rate", "%64.1"), metric_card("Profit Factor", "1.84"),
        metric_card("Sharpe", "1.62"), metric_card("Max DD", "-%4.8"), metric_card("Toplam İşlem", "128"),
        metric_card("Ortalama İşlem", "+%0.68"), metric_card("Kazanılan", "82"), metric_card("Kaybedilen", "41"),
        metric_card("Beklemede", "5"))) + '</div>'
    filters = '<div class="field-grid grid-4 report-filter-row"><label class="display-field"><span>Dönem</span><b>01.09 – 02.09</b></label><label class="display-field"><span>Sembol</span><b>TÜMÜ</b></label><label class="display-field"><span>Mod</span><b>PAPER / CLOSED</b></label><label class="display-field"><span>Kaynak</span><b>LEDGER</b></label></div>'
    primary = panel("PERFORMANS ANALİZİ", filters + '<div class="screen-grid grid-3 performance-chart-row">' +
        panel("KÜMÜLATİF GETİRİ", line_chart(((2, 8, 6, 15, 21, 18, 31, 39, 47),), ("#42c981",), ("Net PnL",)), "fill") +
        panel("EQUITY CURVE", line_chart(((100, 104, 103, 108, 112, 111, 118, 124, 128),), ("#d9bb58",), ("Equity",)), "fill") +
        panel("AYLIK DAĞILIM", bar_chart((18, -7, 24, 14, -11, 31, 22), labels=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")), "fill") +
        '</div><div class="screen-grid grid-3 performance-lower-row">' +
        panel("PERFORMANS ÖZETİ", table(("Dönem", "İşlem", "Win %", "Net PnL"), (("Bugün", "12", "%66.7", "+48.20"), ("7 Gün", "54", "%63.0", "+184.50"), ("30 Gün", "128", "%64.1", "+486.20")), "dense"), "fill") +
        panel("KÂR / ZARAR", donut((("KÂR", 82, "#38c67b"), ("ZARAR", 41, "#df5e5e"), ("BE", 5, "#76859a")), "128"), "fill") +
        panel("DRAWDOWN", line_chart(((-1, -2, -1, -4, -3, -2, -1),), ("#df5e5e",), ("DD",)), "fill") + '</div>', "fill")
    secondary = panel("STRATEJİ PERFORMANSI", table(("Strateji", "İşlem", "Win %", "Net PnL", "DD"), (("Tilson T3 Slope", "128", "%64.1", "+486.20", "-%4.8"), ("Değişim", "61", "%68.0", "+312.10", "-%3.1"), ("Devam", "67", "%61.2", "+174.10", "-%4.8")), "dense"), "event-panel")
    return render_report_page("PERFORMANS ANALİZİ", "performance_report", metrics, primary, secondary, "Ledger tabanlı performans metrikleri")
