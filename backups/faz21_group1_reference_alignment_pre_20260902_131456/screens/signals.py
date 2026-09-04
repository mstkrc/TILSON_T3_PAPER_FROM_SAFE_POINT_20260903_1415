"""03_SINYALLER display-only screen."""

from ..components import donut, kv_list, metric_card, panel, scroll_container, table
from ..data import SIGNAL_ROWS
from ..layout import render_screen


def render_signals_screen(model=None) -> str:
    summary = '<div class="screen-grid grid-4 top-band">' + "".join((
        panel("SİNYAL ÖZETİ", '<div class="metric-grid grid-3">' + metric_card("Toplam", "10", "son tarama") + metric_card("PASS", "7", "izinli") + metric_card("BLOCKED", "3", "engelli") + '</div>', "compact"),
        panel("YÖN DAĞILIMI", donut((("LONG", 5, "#28c76f"), ("SHORT", 2, "#ea5455"), ("NÖTR", 3, "#75839a")), "10"), "compact"),
        panel("SONUÇ DAĞILIMI", donut((("PASS", 7, "#3ebd78"), ("BLOCK", 3, "#d85b5b")), "70%"), "compact"),
        panel("FİLTRE ÖZETİ", kv_list((("Closed candle", "1H"), ("ADX threshold", "20"), ("Slope", "ON / N=6"), ("Volume", "ON"))), "compact"),
    )) + '</div>'
    signal_table = panel("SİNYAL LİSTESİ", scroll_container(table(("Saat", "Sembol", "Fiyat", "Hacim", "T3", "Mode", "+DI", "-DI", "ADX", "Slope", "Final", "Rank", "İzin", "TF"), SIGNAL_ROWS, "dense wide-table"), "Sinyal listesi"), "fill", "AÇIKLANABİLİR KARAR ZİNCİRİ")
    detail = panel("SİNYAL DETAYI", kv_list((("Sembol", "BTC/USDT"), ("Karar zamanı", "19:42:16 UTC+3"), ("Candle", "CLOSED"), ("T3 color", "YEŞİL"), ("Entry mode", "DEVAM"), ("DMI", "+DI > -DI"), ("ADX", "35.7"), ("Slope", "UP"), ("Final decision", "LONG / PASS"), ("No-trade nedeni", "—"))), "fill")
    strategy = panel("STRATEJİ AÇIKLAMASI", kv_list((("Kural", "Tilson T3 Slope"), ("T3 Factor", "0.70"), ("T3 Period", "8"), ("ADX Smoothing", "14"), ("Risk permission", "PASS"), ("Execution", "DISPLAY ONLY"))), "fill")
    events = panel("SİNYAL OLAY AKIŞI", scroll_container(table(("Saat", "Adım", "Değer", "Sonuç"), (("19:42:16", "Closed candle", "BTC 1H", "PASS"), ("19:42:16", "Indicator", "T3 / DMI / ADX", "PASS"), ("19:42:16", "Candidate", "Rank 1", "PASS"), ("19:42:16", "Risk", "Permission", "PASS"), ("19:41:56", "No-trade", "ADX threshold", "BLOCKED")), "dense"), "Sinyal olay akışı"), "event-panel")
    body = summary + f'<div class="screen-grid with-rail fill"><div class="stack fill">{signal_table}{events}</div><aside class="stack fill">{detail}{strategy}</aside></div>'
    return render_screen("SİNYALLER", "Sinyaller", body, "Sinyal, no-trade ve karar gerekçeleri · display-only", "signals-screen")
