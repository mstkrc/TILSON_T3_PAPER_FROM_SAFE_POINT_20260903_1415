"""15_STRATEJI_RAPORLARI display-only report."""

from ..components import bar_chart, donut, kv_list, line_chart, metric_card, panel, table
from .report_common import render_report_page


def render_strategy_reports_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Strateji", "Tilson T3 Slope"), metric_card("Signal PASS", "74"), metric_card("Win Rate", "%64.1"), metric_card("Net PnL", "+$486.20"), metric_card("Auto Apply", "YOK"))) + '</div>'
    primary = panel("STRATEJİ RAPORLARI", '<div class="screen-grid grid-3 strategy-report-top">' + panel("STRATEJİ KARŞILAŞTIRMA", table(("Profil", "İşlem", "Win %", "Net PnL", "Durum"), (("Tilson T3 Slope", "128", "%64.1", "+486.20", "PASS"), ("Değişim", "61", "%68.0", "+312.10", "PASS"), ("Devam", "67", "%61.2", "+174.10", "PASS")), "dense"), "fill") + panel("KALİTE DAĞILIMI", donut((("PASS", 74, "#3cc47b"), ("BLOCK", 12, "#df6060"), ("WAIT", 14, "#d9bb58")), "74"), "fill") + panel("FİLTRE ETKİSİ", bar_chart((68, 61, 72, 64), labels=("T3", "DMI", "ADX", "Volume")), "fill") + '</div><div class="screen-grid grid-3 strategy-report-lower">' + panel("PARAMETRE ÖZETİ", kv_list((("T3 Factor", "0.70"), ("T3 Period", "8"), ("ADX", "25"), ("Volume", "ON"))), "fill") + panel("BLOCK ANALİZİ", table(("Neden", "Sayı", "Durum"), (("Weak ADX", "18", "INFO"), ("Volume", "9", "INFO"), ("Risk", "3", "WARNING")), "dense"), "fill") + panel("RAPOR TRENDİ", line_chart(((3, 8, 7, 14, 19, 17, 26, 34, 41),), ("#42c67d",), ("Tilson T3",)), "fill") + '</div>', "fill")
    secondary = panel("SON STRATEJİ RAPORLARI", table(("Rapor", "Saat", "Durum"), (("Günlük strateji", "19:30", "PASS"), ("Signal quality", "19:00", "PASS"), ("Block analysis", "18:30", "PASS")), "dense"), "event-panel")
    return render_report_page("STRATEJİ RAPORLARI", "strategy_reports", metrics, primary, secondary, "Strateji sonuçları; trade_config mutation yok")
