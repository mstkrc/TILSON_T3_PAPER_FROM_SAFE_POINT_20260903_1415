"""14_RISK_MERKEZI display-only report."""

from ..components import bar_chart, donut, line_chart, metric_card, panel, progress, table
from .report_common import render_report_page


def render_risk_center_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Açık Risk", "$428.70"), metric_card("Margin", "%24.2"), metric_card("Max DD", "-%4.8"), metric_card("VaR 95%", "$182.40"), metric_card("Permission", "PASS"))) + '</div>'
    primary = panel("RİSK MERKEZİ", '<div class="screen-grid grid-3 risk-top-row">' + panel("RİSK OLAY GÜNLÜĞÜ", table(("Saat", "Kural", "Değer", "Sonuç"), (("19:42", "Risk permission", "%3.34", "PASS"), ("19:41", "Coin limit", "9 / 10", "WARNING"), ("19:40", "Same-symbol", "LOCK", "PASS"), ("19:39", "Live-lock", "false", "PASS")), "dense"), "fill") + panel("EXPOSURE", donut((("BTC", 28, "#d9bb58"), ("ETH", 22, "#3cc47b"), ("Diğer", 50, "#4aa7c7")), "%64"), "fill") + panel("DRAWDOWN", line_chart(((-1, -2, -1, -4, -3, -2, -1),), ("#df5e5e",), ("DD",)), "fill") + '</div><div class="screen-grid grid-4 risk-lower-row">' + panel("YOĞUNLAŞMA", progress("BTC", 28, "yellow") + progress("ETH", 22, "green") + progress("Diğer", 50, "blue"), "fill") + panel("BLOCK REASON", table(("Neden", "Sayı"), (("Risk limit", "3"), ("Coin limit", "2"), ("Veri", "0")), "dense"), "fill") + panel("RİSK KURALLARI", table(("Kural", "Durum"), (("Max coin", "PASS"), ("Stop loss", "ON"), ("Closed candle", "PASS")), "dense"), "fill") + panel("YÜKSEK RİSK", table(("Sembol", "Risk", "Durum"), (("SOL/USDT", "%8.2", "WARNING"), ("ADA/USDT", "%5.1", "PASS")), "dense"), "fill") + '</div>', "fill")
    secondary = panel("RİSK AKIŞI", table(("Saat", "Olay", "Sonuç"), (("19:42", "Exposure check", "PASS"), ("19:41", "Drawdown check", "PASS"), ("19:40", "Permission check", "PASS")), "dense"), "event-panel")
    return render_report_page("RİSK MERKEZİ", "risk_center", metrics, primary, secondary, "Risk limitleri ve ihlal görünümü")
