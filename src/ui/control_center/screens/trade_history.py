"""05_ISLEM_GECMISI reference-aligned, ledger display-only screen."""

from ..components import bar_chart, display_button, donut, field, kv_list, panel, scroll_container, table
from ..layout import render_screen


HISTORY_ROWS = (
    (1, "19.05.2026 18:56", "BTC/USDT", "LONG", "19.05 16:48", "19.05 18:56", "68,102.45", "68,302.54", "0.0321", "2,185.68", "+6.42", "+0.29%", "DEVAM", "YEŞİL", "UP", "2h 08m", "EMA Model v1.6", "KÂR", "⌾"),
    (2, "19.05.2026 17:41", "ETH/USDT", "LONG", "19.05 15:12", "19.05 17:41", "2,576.10", "2,604.18", "0.2100", "541.00", "+5.90", "+1.09%", "DEĞİŞİM", "YEŞİL", "UP", "2h 29m", "EMA Model v1.6", "KÂR", "⌾"),
    (3, "19.05.2026 16:33", "SOL/USDT", "SHORT", "19.05 14:21", "19.05 16:33", "178.45", "175.84", "4.2500", "758.41", "+11.07", "+1.46%", "DEVAM", "KIRMIZI", "DOWN", "2h 12m", "EMA Model v1.6", "KÂR", "⌾"),
    (4, "19.05.2026 15:22", "XRP/USDT", "LONG", "19.05 13:44", "19.05 15:22", "0.5256", "0.5265", "1,400.0", "735.84", "+1.26", "+0.17%", "DEVAM", "YEŞİL", "UP", "1h 38m", "EMA Model v1.6", "KÂR", "⌾"),
    (5, "19.05.2026 14:18", "BNB/USDT", "LONG", "19.05 12:02", "19.05 14:18", "596.20", "590.81", "0.8400", "500.81", "-4.52", "-0.90%", "DEĞİŞİM", "KIRMIZI", "DOWN", "2h 16m", "EMA Model v1.6", "ZARAR", "⌾"),
    (6, "19.05.2026 13:05", "MATIC/USDT", "SHORT", "19.05 11:27", "19.05 13:05", "0.4915", "0.4721", "2,000.0", "983.00", "+38.80", "+3.95%", "DEĞİŞİM", "KIRMIZI", "DOWN", "1h 38m", "EMA Model v1.6", "KÂR", "⌾"),
    (7, "19.05.2026 11:47", "AVAX/USDT", "LONG", "19.05 09:58", "19.05 11:47", "37.21", "37.21", "3.21", "147.64", "0.00", "0.00%", "DEĞİŞİM", "GRİ", "FLAT", "1h 49m", "EMA Model v1.6", "BE", "⌾"),
    (8, "19.05.2026 10:34", "LINK/USDT", "LONG", "19.05 08:12", "19.05 10:34", "14.80", "14.20", "74.19", "74.19", "-4.44", "-0.60%", "DEVAM", "KIRMIZI", "DOWN", "2h 22m", "EMA Model v1.6", "ZARAR", "⌾"),
    (9, "19.05.2026 09:21", "DOT/USDT", "LONG", "19.05 07:33", "19.05 09:21", "6.24", "6.42", "63.37", "63.37", "+1.79", "+2.90%", "DEVAM", "YEŞİL", "UP", "1h 48m", "EMA Model v1.6", "KÂR", "⌾"),
    (10, "19.05.2026 08:09", "LTC/USDT", "LONG", "19.05 05:44", "19.05 08:09", "88.21", "88.21", "49.35", "49.35", "0.00", "0.00%", "DEĞİŞİM", "GRİ", "FLAT", "2h 25m", "EMA Model v1.6", "BE", "⌾"),
)


BEST_ROWS = (
    (1, "ETH/USDT", "LONG", "+21.87", "+4.21%", "3h 12m", "18.05.2026"),
    (2, "SOL/USDT", "SHORT", "+18.32", "+2.48%", "2h 45m", "18.05.2026"),
    (3, "MATIC/USDT", "SHORT", "+12.63", "+2.15%", "1h 52m", "17.05.2026"),
    (4, "BTC/USDT", "LONG", "+11.24", "+0.51%", "4h 33m", "17.05.2026"),
    (5, "XRP/USDT", "LONG", "+8.32", "+1.12%", "1h 38m", "19.05.2026"),
)


WORST_ROWS = (
    (1, "BNB/USDT", "SHORT", "-8.64", "-1.61%", "2h 05m", "18.05.2026"),
    (2, "ADA/USDT", "SHORT", "-6.64", "-1.47%", "1h 27m", "17.05.2026"),
    (3, "ETH/USDT", "SHORT", "-5.23", "-1.06%", "1h 33m", "17.05.2026"),
    (4, "DOT/USDT", "SHORT", "-4.21", "-0.92%", "1h 42m", "19.05.2026"),
    (5, "AVAX/USDT", "SHORT", "-3.87", "-0.78%", "1h 18m", "16.05.2026"),
)


def _filters() -> str:
    controls = '<div class="field-grid">' + ''.join((
        field("Tarih Aralığı", "Son 3 Gün"), field("Başlangıç", "16.05.2026 00:00"),
        field("Bitiş", "19.05.2026 19:42"), field("Sembol", "Tümü"),
        field("Yön", "Tümü"), field("Sonuç", "Tümü"), field("Strateji", "Tümü"), field("T3 Mode", "Tümü"),
    )) + '</div>'
    buttons = '<div class="group1-actions-grid" style="margin-top:7px">' + display_button("FİLTRELE", "info") + display_button("SIFIRLA", "neutral") + '</div>'
    return controls + buttons


