"""13_ISLEM_ANALIZI display-only report."""

from ..components import bar_chart, donut, kv_list, metric_card, panel, table
from ..data import TRADE_ROWS
from .report_common import render_report_page


def render_trade_analysis_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Toplam İşlem", "128"), metric_card("LONG", "76"), metric_card("SHORT", "52"), metric_card("Ort. Süre", "1sa 24dk"), metric_card("Ort. PnL", "+%0.68"))) + '</div>'
    primary = panel("İŞLEM ANALİZİ", '<div class="screen-grid grid-3">' + panel("YÖN DAĞILIMI", donut((("LONG", 76, "#39c57b"), ("SHORT", 52, "#df5d5d")), "128"), "fill") + panel("SAATLİK PERFORMANS", bar_chart((12, 18, -5, 24, 31, 16, -8, 20), labels=("10", "11", "12", "13", "14", "15", "16", "17")), "fill") + panel("SİNYAL KIRILIMI", kv_list((("DEĞİŞİM", "61 / %68 win"), ("DEVAM", "67 / %61 win"), ("LONG", "%66 win"), ("SHORT", "%62 win"))), "fill") + '</div>', "fill")
    secondary = panel("İŞLEM DETAYLARI", table(("Tarih", "Sembol", "Yön", "Net PnL", "PnL %", "Mode", "Sonuç"), ((r[0], r[1], r[2], r[5], r[6], r[7], r[10]) for r in TRADE_ROWS), "dense"), "event-panel")
    return render_report_page("İŞLEM ANALİZİ", "trade_analysis", metrics, primary, secondary, "Yön, süre ve sinyal modu kırılımı")
