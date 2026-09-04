"""04_ACIK_POZISYONLAR reference-aligned, display-only screen."""

from ..components import display_button, donut, kv_list, panel, progress, scroll_container, table
from ..layout import render_screen


POSITION_ROWS = (
    (1, "BTC/USDT", "LONG", "68,302.54", "0.0321", "2,195.68", "68,754.21", "2,209.84", "+14.16", "+0.65%", "66,936.49", "70,390.62", "1H 42m", "T3: DEVAM · ADX ON", "KAPAT"),
    (2, "ETH/USDT", "LONG", "2,604.18", "0.2100", "546.88", "2,650.32", "556.56", "+9.68", "+1.77%", "2,552.10", "2,761.35", "49m", "T3: DEĞİŞİM · SL %2", "KAPAT"),
    (3, "SOL/USDT", "SHORT", "178.45", "4.2500", "758.41", "176.32", "748.86", "+9.55", "+1.26%", "182.02", "167.30", "1H 18m", "T3: DEVAM · CC 1H", "KAPAT"),
    (4, "XRP/USDT", "LONG", "0.5265", "1,400.0", "737.10", "0.5243", "734.02", "-3.08", "-0.42%", "0.5160", "0.5370", "37m", "T3: DEĞİŞİM · Slope OFF", "KAPAT"),
    (5, "BNB/USDT", "LONG", "596.20", "0.8400", "500.81", "590.12", "495.70", "-5.11", "-1.02%", "584.27", "614.09", "56m", "T3: DEVAM · ADX ON", "KAPAT"),
    (6, "MATIC/USDT", "SHORT", "0.4915", "2,000.0", "983.00", "0.4961", "973.34", "+9.66", "+0.98%", "0.5013", "0.4768", "28m", "T3: DEĞİŞİM · SL %2", "KAPAT"),
)


ACTIVITY_ROWS = (
    ("19:41:58", "BTC/USDT", "PnL GÜNCELLEME", "Güncel PnL: +14.16 USDT (+0.65%)"),
    ("19:41:47", "ETH/USDT", "PnL GÜNCELLEME", "Güncel PnL: +9.68 USDT (+1.77%)"),
    ("19:41:33", "SOL/USDT", "PnL GÜNCELLEME", "Güncel PnL: +9.55 USDT (+1.26%)"),
    ("19:41:21", "XRP/USDT", "PnL GÜNCELLEME", "Güncel PnL: -3.08 USDT (-0.42%)"),
    ("19:41:09", "BNB/USDT", "PnL GÜNCELLEME", "Güncel PnL: -5.11 USDT (-1.02%)"),
    ("19:40:55", "MATIC/USDT", "PnL GÜNCELLEME", "Güncel PnL: +9.66 USDT (+0.98%)"),
    ("19:40:34", "BTC/USDT", "POZİSYON AÇILDI", "T3 DEVAM, ADX 35.7, +DI > -DI"),
    ("19:39:52", "SOL/USDT", "STOP KONTROL", "Stop loss ON (%2), state PASS"),
)


def _quick_actions() -> str:
    return '<div class="group1-actions-grid">' + ''.join((
        display_button("TÜM POZİSYONLARI KAPAT", "success"),
        display_button("ZARARDAKİLERİ KAPAT", "danger"),
        display_button("KÂRDAKİLERİ KORU", "warning"),
        display_button("YENİ GİRİŞLERİ DURDUR", "info"),
    )) + '</div><div class="group1-note">Bu kontroller PAPER modda yalnız UIIntent olarak gösterilir. Gerçek emir gönderimi yapılmaz.</div>'