def render_trade_history_screen(model=None) -> str:
    top = '<div class="screen-grid grid-4 group1-history-top">' + ''.join((
        panel("FİLTRELER", _filters(), "compact"),
        panel("İŞLEM ÖZETİ", '<div class="group1-summary-split">' + kv_list((("Toplam İşlem", "124"), ("Kârlı İşlem", "78 (62.90%)"), ("Zararlı İşlem", "46 (37.10%)"), ("Toplam PnL (USDT)", "+142.56"), ("Toplam PnL (%)", "+1.42%"), ("Ort. PnL / İşlem", "+1.15 USDT"), ("Ortalama Kazanç", "+2.91 USDT"))) + kv_list((("Ortalama Zarar", "-1.58 USDT"), ("En Büyük Kazanç", "+21.87 USDT"), ("En Büyük Zarar", "-8.64 USDT"), ("Kazanç Faktörü", "1.84"), ("Ort. İşlem Süresi", "2h 07m"), ("Toplam Hacim", "68,754.21"), ("Komisyon / Finansman", "14.85 / -1.23"))) + '</div>', "compact"),
        panel("GÜNLÜK PNL", bar_chart((37, 52, 41, -12), labels=("16 May", "17 May", "18 May", "19 May")), "compact", "SEÇİLEN ARALIK"),
        panel("SONUÇ DAĞILIMI", donut((("KÂRLI", 78, "#32b458"), ("ZARARLI", 46, "#e63d34")), "124"), "compact"),
    )) + '</div>'
    history_table = table(("#", "Kapanış Zamanı", "Sembol", "Yön", "Giriş Zamanı", "Çıkış Zamanı", "Giriş Fiyatı", "Çıkış Fiyatı", "Miktar", "Yatırım", "PnL", "PnL %", "T3 Mode", "T3 Renk", "ADX Slope", "Süre", "Strateji", "Sonuç", "Detay"), HISTORY_ROWS, "dense wide-table")
    pagination = '<div class="group1-pagination"><b style="margin-right:auto">Toplam 124 kayıt (1–10 gösteriliyor)</b><span>‹</span><span class="active">1</span><span>2</span><span>3</span><span>…</span><span>13</span><span>›</span><span style="width:auto;padding:0 7px">10 / sayfa</span></div>'
    history = panel("İŞLEM GEÇMİŞİ TABLOSU", scroll_container(history_table, "Detaylı işlem geçmişi") + pagination, "group1-history-table")
    best = panel("EN İYİ İŞLEMLER", table(("#", "Sembol", "Yön", "PnL", "PnL %", "Süre", "Tarih"), BEST_ROWS, "dense"), "fill", "TOP 5")
    worst = panel("EN KÖTÜ İŞLEMLER", table(("#", "Sembol", "Yön", "PnL", "PnL %", "Süre", "Tarih"), WORST_ROWS, "dense"), "fill", "TOP 5")
    duration = panel("İŞLEM SÜRESİ DAĞILIMI", '<div class="screen-grid grid-2" style="height:100%">' + table(("Süre Aralığı", "İşlem Sayısı", "Yüzde"), (("0–1 Saat", 28, "22.58%"), ("1–3 Saat", 64, "51.61%"), ("3–6 Saat", 22, "17.74%"), ("6 Saat +", 10, "8.06%"), ("TOPLAM", 124, "100%")), "dense") + donut((("0–1", 28, "#e5a914"), ("1–3", 64, "#31ae56"), ("3–6", 22, "#067cb9"), ("6+", 10, "#df483a")), "124") + '</div>', "fill")
    detail_content = kv_list((("Sembol / Yön", "BTC/USDT · LONG"), ("Giriş Zamanı", "19.05.2026 16:48:12"), ("Çıkış Zamanı", "19.05.2026 18:56:33"), ("Giriş Fiyatı", "68,102.45"), ("Çıkış Fiyatı (USDT)", "68,302.54"), ("Miktar", "0.0321"), ("Yatırım (USDT)", "2,185.68"), ("PnL (USDT)", "+6.42"), ("PnL (%)", "+0.29%"), ("Komisyon (USDT)", "0.56"), ("Finansman (USDT)", "-0.02"), ("Net PnL (USDT)", "+5.86"), ("T3 Mode", "DEVAM"), ("T3 Renk", "YEŞİL"), ("ADX Slope (N=6)", "UP"), ("ADX Giriş / Çıkış", "35.7 / 37.2"), ("Süre", "2h 08m 21s"), ("Strateji", "EMA Model Trade v1.6"), ("Sonuç", "KÂRLI"), ("Not", "—"))) + donut((("Net Kâr", 59, "#32b15a"), ("Maliyet", 25, "#e6ad18"), ("Risk", 16, "#1783ba")), "+5.86")
    detail = panel("SEÇİLİ İŞLEM DETAYI", scroll_container(detail_content, "Seçili işlem detayı"), "fill")
    lower = f'<div class="screen-grid grid-3 group1-lower">{best}{worst}{duration}</div>'
    body = top + f'<div class="screen-grid with-rail group1-main"><div class="stack">{history}{lower}</div><aside class="stack">{detail}</aside></div>'
    return render_screen("İŞLEM GEÇMİŞİ", "İşlem Geçmişi", body, "", "group1-screen trade-history-screen")
