"""13_ISLEM_ANALIZI display-only report."""

from ..components import bar_chart, donut, kv_list, line_chart, metric_card, panel, table
from ..data import TRADE_ROWS
from .report_common import render_report_page


def render_trade_analysis_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Toplam İşlem", "128"), metric_card("LONG", "76"), metric_card("SHORT", "52"), metric_card("Ort. Süre", "1sa 24dk"), metric_card("Ort. PnL", "+%0.68"))) + '</div>'
    trades = table(("Tarih", "Sembol", "Yön", "Net PnL", "PnL %", "Mode", "Sonuç"), ((r[0], r[1], r[2], r[5], r[6], r[7], r[10]) for r in TRADE_ROWS), "dense")
    primary = panel("İŞLEM ANALİZİ", '<div class="screen-grid grid-3 trade-top-row">' +
        panel("İŞLEMLER", trades, "fill") + panel("İŞLEM SAYISI TRENDİ", line_chart(((12, 18, 15, 24, 31, 22, 28),), ("#4aa7c7",), ("Trades",)), "fill") +
        panel("SAATLİK DAĞILIM", bar_chart((12, 18, -5, 24, 31, 16, -8, 20), labels=("10", "11", "12", "13", "14", "15", "16", "17")), "fill") +
        '</div><div class="screen-grid grid-3 trade-lower-row">' + panel("GÜNLÜK PERFORMANS", kv_list((("Bugün", "+48.20"), ("7 Gün", "+184.50"), ("30 Gün", "+486.20"))), "fill") + panel("EN İYİ / KÖTÜ İŞLEMLER", table(("Tip", "Sembol", "PnL"), (("En iyi", "BTC/USDT", "+42.10"), ("En kötü", "SOL/USDT", "-18.40")), "dense"), "fill") + panel("SONUÇ DAĞILIMI", donut((("Kâr", 82, "#38c67b"), ("Zarar", 41, "#df5e5e"), ("BE", 5, "#76859a")), "128"), "fill") + '</div>', "fill")
    secondary = panel("SLIPPAGE / COMMISSION", table(("Alan", "Değer", "Durum"), (("Ortalama slippage", "%0.04", "PASS"), ("Commission", "$12.40", "PASS"), ("Ledger sonucu", "128", "PASS")), "dense"), "event-panel")
    return render_report_page("İŞLEM ANALİZİ", "trade_analysis", metrics, primary, secondary, "Yön, süre ve sinyal modu kırılımı")
