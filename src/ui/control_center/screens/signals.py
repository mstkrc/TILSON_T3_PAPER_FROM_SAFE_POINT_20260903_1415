"""03_SINYALLER reference-aligned, display-only screen."""

from ..components import display_button, donut, kv_list, panel, scroll_container, table
from ..layout import render_screen


SIGNAL_TABLE_ROWS = (
    (1, "19:42:16", "BTC/USDT", "68,302.54", "2.23B", "YEŞİL", "DEVAM", "36.7", "12.6", "35.7 / UP", "LONG", "STRONG", 1, "PASS", "1H", "⌾"),
    (2, "19:42:11", "ETH/USDT", "2,604.18", "2.42B", "YEŞİL", "DEĞİŞİM", "31.2", "15.6", "34.6 / UP", "LONG", "LONG", 2, "PASS", "1H", "⌾"),
    (3, "19:42:09", "SOL/USDT", "175.84", "812.5M", "YEŞİL", "DEVAM", "34.8", "13.9", "33.1 / UP", "LONG", "LONG", 3, "PASS", "1H", "⌾"),
    (4, "19:42:08", "BNB/USDT", "596.20", "391.2M", "KIRMIZI", "DEĞİŞİM", "16.3", "31.8", "23.9 / DOWN", "SHORT", "SHORT", 4, "PASS", "1H", "⌾"),
    (5, "19:42:06", "ADA/USDT", "0.4915", "312.9M", "YEŞİL", "DEVAM", "29.1", "14.2", "24.6 / UP", "LONG", "LONG", 5, "PASS", "1H", "⌾"),
    (6, "19:42:05", "XRP/USDT", "0.5265", "256.1M", "KIRMIZI", "DEĞİŞİM", "10.2", "28.4", "22.8 / DOWN", "SHORT", "SHORT", 6, "PASS", "1H", "⌾"),
    (7, "19:42:03", "MATIC/USDT", "0.4721", "218.9M", "YEŞİL", "DEVAM", "31.6", "12.8", "28.1 / UP", "LONG", "LONG", 7, "PASS", "1H", "⌾"),
    (8, "19:41:59", "AVAX/USDT", "37.21", "147.6M", "GRİ", "NÖTR", "18.2", "17.9", "19.1 / FLAT", "—", "NO SIGNAL", "—", "—", "1H", "⌾"),
    (9, "19:41:58", "LINK/USDT", "14.80", "74.1M", "GRİ", "NÖTR", "15.1", "15.6", "16.2 / FLAT", "—", "NO SIGNAL", "—", "—", "1H", "⌾"),
    (10, "19:41:56", "DOT/USDT", "6.24", "63.2M", "KIRMIZI", "DEĞİŞİM", "9.8", "24.6", "20.4 / DOWN", "SHORT", "BLOCKED", "—", "BLOCKED", "1H", "⌾"),
)


SIGNAL_EVENTS = (
    ("19:42:16", "BTC/USDT", "YENİ SİNYAL", "DEVAM", "LONG", "STRONG", 1, "PASS", "T3 yeşil devam, +DI > -DI, ADX 35.7, slope UP"),
    ("19:42:11", "ETH/USDT", "YENİ SİNYAL", "DEĞİŞİM", "LONG", "STRONG", 2, "PASS", "T3 kırmızıdan yeşile değişim, +DI > -DI"),
    ("19:42:08", "BNB/USDT", "YENİ SİNYAL", "DEĞİŞİM", "SHORT", "CANDIDATE", 4, "PASS", "T3 yeşilden kırmızıya değişim, -DI > +DI"),
    ("19:42:05", "XRP/USDT", "YENİ SİNYAL", "DEĞİŞİM", "SHORT", "CANDIDATE", 6, "PASS", "T3 değişim, ADX 22.8, risk PASS"),
    ("19:41:56", "DOT/USDT", "BLOCKED", "DEĞİŞİM", "SHORT", "BLOCKED", "—", "BLOCKED", "24H hacim 63.2M < filtre kuralına takıldı"),
    ("19:41:53", "LTC/USDT", "NO SIGNAL", "NÖTR", "—", "NO SIGNAL", "—", "—", "ADX 15.8 < 20, sinyal üretilmedi"),
    ("19:41:49", "AVAX/USDT", "NO SIGNAL", "NÖTR", "—", "NO SIGNAL", "—", "—", "DMI yönü ve slope nötr"),
    ("19:41:45", "SOL/USDT", "VALIDITY", "DEVAM", "LONG", "STRONG", 3, "PASS", "Closed candle 1H geçerliliği korundu"),
)


def _strategy_controls() -> str:
    return '<div class="group1-control-grid">' + ''.join((
        display_button("DEĞİŞİM", "info", True), display_button("DEVAM", "neutral"), display_button("ENTRY", "neutral"),
        display_button("ON", "info", True), display_button("OFF", "neutral"), display_button("N=6", "warning"),
        display_button("ON", "success", True), display_button("OFF", "neutral"), display_button(">5M", "warning"),
    )) + '</div>'


