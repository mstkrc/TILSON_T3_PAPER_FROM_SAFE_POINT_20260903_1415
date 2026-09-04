"""11_PORTFOY_ANALIZ_RAPORU display-only report."""

from ..components import donut, kv_list, line_chart, metric_card, panel, table
from .report_common import render_report_page


def render_portfolio_report_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-6 top-band">' + ''.join((
        metric_card("Equity", "$12,842.54"), metric_card("Free Balance", "$9,738.32"),
        metric_card("Açık PnL", "+$102.54"), metric_card("Margin", "%24.2"),
        metric_card("Açık Coin", "9 / 10"), metric_card("Günlük Değişim", "+%1.8"))) + '</div>'
    assets = table(("Sembol", "Yön", "Allocation", "Net PnL", "Risk"), (
        ("BTC/USDT", "LONG", "%28", "+102.54", "PASS"), ("ETH/USDT", "LONG", "%22", "+28.08", "PASS"),
        ("SOL/USDT", "SHORT", "%14", "-27.61", "PASS"), ("ADA/USDT", "SHORT", "%8", "-6.64", "PASS")), "dense")
    primary = panel("RAPOR MERKEZİ > PORTFÖY ANALİZ RAPORU", '<div class="screen-grid grid-2 portfolio-top-row">' +
        panel("PORTFÖY DEĞERİ ZAMAN GRAFİĞİ", line_chart(((102, 106, 104, 111, 116, 114, 121, 128),), ("#42c681",), ("Equity",)), "fill") +
        panel("VARLIK DAĞILIMI", donut((("USDT", 58, "#d9bb58"), ("LONG", 28, "#3cc47b"), ("SHORT", 14, "#df6060")), "$12.8K"), "fill") +
        '</div><div class="screen-grid grid-2 portfolio-bottom-row">' +
        panel("VARLIK PERFORMANSI", assets, "fill") +
        panel("VARLIK DETAYLARI", table(("Sembol", "Fiyat", "Miktar", "Değer"), (("BTC/USDT", "$68,420", "0.042", "$2,873"), ("ETH/USDT", "$3,420", "0.81", "$2,770"), ("SOL/USDT", "$178", "15.2", "$2,706")), "dense"), "fill") + '</div>', "fill")
    secondary = panel("GETİRİ ANALİZİ / RİSK METRİKLERİ", kv_list((("Toplam getiri", "+%8.42"), ("Volatilite", "%4.1"), ("Sharpe", "1.62"), ("Max DD", "-%4.8"), ("Ledger kaynak", "PASS"))), "event-panel")
    return render_report_page("PORTFÖY ANALİZ RAPORU", "portfolio_report", metrics, primary, secondary, "Allocation, equity ve ledger pozisyon analizi")