def render_positions_screen(model=None) -> str:
    top = '<div class="screen-grid grid-5 group1-top">' + ''.join((
        panel("AÇIK POZİSYON ÖZETİ", kv_list((("Toplam Açık Pozisyon", "6"), ("Toplam Yatırım (USDT)", "1,207.45"), ("Toplam Güncel Değer", "1,268.32"), ("Toplam PnL (USDT)", "+60.87"), ("Toplam PnL (%)", "+5.04%"), ("Ortalama PnL (%)", "+0.84%"), ("Kârda Pozisyon", "4 (66.7%)"), ("Zararda Pozisyon", "2 (33.3%)"))), "compact"),
        panel("POZİSYON DAĞILIMI (YÖN)", donut((("LONG", 4, "#2daf51"), ("SHORT", 2, "#e83a32")), "6"), "compact"),
        panel("POZİSYON DAĞILIMI (COİN)", donut((("BTC/USDT", 2, "#e4a414"), ("ETH/USDT", 1, "#0b87ce"), ("SOL/USDT", 1, "#7d1bad"), ("XRP/USDT", 1, "#00a6ba"), ("BNB/USDT", 1, "#d8a426")), "6"), "compact"),
        panel("RİSK KONTROL", kv_list((("Portföy Risk Kullanımı", "24.15%"), ("Max Coin Limiti", "6 / 50"), ("Coin Başı Max Allocation", "200 USDT"), ("Kullanılan Allocation", "201.24 USDT"), ("Kullanılabilir Bakiye", "8,642.10 USDT"), ("Stop Loss", "ON (%2)"), ("Closed Candle", "1H"))), "compact"),
        panel("HIZLI İŞLEMLER", _quick_actions(), "compact"),
    )) + '</div>'
    positions = panel("AÇIK POZİSYONLAR", scroll_container(table(("#", "Sembol", "Yön", "Giriş Fiyatı", "Miktar", "Yatırım", "Güncel Fiyat", "Güncel Değer", "PnL", "PnL %", "Stop Loss", "Kâr Hedefi", "Süre", "Strateji Snapshot", "İşlem"), POSITION_ROWS, "dense wide-table", action_last=True), "Açık pozisyonlar detay tablosu") + '<div class="group1-note">Açık pozisyonlar tarama filtrelerinden etkilenmez. Strateji değişikliği yalnızca yeni giriş adaylarını etkiler. <span style="float:right">Son Güncelleme: 19:42:16</span></div>', "group1-table-panel", "FİLTRELERDEN ETKİLENMEZ")
    activity = panel("POZİSYON YÖNETİM ETKİNLİK AKIŞI", scroll_container(table(("Zaman", "Sembol", "Olay", "Detay"), ACTIVITY_ROWS, "dense"), "Pozisyon yönetim etkinlik akışı"), "fill", "SON 15")
    allocation = panel("RİSK & ALLOCATION", kv_list((("Kullanılabilir Bakiye (USDT)", "8,642.10"), ("Toplam Açık Pozisyon Değeri", "1,268.32"), ("Kullanılan Margin (USDT)", "1,207.45"), ("Kullanılan Margin Oranı", "24.15%"), ("Max Coin Limiti", "6 / 50"), ("Ortalama Coin Başı Yatırım", "201.24 USDT"), ("Max Coin Başı Allocation", "200 USDT"), ("Leverage", "1x"), ("Stop Loss", "ON (%2)"))) + progress("Margin Kullanımı", 24, "green", "24.15%"), "fill", "CANLI DISPLAY")
    detail = panel("SEÇİLİ POZİSYON DETAYI", scroll_container(kv_list((("Sembol", "BTC/USDT"), ("Yön", "LONG"), ("Giriş Zamanı", "19:40:34"), ("Giriş Fiyatı", "68,302.54"), ("Miktar", "0.0321"), ("Yatırım (USDT)", "2,195.68"), ("Güncel Fiyat", "68,754.21"), ("Güncel Değer (USDT)", "2,209.84"), ("PnL (USDT)", "+14.16"), ("PnL (%)", "+0.65%"), ("Stop Loss (%2)", "66,936.49"), ("Kâr Hedefi (Öneri)", "70,390.62"), ("Süre", "1H 42m"), ("Strateji Snapshot", "T3 DEVAM · ADX Slope ON (N=6) · SL ON (%2) · CC 1H"), ("Not", "—"))), "Seçili pozisyon detayı"), "group1-right-detail")
    rules_content = '<ul class="group1-checklist"><li>Açık pozisyonlar tarama filtrelerinden etkilenmez.</li><li>Strateji değişikliği mevcut pozisyonları etkilemez.</li><li>Sadece yeni giriş adaylarını etkiler.</li><li>ENTRY / ADD / PROTECTION / EXIT kurallarına göre yürütülür.</li><li>Tüm işlemler PAPER modda simüle edilir.</li><li>Gerçek emir gönderimi yapılmaz.</li></ul>'
    rules = panel("POZİSYON KURALLARI", scroll_container(rules_content, "Pozisyon kuralları checklist"), "group1-right-secondary")
    lower = f'<div class="screen-grid grid-2 group1-position-lower">{activity}{allocation}</div>'
    body = top + f'<div class="screen-grid with-rail group1-main"><div class="stack">{positions}{lower}</div><aside class="stack">{detail}{rules}</aside></div>'
    return render_screen("AÇIK POZİSYONLAR", "Açık Pozisyonlar", body, "", "group1-screen positions-screen")
