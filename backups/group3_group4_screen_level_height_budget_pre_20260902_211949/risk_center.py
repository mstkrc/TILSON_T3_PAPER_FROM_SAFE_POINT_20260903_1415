"""14_RISK_MERKEZI display-only report."""

from ..components import bar_chart, line_chart, metric_card, panel, progress, table
from .report_common import render_report_page


def render_risk_center_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Açık Risk", "$428.70"), metric_card("Margin", "%24.2"), metric_card("Max DD", "-%4.8"), metric_card("VaR 95%", "$182.40"), metric_card("Permission", "PASS"))) + '</div>'
    primary = panel("RİSK MERKEZİ", '<div class="screen-grid grid-3">' + panel("RİSK EĞRİSİ", line_chart(((18, 22, 20, 27, 25, 31, 29, 35), (42, 41, 39, 37, 35, 33, 31, 29)), ("#dfbd58", "#d85a5a"), ("Risk", "Limit")), "fill") + panel("LIMIT KULLANIMI", progress("Coin", 90, "yellow", "9 / 10") + progress("Margin", 24, "green") + progress("Daily loss", 16, "green") + progress("Allocation", 64, "blue"), "fill") + panel("DD GÜNLÜK", bar_chart((-1, -2, -1, -4, -3, -2, -1), labels=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")), "fill") + '</div>', "fill")
    secondary = panel("RİSK OLAYLARI", table(("Saat", "Kural", "Değer", "Sonuç"), (("19:42", "Risk permission", "%3.34", "PASS"), ("19:41", "Coin limit", "9 / 10", "WARNING"), ("19:40", "Same-symbol", "LOCK", "PASS"), ("19:39", "Live-lock", "false", "PASS")), "dense"), "event-panel")
    return render_report_page("RİSK MERKEZİ", "risk_center", metrics, primary, secondary, "Risk limitleri ve ihlal görünümü")
