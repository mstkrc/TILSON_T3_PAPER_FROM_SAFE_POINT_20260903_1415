"""02_CANLI_TARAMA reference-aligned, display-only screen."""

from ..components import display_button, kv_list, panel, scroll_container, table
from ..data import OPEN_POSITIONS
from ..layout import render_screen


SCAN_ROWS = (
    (1, "BTCUSDT", "68,302.54", "2.38B", "PASS", "0.91", "DEĞİŞİM", "28.4", "12.6", "36.7", "UP", "LONG", "LONG_CANDIDATE", 1, "PASS", "LONG", "—", "VAR", "⌕"),
    (2, "ETHUSDT", "2,604.18", "1.42B", "PASS", "0.88", "DEĞİŞİM", "31.2", "15.8", "34.5", "UP", "LONG", "LONG_CANDIDATE", 2, "PASS", "LONG", "—", "VAR", "⌕"),
    (3, "SOLUSDT", "175.84", "842.67M", "PASS", "-0.73", "DEĞİŞİM", "14.3", "31.9", "33.1", "DOWN", "SHORT", "SHORT_CANDIDATE", 1, "PASS", "SHORT", "—", "VAR", "⌕"),
    (4, "BNBUSDT", "596.20", "389.21M", "PASS", "0.62", "DEĞİŞİM", "26.5", "13.1", "30.2", "UP", "LONG", "LONG_CANDIDATE", 3, "PASS", "LONG", "—", "VAR", "⌕"),
    (5, "ADAUSDT", "0.4915", "182.54M", "PASS", "-0.45", "DEĞİŞİM", "16.8", "24.6", "23.4", "DOWN", "SHORT", "SHORT_CANDIDATE", 2, "PASS", "SHORT", "—", "VAR", "⌕"),
    (6, "XRPUSDT", "0.5265", "256.11M", "PASS", "0.41", "DEĞİŞİM", "20.2", "14.9", "26.1", "UP", "LONG", "LONG_CANDIDATE", 4, "PASS", "LONG", "—", "VAR", "⌕"),
    (7, "DOGEUSDT", "0.12793", "98.42M", "FAIL", "0.55", "DEĞİŞİM", "18.1", "12.7", "21.3", "FLAT", "—", "NO_SIGNAL", "—", "—", "BLOCKED", "Hacim filtresi", "HAYIR", "⌕"),
    (8, "AVAXUSDT", "37.21", "127.63M", "PASS", "0.33", "DEVAM", "19.5", "14.6", "24.8", "UP", "LONG", "NO_SIGNAL", "—", "—", "BLOCKED", "ADX düşük", "VAR", "⌕"),
    (9, "LINKUSDT", "14.80", "74.18M", "PASS", "-0.28", "DEVAM", "13.7", "18.6", "19.4", "DOWN", "—", "NO_SIGNAL", "—", "—", "BLOCKED", "ADX düşük", "VAR", "⌕"),
    (10, "DOTUSDT", "6.24", "53.21M", "PASS", "-0.62", "DEĞİŞİM", "11.2", "22.9", "22.1", "DOWN", "SHORT", "NO_SIGNAL", "—", "—", "BLOCKED", "T3 kırmızı", "HAYIR", "⌕"),
    (11, "LTCUSDT", "88.21", "49.35M", "PASS", "0.12", "DEVAM", "17.1", "15.3", "17.8", "FLAT", "—", "NO_SIGNAL", "—", "—", "BLOCKED", "No signal", "HAYIR", "⌕"),
    (12, "MATICUSDT", "0.4721", "61.77M", "PASS", "0.18", "DEVAM", "16.5", "13.8", "18.2", "UP", "—", "NO_SIGNAL", "—", "—", "BLOCKED", "No signal", "VAR", "⌕"),
)


