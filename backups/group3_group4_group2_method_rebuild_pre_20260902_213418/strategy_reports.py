"""15_STRATEJI_RAPORLARI display-only report."""

from ..components import bar_chart, donut, kv_list, line_chart, metric_card, panel, table
from .report_common import render_report_page


def render_strategy_reports_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Strateji", "Tilson T3 Slope"), metric_card("Signal PASS", "74"), metric_card("Win Rate", "%64.1"), metric_card("Net PnL", "+$486.20"), metric_card("Auto Apply", "YOK"))) + '</div>'
    primary = panel("STRATEJİ PERFORMANSI", '<div class="screen-grid grid-3">' + panel("PNL EĞRİSİ", line_chart(((3, 8, 7, 14, 19, 17, 26, 34, 41),), ("#42c67d",), ("Tilson T3",)), "fill") + panel("ENTRY MODE", donut((("DEĞİŞİM", 61, "#4da7d8"), ("DEVAM", 67, "#d4b957")), "128"), "fill") + panel("FİLTRE ETKİSİ", bar_chart((68, 61, 72, 64), labels=("T3", "DMI", "ADX", "Volume")), "fill") + '</div>', "fill")
    secondary = panel("STRATEJİ KIRILIMI", table(("Profil", "İşlem", "Win %", "Net PnL", "Durum"), (("PAPER DEFAULT", "128", "%64.1", "+486.20", "AKTİF"), ("CONSERVATIVE", "—", "—", "—", "DISPLAY"), ("RESEARCH", "—", "—", "—", "KİLİTLİ")), "dense") + kv_list((("Optimization transfer", "YOK"), ("Direct apply", "YASAK"), ("Historical mini backtest", "YOK"))), "event-panel")
    return render_report_page("STRATEJİ RAPORLARI", "strategy_reports", metrics, primary, secondary, "Strateji sonuçları; trade_config mutation yok")
