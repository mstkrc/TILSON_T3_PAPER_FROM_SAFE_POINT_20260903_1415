"""11_PORTFOY_ANALIZ_RAPORU display-only report."""

from ..components import donut, kv_list, line_chart, metric_card, panel, table
from .report_common import render_report_page


def render_portfolio_report_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Equity", "$12,842.54"), metric_card("Free Balance", "$9,738.32"), metric_card("Açık PnL", "+$102.54"), metric_card("Margin", "%24.2"), metric_card("Açık Coin", "9 / 10"))) + '</div>'
    primary = panel("PORTFÖY DAĞILIMI", '<div class="screen-grid grid-3">' + panel("VARLIK DAĞILIMI", donut((("USDT", 58, "#d9bb58"), ("LONG", 28, "#3cc47b"), ("SHORT", 14, "#df6060")), "$12.8K"), "fill") + panel("EQUITY EĞRİSİ", line_chart(((102, 106, 104, 111, 116, 114, 121, 128),), ("#42c681",), ("Equity",)), "fill") + panel("ALLOCATION", kv_list((("BTC", "%28"), ("ETH", "%22"), ("SOL", "%14"), ("Diğer", "%36"))), "fill") + '</div>', "fill")
    secondary = panel("PORTFÖY POZİSYONLARI", table(("Sembol", "Yön", "Allocation", "Net PnL", "Risk"), (("BTC/USDT", "LONG", "%28", "+102.54", "PASS"), ("ETH/USDT", "LONG", "%22", "+28.08", "PASS"), ("SOL/USDT", "SHORT", "%14", "-27.61", "PASS"), ("ADA/USDT", "SHORT", "%8", "-6.64", "PASS")), "dense"), "event-panel")
    return render_report_page("PORTFÖY ANALİZ RAPORU", "portfolio_report", metrics, primary, secondary, "Allocation, equity ve ledger pozisyon analizi")
