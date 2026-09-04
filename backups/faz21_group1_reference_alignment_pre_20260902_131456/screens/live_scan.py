"""02_CANLI_TARAMA display-only screen."""

from ..components import kv_list, panel, scroll_container, table, toggle
from ..data import OPEN_POSITIONS, SIGNAL_ROWS
from ..layout import render_screen


def render_live_scan_screen(model=None) -> str:
    candidate_rows = [row[:11] + (row[12],) for row in SIGNAL_ROWS]
    top = '<div class="screen-grid grid-5 top-band">' + "".join((
        panel("TARAMA DURUMU", kv_list((("Durum", "AKTİF"), ("Son tarama", "19:42:16"), ("Evren", "156 USDT-M"), ("Closed candle", "1H / 18:00"))), "compact"),
        panel("STRATEJİ KONTROLÜ", kv_list((("Tilson T3", "DEĞİŞİM"), ("ADX slope", "ON / N=6"), ("Volume filter", "ON"), ("Sinyal modu", "CLOSED CANDLE"))), "compact"),
        panel("FİLTRE / EVREN", kv_list((("Min. hacim", "50M USDT"), ("Hariç", "Stable / Leveraged"), ("Aday", "10"), ("Bloklanan", "3"))), "compact"),
        panel("TARAMA RAPORU", kv_list((("PASS", "7"), ("BLOCKED", "3"), ("LONG", "5"), ("SHORT", "2"))), "compact"),
        panel("AÇIK POZİSYONLAR", scroll_container(table(("Sembol", "Yön", "PnL %"), ((r[0], r[1], r[6]) for r in OPEN_POSITIONS), "dense"), "Açık pozisyon özeti"), "compact"),
    )) + '</div>'
    market = panel("MARKET / CANDIDATES", scroll_container(table(("Saat", "Sembol", "Fiyat", "Hacim", "T3", "Mode", "+DI", "-DI", "ADX", "Slope", "Sinyal", "İzin"), candidate_rows, "dense wide-table"), "Canlı tarama aday tablosu"), "fill", "CLOSED CANDLE · DISPLAY ONLY")
    events = panel("TARAMA OLAY AKIŞI", scroll_container(table(("Saat", "Olay", "Sembol", "Sonuç"), (("19:42:16", "Closed candle tarandı", "BTC/USDT", "PASS"), ("19:42:11", "Aday sıralandı", "ETH/USDT", "RANK 2"), ("19:42:08", "Risk izni", "BNB/USDT", "PASS"), ("19:41:56", "Block reason", "DOT/USDT", "ADX THRESHOLD")), "dense"), "Tarama olay akışı"), "event-panel")
    detail = panel("SEÇİLİ COİN ÖZETİ", kv_list((("Sembol", "BTC/USDT"), ("Fiyat", "68,302.54"), ("T3", "YEŞİL / DEVAM"), ("DMI", "+DI 36.7 / -DI 12.6"), ("ADX", "35.7 / UP"), ("Final signal", "LONG"), ("Rank", "1"), ("Risk permission", "PASS"))), "fill")
    strategy = panel("STRATEJİ / FİLTRE", kv_list((("T3 Entry Mode", "DEĞİŞİM"), ("ADX Threshold", "20"), ("ADX Slope", "ON / N=6"), ("Volume", "ON"), ("Stop Loss", "ON / %2"), ("Execution", "PAPER ONLY"))) + '<div class="toggle-row">' + toggle("Canlı emir", False) + toggle("Auto apply", False) + '</div>', "fill")
    body = top + f'<div class="screen-grid with-rail fill"><div class="stack fill">{market}{events}</div><aside class="stack fill">{detail}{strategy}</aside></div>'
    return render_screen("CANLI TARAMA", "Canlı Tarama", body, "Closed-candle candidate pipeline · gerçek emir üretmez", "live-scan-screen")
