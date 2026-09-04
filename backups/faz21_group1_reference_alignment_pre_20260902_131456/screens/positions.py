"""04_ACIK_POZISYONLAR display-only ledger view."""

from ..components import action_stack, donut, kv_list, metric_card, panel, progress, scroll_container, table
from ..data import OPEN_POSITIONS
from ..layout import render_screen


def render_positions_screen(model=None) -> str:
    top = '<div class="screen-grid grid-5 top-band">' + "".join((
        panel("POZİSYON ÖZETİ", '<div class="metric-grid grid-3">' + metric_card("Açık", "9") + metric_card("LONG", "6") + metric_card("SHORT", "3") + '</div>', "compact"),
        panel("YÖN DAĞILIMI", donut((("LONG", 6, "#2fc878"), ("SHORT", 3, "#e35c5c")), "9"), "compact"),
        panel("COİN DAĞILIMI", donut((("BTC", 28, "#e8c85e"), ("ETH", 22, "#7699ef"), ("Diğer", 50, "#4fa9a2")), "$8.2K"), "compact"),
        panel("RİSK DURUMU", kv_list((("Kullanım", "%64"), ("Max coin", "10"), ("Kalan hak", "1"), ("Permission", "PASS"))), "compact"),
        panel("HIZLI AKSİYONLAR", action_stack((("YENİ GİRİŞLERİ DURDUR", "warning"), ("PANIC · ONAY GEREKLİ", "danger"), ("LIVE KİLİTLİ", "locked"))), "compact"),
    )) + '</div>'
    positions = panel("AÇIK POZİSYONLAR", scroll_container(table(("Sembol", "Yön", "Miktar", "Giriş", "Mark", "PnL", "PnL %", "Aksiyon"), OPEN_POSITIONS, "dense", action_last=True), "Açık pozisyonlar"), "fill", "LEDGER / POSITION STATE")
    detail = panel("SEÇİLİ POZİSYON", kv_list((("Sembol", "BTC/USDT"), ("State", "POSITION"), ("Yön", "LONG"), ("Giriş", "68,200.00"), ("Mark", "68,302.54"), ("Net PnL", "+102.54"), ("Commission", "-1.40"), ("Funding", "+0.22"), ("Stop Loss", "ON / %2"), ("Config snapshot", "LEDGER-REF-1042"), ("Close action", "UIIntent / disabled"))), "fill")
    activity = panel("POZİSYON AKTİVİTESİ", scroll_container(table(("Saat", "Sembol", "Olay", "Durum"), (("19:42:16", "BTC/USDT", "Mark price update", "PASS"), ("19:41:58", "ETH/USDT", "PnL recalculated", "PASS"), ("19:41:32", "SOL/USDT", "Stop state checked", "PASS"), ("19:40:44", "ADA/USDT", "Funding snapshot", "PASS")), "dense"), "Pozisyon aktivitesi"), "event-panel")
    allocation = panel("RİSK / ALLOCATION", progress("Margin kullanımı", 64, "blue") + progress("Coin limiti", 90, "yellow", "9 / 10") + progress("Günlük risk", 38, "green") + kv_list((("Same-symbol lock", "PASS"), ("No hedge", "PASS"), ("Auto reversal", "OFF"))), "event-panel")
    rules = panel("POZİSYON KURALLARI", kv_list((("Ledger authority", "TEK KAYNAK"), ("Manual close", "DISPLAY ONLY"), ("New order", "YOK"), ("Live endpoint", "YOK"), ("Mode", "PAPER / LOCKED"))), "fill")
    body = top + f'<div class="screen-grid with-rail fill"><div class="stack fill">{positions}<div class="screen-grid grid-2 lower-row">{activity}{allocation}</div></div><aside class="stack fill">{detail}{rules}</aside></div>'
    return render_screen("AÇIK POZİSYONLAR", "Açık Pozisyonlar", body, "Ledger kaynaklı, execution bağlantısı olmayan pozisyon görünümü", "positions-screen")
