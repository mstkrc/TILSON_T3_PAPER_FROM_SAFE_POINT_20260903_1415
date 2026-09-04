"""05_ISLEM_GECMISI ledger-sourced display-only history."""

from ..components import bar_chart, donut, field, kv_list, metric_card, panel, scroll_container, table
from ..data import TRADE_ROWS
from ..layout import render_screen


def render_trade_history_screen(model=None) -> str:
    filters = panel("FİLTRELER", '<div class="field-grid">' + field("Başlangıç", "01.05.2026") + field("Bitiş", "19.05.2026") + field("Sembol", "TÜMÜ") + field("Yön", "TÜMÜ") + '</div>', "compact")
    summary = panel("İŞLEM ÖZETİ", '<div class="metric-grid grid-3">' + metric_card("Toplam", "128") + metric_card("Kârlı", "82") + metric_card("Zararlı", "41") + '</div>', "compact")
    daily = panel("GÜNLÜK PNL", bar_chart((18, -7, 24, 14, -11, 31, 22), labels=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")), "compact")
    result = panel("SONUÇ DAĞILIMI", donut((("KÂR", 82, "#30c47a"), ("ZARAR", 41, "#df5c5c"), ("BE", 5, "#77859a")), "64%"), "compact")
    top = f'<div class="screen-grid grid-4 top-band">{filters}{summary}{daily}{result}</div>'
    history = panel("İŞLEM GEÇMİŞİ", scroll_container(table(("Tarih / Saat", "Sembol", "Yön", "Giriş", "Çıkış", "Net PnL", "PnL %", "Mode", "T3", "Slope", "Sonuç"), TRADE_ROWS, "dense wide-table"), "Ledger işlem geçmişi"), "fill", "LEDGER SINGLE SOURCE")
    detail = panel("SEÇİLİ İŞLEM DETAYI", kv_list((("Sembol", "BTC/USDT"), ("Yön", "LONG"), ("Entry", "68,102.45"), ("Exit", "68,302.54"), ("Gross PnL", "+7.90"), ("Commission", "-1.26"), ("Funding", "-0.22"), ("Slippage", "0.00"), ("Net PnL", "+6.42"), ("Decision candle", "19.05.2026 18:00 UTC+3"), ("Config snapshot", "LEDGER-REF-1038"))), "fill")
    detail_chart = panel("İŞLEM SONUCU", donut((("Net", 642, "#38c47a"), ("Maliyet", 148, "#ddbf62")), "+6.42"), "compact")
    footer = '<div class="screen-grid grid-3 lower-row">' + panel("EN İYİ / EN KÖTÜ", kv_list((("En iyi", "MATIC +38.80"), ("En kötü", "LINK -4.44"))), "compact") + panel("SÜRE ANALİZİ", kv_list((("Ort. süre", "1sa 24dk"), ("En uzun", "4sa 18dk"))), "compact") + panel("LEDGER KONTROLÜ", kv_list((("PnL mismatch", "YOK"), ("Kayıt durumu", "PASS"))), "compact") + '</div>'
    body = top + f'<div class="screen-grid with-rail fill"><div class="stack fill">{history}{footer}</div><aside class="stack fill">{detail}{detail_chart}</aside></div>'
    return render_screen("İŞLEM GEÇMİŞİ", "İşlem Geçmişi", body, "Ledger kaynaklı PnL, maliyet ve config snapshot görünümü", "trade-history-screen")