def render_signals_screen(model=None) -> str:
    top = '<div class="screen-grid grid-5 group1-top">' + ''.join((
        panel("SİNYAL ÖZETİ", kv_list((("Toplam Sinyal", "156"), ("LONG Sinyal", "62 (39.7%)"), ("SHORT Sinyal", "48 (30.8%)"), ("NO SIGNAL", "26 (16.7%)"), ("BLOCKED", "20 (12.8%)"), ("En Son Sinyal", "19:42:16"), ("Sinyal Yoğunluğu", "Orta"), ("Geçerlilik", "1H Kapandı"))), "compact"),
        panel("YÖN DAĞILIMI", donut((("LONG", 62, "#35b95d"), ("SHORT", 48, "#f0332d"), ("NO SIGNAL", 26, "#aaa49a"), ("BLOCKED", 20, "#f05236")), "156"), "compact"),
        panel("T3 ENTRY MODE DAĞILIMI", donut((("DEĞİŞİM", 74, "#078ed0"), ("DEVAM", 60, "#e9a900"), ("NÖTR", 22, "#aaa49a")), "156"), "compact"),
        panel("SİNYAL FİLTRE ÖZETİ", kv_list((("ADX Slope", "ON (N=6)"), ("Volume Filter", "ON"), ("Min 24H Hacim", "> 5M USDT"), ("Data Quality", "PASS"), ("Inactive / Delisted", "Hariç"), ("Open Position İstisna", "Aktif"), ("Closed Candle", "1H"), ("UI Refresh", "2 dk"))), "compact"),
        panel("RAPOR ÖZETİ (BUGÜN)", kv_list((("Sinyal Oluşan", "1,324"), ("LONG", "542 (40.9%)"), ("SHORT", "508 (38.4%)"), ("NO SIGNAL", "274 (20.7%)"), ("BLOCKED", "132 (10.0%)"), ("İşleme Dönüşen", "69"), ("Ortalama Sinyal → İşlem", "2.12"), ("Ortalama İşlem Süresi", "2h 14m"))), "compact"),
    )) + '</div>'
    filters = '<div class="group1-filter-row">' + ''.join((display_button("TÜMÜ", "info", True), display_button("LONG", "success"), display_button("SHORT", "danger"), display_button("NO SIGNAL", "neutral"), display_button("BLOCKED", "danger"))) + '</div>'
    signals = panel("SİNYAL TABLOSU (CANLI)", filters + scroll_container(table(("#", "Zaman", "Sembol", "Fiyat", "24H Hacim", "T3 Renk", "T3 Mode", "+DI", "-DI", "ADX Slope", "Yön", "Sinyal", "Rank", "Risk", "Geçerlilik", "Detay"), SIGNAL_TABLE_ROWS, "dense wide-table"), "Canlı sinyal tablosu"), "group1-table-panel", "SON 10")
    events = panel("SİNYAL OLAY AKIŞI", scroll_container(table(("Zaman", "Sembol", "Olay", "T3 Mode", "Yön", "Sinyal", "Rank", "Risk", "Açıklama"), SIGNAL_EVENTS, "dense wide-table"), "Sinyal olay akışı"), "group1-events", "SON 15")
    detail = panel("SEÇİLİ SİNYAL DETAYI", scroll_container(kv_list((("Sembol", "BTC/USDT · LONG"), ("Zaman", "19:42:16"), ("Fiyat (USDT)", "68,302.54"), ("24H Hacim", "2.23B"), ("T3 Renk", "YEŞİL"), ("T3 Entry Mode", "DEVAM"), ("+DI / -DI", "36.7 / 12.6"), ("ADX", "35.7"), ("ADX Slope (N=6)", "UP"), ("Sinyal", "STRONG"), ("Rank", "1"), ("Risk", "PASS"), ("Geçerlilik", "1H Kapandı"), ("Strateji", "EMA Model Trade v1.6"), ("Block Reason", "—"), ("Not", "—"))), "Seçili sinyal detayı"), "group1-right-detail")
    strategy_content = kv_list((("T3 Entry Mode", "DEĞİŞİM / DEVAM"), ("ADX Slope", "ON (N=6)"), ("Volume Filter", "ON (>5M USDT)"), ("Stop Loss", "ON (%2)"), ("Closed Candle", "1H"), ("UI Refresh", "2 dk"))) + _strategy_controls() + '<div class="detail-note">Strateji değişikliği mevcut açık pozisyonları etkilemez. Sadece sonraki kapanmış 1H mumdan itibaren yeni entry adaylarını etkiler.</div>'
    strategy = panel("STRATEJİ ÖZETİ", scroll_container(strategy_content, "Sinyal strateji özeti"), "group1-right-secondary")
    body = top + f'<div class="screen-grid with-rail group1-main"><div class="stack">{signals}{events}</div><aside class="stack">{detail}{strategy}</aside></div>'
    return render_screen("SİNYALLER", "Sinyaller", body, "", "group1-screen signals-screen")
