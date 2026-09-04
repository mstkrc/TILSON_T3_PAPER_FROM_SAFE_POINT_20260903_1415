"""08_RISK display-only risk operations screen."""

from ..components import action_stack, bar_chart, kv_list, line_chart, metric_card, panel, progress, scroll_container, table
from ..data import OPEN_POSITIONS
from ..layout import render_screen


def render_risk_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Toplam Equity", "$12,842.54", "+2.6%"), metric_card("Kullanılan Margin", "$3,104.22", "%24.2"), metric_card("Açık Risk", "$428.70", "%3.34"), metric_card("Günlük Drawdown", "-%0.82", "limit %5"), metric_card("Risk Permission", "PASS", "paper-only"))) + '</div>'
    risk_rows = ((r[0], r[1], r[2], r[5], r[6], "%2", "PASS") for r in OPEN_POSITIONS)
    table_panel = panel("POZİSYON RİSK TABLOSU", scroll_container(table(("Sembol", "Yön", "Miktar", "PnL", "PnL %", "Stop", "İzin"), risk_rows, "dense"), "Pozisyon risk tablosu"), "fill")
    timeline = panel("RİSK ZAMAN ÇİZGİSİ", line_chart(((18, 22, 21, 29, 25, 34, 31, 38, 35), (42, 40, 39, 36, 34, 31, 29, 27, 24)), ("#e5bd54", "#cf5c5c"), ("Risk %", "DD limiti")), "event-panel")
    limits = panel("RİSK LİMİTLERİ", progress("Max coin", 90, "yellow", "9 / 10") + progress("Margin", 24, "green") + progress("Daily loss", 16, "green", "%0.82 / %5") + progress("Allocation", 64, "blue"), "fill")
    controls = panel("RİSK KONTROLLERİ", kv_list((("Same-symbol lock", "PASS"), ("No hedge", "PASS"), ("No auto reversal", "PASS"), ("Stop Loss", "ON"), ("Live order", "LOCKED"))), "fill")
    actions = panel("ACİL KONTROLLER", action_stack((("YENİ GİRİŞLERİ DURDUR", "warning"), ("SAFE MODE", "info"), ("PANIC · ÇİFT ONAY", "danger"))), "compact")
    lower = '<div class="screen-grid grid-3 lower-row">' + panel("GÜNLÜK RİSK", bar_chart((12, 19, 14, 27, 18, 22, 16), labels=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")), "compact") + panel("KORELASYON", table(("Grup", "Değer", "Durum"), (("BTC / ETH", "0.82", "UYARI"), ("SOL / AVAX", "0.66", "PASS"), ("ALT sepet", "0.58", "PASS")), "dense"), "compact") + panel("RİSK OLAYLARI", table(("Saat", "Olay", "Durum"), (("19:42", "Permission check", "PASS"), ("19:41", "Coin limit", "9 / 10"), ("19:40", "Live-lock", "PASS")), "dense"), "compact") + '</div>'
    body = metrics + f'<div class="screen-grid with-rail fill"><div class="stack fill">{table_panel}{timeline}{lower}</div><aside class="stack fill">{limits}{controls}{actions}</aside></div>'
    return render_screen("RİSK", "Risk", body, "Risk permission, limit ve live-lock görünümü", "risk-screen")