EVENT_ROWS = (
    ("19:42:16", "Aday bulundu", "SOLUSDT", "SHORT_CANDIDATE", 1, "PASS", "SHORT", "T3 aşağı kırıldı, -DI > +DI, ADX 33.1, hacim PASS"),
    ("19:42:08", "Risk PASS", "BTCUSDT", "LONG_CANDIDATE", 1, "PASS", "LONG", "Risk kontrolleri PASS, işleme izin verildi"),
    ("19:41:59", "Aday bulundu", "ETHUSDT", "LONG_CANDIDATE", 2, "PASS", "LONG", "+DI > -DI, ADX 34.5 ile trend güçlü"),
    ("19:41:52", "Aday bulundu", "ADAUSDT", "SHORT_CANDIDATE", 2, "PASS", "SHORT", "T3 aşağı, -DI baskın, hacim PASS"),
    ("19:41:41", "Hacim filtresi elendi", "DOGEUSDT", "NO_SIGNAL", "—", "—", "BLOCKED", "24s hacim 5M altı"),
    ("19:41:29", "ADX düşük elendi", "LINKUSDT", "NO_SIGNAL", "—", "—", "BLOCKED", "ADX 19.4 < 20"),
    ("19:41:18", "Risk PASS", "XRPUSDT", "LONG_CANDIDATE", 4, "PASS", "LONG", "Risk kontrolleri PASS"),
    ("19:41:07", "T3 kırmızı elendi", "DOTUSDT", "NO_SIGNAL", "—", "—", "BLOCKED", "T3 -0.62, kırmızı bölgede"),
    ("19:40:55", "No signal", "LTCUSDT", "NO_SIGNAL", "—", "—", "BLOCKED", "Trend yok, ADX 17.8 < 20"),
    ("19:40:42", "Closed candle OK", "SOLUSDT", "SHORT_CANDIDATE", 1, "PASS", "SHORT", "1H candle kapandı, sinyal onaylandı"),
)


def _strategy_controls() -> str:
    return '<div class="group1-control-grid">' + ''.join((
        display_button("DEĞİŞİM", "info", True), display_button("DEVAM", "neutral"), display_button("T3 MODE", "neutral"),
        display_button("ON", "info", True), display_button("OFF", "neutral"), display_button("N = 6", "warning"),
        display_button("ON", "info", True), display_button("OFF", "neutral"), display_button("VOLUME", "neutral"),
        display_button("ON", "success", True), display_button("OFF", "neutral"), display_button("%2", "warning"),
    )) + '</div>'


