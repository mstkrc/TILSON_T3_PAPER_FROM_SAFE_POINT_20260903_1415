"""Display-only datasets and route metadata for the modular Control Center."""

from __future__ import annotations

from dataclasses import dataclass

REFERENCE_ROOT = "DOKUMANTASYON/CONTROL CENTER"
PAPER_ONLY = True
LIVE_LOCKED = True
LIVE_TRADING = False
LIVE_ORDER_SENDING_ALLOWED = False


@dataclass(frozen=True)
class ScreenDefinition:
    key: str
    title: str
    reference_file: str
    navigation_label: str
    output_file: str


SCREEN_DEFINITIONS = (
    ScreenDefinition("overview", "Genel Bakış", "01_GENEL_BAKIS.png", "Genel Bakış", "../faz21_control_center.html"),
    ScreenDefinition("live_scan", "Canlı Tarama", "02_CANLI_TARAMA.png", "Canlı Tarama", "02_canli_tarama.html"),
    ScreenDefinition("signals", "Sinyaller", "03_SINYALLER.png", "Sinyaller", "03_sinyaller.html"),
    ScreenDefinition("positions", "Açık Pozisyonlar", "04_ACIK_POZISYONLAR.png", "Açık Pozisyonlar", "04_acik_pozisyonlar.html"),
    ScreenDefinition("trade_history", "İşlem Geçmişi", "05_ISLEM_GECMISI.png", "İşlem Geçmişi", "05_islem_gecmisi.html"),
    ScreenDefinition("charts", "Grafikler", "06_GRAFIKLER.png", "Grafikler", "06_grafikler.html"),
    ScreenDefinition("strategy", "Strateji", "07_STRATEJI.png", "Strateji", "07_strateji.html"),
    ScreenDefinition("risk", "Risk", "08_RISK.png", "Risk", "08_risk.html"),
    ScreenDefinition("system_health", "Sistem Sağlığı", "09_SISTEM_SAGLIGI.png", "Sistem Sağlığı", "09_sistem_sagligi.html"),
    ScreenDefinition("report_center", "Rapor Merkezi", "10_RAPOR_MERKEZI.png", "Raporlar", "10_rapor_merkezi.html"),
    ScreenDefinition("portfolio_report", "Portföy Analiz Raporu", "11_PORTFOY_ANALIZ_RAPORU.png", "Raporlar", "11_portfoy_analiz_raporu.html"),
    ScreenDefinition("performance_report", "Performans Analizi", "12_PERFORMANS_ANALIZI.png", "Raporlar", "12_performans_analizi.html"),
    ScreenDefinition("trade_analysis", "İşlem Analizi", "13_ISLEM_ANALIZI.png", "Raporlar", "13_islem_analizi.html"),
    ScreenDefinition("risk_center", "Risk Merkezi", "14_RISK_MERKEZI.png", "Raporlar", "14_risk_merkezi.html"),
    ScreenDefinition("strategy_reports", "Strateji Raporları", "15_STRATEJI_RAPORLARI.png", "Raporlar", "15_strateji_raporlari.html"),
    ScreenDefinition("custom_reports", "Özel Raporlar", "16_OZEL_RAPORLAR.png", "Raporlar", "16_ozel_raporlar.html"),
    ScreenDefinition("notifications", "Bildirimler", "17_BILDIRIMLER.png", "Bildirimler", "17_bildirimler.html"),
)

SCREEN_BY_KEY = {item.key: item for item in SCREEN_DEFINITIONS}

NAVIGATION_ITEMS = (
    ("▣", "Genel Bakış", "overview"), ("ϟ", "Canlı Tarama", "live_scan"),
    ("◎", "Sinyaller", "signals"), ("⬡", "Açık Pozisyonlar", "positions"),
    ("↶", "İşlem Geçmişi", "trade_history"), ("▥", "Grafikler", "charts"),
    ("◌", "Strateji", "strategy"), ("⬟", "Risk", "risk"),
    ("♨", "Sistem Sağlığı", "system_health"), ("▣", "Raporlar", "report_center"),
    ("✉", "Bildirimler", "notifications"),
)