def render_live_scan_screen(model=None) -> str:
    top = '<div class="screen-grid grid-5 group1-top">' + ''.join((
        panel("CANLI TARAMA ÖZETİ", kv_list((("Tarama Durumu", "ÇALIŞIYOR"), ("Son Tarama", "19:42:16"), ("Tarama Süresi", "0.32s"), ("Taranan Sembol", "312"), ("Elenen Sembol", "218"), ("Filtrelenen Sembol", "294"), ("Sonuç Üreten Strateji", "3 / 5"), ("Son Eşleşme", "SOL/USDT (SHORT)"))), "compact"),
        panel("STRATEJİ KONTROL ÖZETİ", kv_list((("T3 Factor", "0.7"), ("T3 Period", "4"), ("DMI Length", "24"), ("ADX Smoothing", "24"), ("ADX Threshold", "30"), ("ADX Slope", "ON (N=6)"), ("Volume Filter", "ON"), ("Stop Loss", "ON (%2)"))), "compact"),
        panel("FİLTRE / EVREN ÖZETİ", kv_list((("Borsa", "Binance USDT-M Futures"), ("Active Symbols", "312"), ("Inactive/Delisted Hariç", "Evet"), ("24h Volume Filtresi", ">= 5M USDT"), ("Açık Pozisyon İstisnası", "Hariç"), ("Closed Candle", "1H"), ("Veri Kaynağı", "Binance API"), ("Son Güncelleme", "19:42:16"))), "compact"),
        panel("RAPOR ÖZETİ", kv_list((("Toplam İşlem", "1,324"), ("Giriş İşlem", "69"), ("Kârlı İşlem", "642 (48.49%)"), ("Zararlı İşlem", "508 (38.47%)"), ("Ortalama PnL / İşlem", "+2.12 USDT"), ("Son 24s Aday", "76"), ("Blocked Oranı", "59.42%"))), "compact"),
        panel("AÇIK POZİSYONLAR (9)", scroll_container(table(("Sembol", "Yön", "Miktar", "Giriş", "Mevcut", "PnL", "PnL %", ""), OPEN_POSITIONS, "dense", action_last=True), "Açık pozisyon istisnaları"), "compact"),
    )) + '</div>'
    scan_table = panel("MARKET / ADAY TARAMA TABLOSU", scroll_container(table(("#", "Sembol", "Fiyat", "24s Hacim", "Hacim", "T3", "Giriş Modu", "+DI", "-DI", "ADX", "ADX Slope", "Direction", "Sinyal", "Rank", "Risk", "Final", "Block Reason", "Açık Poz.", ""), SCAN_ROWS, "dense wide-table"), "Market aday tarama tablosu") + '<div class="status-key"><b class="is-positive">PASS</b> ≥ 5M USDT <b class="is-negative">FAIL</b> &lt; 5M USDT <b class="is-positive">RISK PASS</b> İşleme izin var <b class="is-negative">BLOCKED</b> Yasak</div>', "group1-table-panel", "12 / 312 SYMBOL")
    events = panel("CANLI TARAMA OLAY AKIŞI / BLOCK REASON", scroll_container(table(("Zaman", "Tür", "Sembol", "Sinyal", "Rank", "Risk", "Final", "Neden / Açıklama"), EVENT_ROWS, "dense wide-table"), "Canlı tarama olay ve block reason akışı"), "group1-events", "SON 3 GÜN")
    detail_content = kv_list((("Sembol", "SOLUSDT"), ("Fiyat", "175.84 USDT"), ("Signal Result", "SHORT_CANDIDATE"), ("Final Decision", "SHORT"), ("Block Reason", "—"), ("Ranking", "1"), ("Risk Permission", "PASS"), ("Volume State", "PASS (842.67M USDT)"), ("Candle State", "Closed Candle OK (1H)"))) + '<div class="detail-note"><b>Açıklama</b><br>T3 kırmızı bölgede ve -DI &gt; +DI. ADX 33.1 ile trend gücü yeterli. Hacim filtresi PASS; risk kontrolleri uygun olduğu için SHORT aday olarak işaretlendi.</div>'
    detail = panel("SEÇİLİ COİN / KARAR DETAYI", scroll_container(detail_content, "Seçili coin karar detayı"), "group1-right-detail")
    strategy_content = kv_list((("T3 Factor", "0.7"), ("T3 Period", "4"), ("T3 Entry Mode", "DEĞİŞİM / DEVAM"), ("DMI Length", "24"), ("ADX Smoothing", "24"), ("ADX Threshold", "30"), ("ADX Slope", "ON / OFF / N=6"), ("Volume Filter", "ON / OFF"), ("Max Coin", "5"), ("Coin Başı Allocation", "200 USDT"), ("Leverage", "1x"), ("Stop Loss", "ON / OFF / %2"), ("Closed Candle", "1H"), ("UI Refresh", "2 dk"))) + _strategy_controls()
    strategy = panel("STRATEJİ ÖZETİ", scroll_container(strategy_content, "Canlı tarama strateji özeti"), "group1-right-secondary")
    body = top + f'<div class="screen-grid with-rail group1-main"><div class="stack">{scan_table}{events}</div><aside class="stack">{detail}{strategy}</aside></div>'
    return render_screen("CANLI TARAMA", "Canlı Tarama", body, "", "group1-screen live-scan-screen")