REPORT_TAB_KEYS = {
    "Rapor Merkezi": "report_center", "Portföy Analiz Raporu": "portfolio_report",
    "Performans Analizi": "performance_report", "İşlem Analizi": "trade_analysis",
    "Risk Merkezi": "risk_center", "Strateji Raporları": "strategy_reports",
    "Özel Raporlar": "custom_reports",
}

SCREEN_KEYS = {
    "Genel Bakış": "overview", "Canlı Tarama": "live_scan", "Sinyaller": "signals",
    "Açık Pozisyonlar": "positions", "İşlem Geçmişi": "trade_history", "Grafikler": "charts",
    "Strateji": "strategy", "Risk": "risk", "Sistem Sağlığı": "system_health",
    "Bildirimler": "notifications",
}

REPORT_TABS = (
    ("RAPORLAR", "report_center"), ("PORTFÖY ANALİZİ", "portfolio_report"),
    ("PERFORMANS ANALİZİ", "performance_report"), ("İŞLEM ANALİZİ", "trade_analysis"),
    ("RİSK RAPORLARI", "risk_center"), ("STRATEJİ RAPORLARI", "strategy_reports"),
    ("ÖZEL RAPORLAR", "custom_reports"),
)

OPEN_POSITIONS = (
    ("BTC/USDT", "LONG", "0.0321", "68,200.00", "68,302.54", "+102.54", "+1.82%", "KAPAT"),
    ("ETH/USDT", "LONG", "0.2100", "2,576.10", "2,604.18", "+28.08", "+1.09%", "KAPAT"),
    ("BNB/USDT", "LONG", "0.8400", "592.00", "596.20", "+4.20", "+0.71%", "KAPAT"),
    ("SOL/USDT", "SHORT", "4.2500", "178.45", "175.84", "-27.61", "-1.61%", "KAPAT"),
    ("ADA/USDT", "SHORT", "1,250.0", "0.4985", "0.4915", "-6.64", "-0.63%", "KAPAT"),
    ("XRP/USDT", "LONG", "1,400.0", "0.5250", "0.5265", "+2.10", "+0.40%", "KAPAT"),
    ("MATIC/USDT", "LONG", "800.0", "0.4721", "0.4721", "+0.00", "0.00%", "KAPAT"),
    ("AVAX/USDT", "LONG", "2.0000", "37.21", "37.21", "+0.00", "0.00%", "KAPAT"),
    ("LINK/USDT", "SHORT", "5.0000", "14.80", "14.80", "+0.00", "0.00%", "KAPAT"),
)

SIGNAL_ROWS = (
    ("19:42:16", "BTC/USDT", "68,302.54", "2.23B", "YEŞİL", "DEVAM", "36.7", "12.6", "35.7", "UP", "LONG", "1", "PASS", "1H"),
    ("19:42:11", "ETH/USDT", "2,604.18", "2.42B", "YEŞİL", "DEĞİŞİM", "31.2", "15.6", "34.6", "UP", "LONG", "2", "PASS", "1H"),
    ("19:42:09", "SOL/USDT", "175.84", "812.5M", "YEŞİL", "DEVAM", "34.8", "13.9", "33.1", "UP", "LONG", "3", "PASS", "1H"),
    ("19:42:08", "BNB/USDT", "596.20", "391.2M", "KIRMIZI", "DEĞİŞİM", "16.3", "31.8", "23.9", "DOWN", "SHORT", "4", "PASS", "1H"),
    ("19:42:06", "ADA/USDT", "0.4915", "312.9M", "YEŞİL", "DEVAM", "29.1", "14.2", "24.6", "UP", "LONG", "5", "PASS", "1H"),
    ("19:42:05", "XRP/USDT", "0.5265", "256.1M", "KIRMIZI", "DEĞİŞİM", "10.2", "28.4", "22.8", "DOWN", "SHORT", "6", "PASS", "1H"),
    ("19:42:03", "MATIC/USDT", "0.4721", "218.9M", "YEŞİL", "DEVAM", "31.6", "12.8", "28.1", "UP", "LONG", "7", "PASS", "1H"),
    ("19:41:59", "AVAX/USDT", "37.21", "147.6M", "GRİ", "NÖTR", "18.2", "17.9", "19.1", "FLAT", "NO SIGNAL", "–", "–", "1H"),
    ("19:41:58", "LINK/USDT", "14.80", "74.1M", "GRİ", "NÖTR", "15.1", "15.6", "16.2", "FLAT", "NO SIGNAL", "–", "–", "1H"),
    ("19:41:56", "DOT/USDT", "6.24", "63.2M", "KIRMIZI", "DEĞİŞİM", "9.8", "24.6", "20.4", "DOWN", "BLOCKED", "–", "BLOCKED", "1H"),
)

TRADE_ROWS = (
    ("19.05.2026 18:56", "BTC/USDT", "LONG", "68,102.45", "68,302.54", "+6.42", "+0.29%", "DEVAM", "YEŞİL", "UP", "KÂR"),
    ("19.05.2026 17:41", "ETH/USDT", "LONG", "2,576.10", "2,604.18", "+5.90", "+1.09%", "DEĞİŞİM", "YEŞİL", "UP", "KÂR"),
    ("19.05.2026 16:33", "SOL/USDT", "SHORT", "178.45", "175.84", "+11.07", "+1.46%", "DEVAM", "KIRMIZI", "DOWN", "KÂR"),
    ("19.05.2026 15:22", "XRP/USDT", "LONG", "0.5256", "0.5265", "+1.26", "+0.17%", "DEVAM", "YEŞİL", "UP", "KÂR"),
    ("19.05.2026 14:18", "BNB/USDT", "LONG", "596.20", "590.81", "-4.52", "-0.90%", "DEĞİŞİM", "KIRMIZI", "DOWN", "ZARAR"),
    ("19.05.2026 13:05", "MATIC/USDT", "SHORT", "0.4915", "0.4721", "+38.80", "+3.95%", "DEĞİŞİM", "KIRMIZI", "DOWN", "KÂR"),
    ("19.05.2026 11:47", "AVAX/USDT", "LONG", "37.21", "37.21", "0.00", "0.00%", "DEĞİŞİM", "GRİ", "FLAT", "BE"),
    ("19.05.2026 10:34", "LINK/USDT", "LONG", "14.80", "14.20", "-4.44", "-0.60%", "DEVAM", "KIRMIZI", "DOWN", "ZARAR"),
)

HEALTH_SERVICES = (
    ("API Bağlantısı", "SAĞLIKLI", "78 ms", "19:42:16"), ("Piyasa Verisi Akışı", "SAĞLIKLI", "92 ms", "19:42:16"),
    ("Veritabanı", "SAĞLIKLI", "12 ms", "19:42:16"), ("Strateji Motoru", "SAĞLIKLI", "94 ms", "19:42:16"),
    ("Emir Yönetim Servisi", "SAĞLIKLI", "81 ms", "19:42:16"), ("Risk Kontrol Servisi", "SAĞLIKLI", "68 ms", "19:42:15"),
    ("Bildirim Servisi", "SAĞLIKLI", "105 ms", "19:42:15"), ("Yedekleme Servisi", "SAĞLIKLI", "134 ms", "19:42:14"),
    ("Dosya Sistemi", "SAĞLIKLI", "6 ms", "19:42:16"),
)

PLACEHOLDER_HEALTH = (
    ("API Bağlantısı", "PASS"), ("Piyasa Verisi", "PASS"), ("Veritabanı", "PASS"),
    ("Recovery", "PASS"), ("Runtime Worker", "PASS"), ("Yedekleme", "WARNING"), ("Veri Gecikmesi", "92 ms"),
)
