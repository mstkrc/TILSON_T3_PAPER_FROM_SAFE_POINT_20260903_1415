"""Display-only route and demo metadata for the modular Control Center."""

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


SCREEN_DEFINITIONS = (
    ScreenDefinition("overview", "Genel Bakış", "01_GENEL_BAKIS.png", "Genel Bakış"),
    ScreenDefinition("live_scan", "Canlı Tarama", "02_CANLI_TARAMA.png", "Canlı Tarama"),
    ScreenDefinition("signals", "Sinyaller", "03_SINYALLER.png", "Sinyaller"),
    ScreenDefinition("positions", "Açık Pozisyonlar", "04_ACIK_POZISYONLAR.png", "Açık Pozisyonlar"),
    ScreenDefinition("trade_history", "İşlem Geçmişi", "05_ISLEM_GECMISI.png", "İşlem Geçmişi"),
    ScreenDefinition("charts", "Grafikler", "06_GRAFIKLER.png", "Grafikler"),
    ScreenDefinition("strategy", "Strateji", "07_STRATEJI.png", "Strateji"),
    ScreenDefinition("risk", "Risk", "08_RISK.png", "Risk"),
    ScreenDefinition("system_health", "Sistem Sağlığı", "09_SISTEM_SAGLIGI.png", "Sistem Sağlığı"),
    ScreenDefinition("report_center", "Rapor Merkezi", "10_RAPOR_MERKEZI.png", "Raporlar"),
    ScreenDefinition("portfolio_report", "Portföy Analiz Raporu", "11_PORTFOY_ANALIZ_RAPORU.png", "Raporlar"),
    ScreenDefinition("performance_report", "Performans Analizi", "12_PERFORMANS_ANALIZI.png", "Raporlar"),
    ScreenDefinition("trade_analysis", "İşlem Analizi", "13_ISLEM_ANALIZI.png", "Raporlar"),
    ScreenDefinition("risk_center", "Risk Merkezi", "14_RISK_MERKEZI.png", "Raporlar"),
    ScreenDefinition("strategy_reports", "Strateji Raporları", "15_STRATEJI_RAPORLARI.png", "Raporlar"),
    ScreenDefinition("custom_reports", "Özel Raporlar", "16_OZEL_RAPORLAR.png", "Raporlar"),
    ScreenDefinition("notifications", "Bildirimler", "17_BILDIRIMLER.png", "Bildirimler"),
)

SCREEN_BY_KEY = {definition.key: definition for definition in SCREEN_DEFINITIONS}

NAVIGATION_ITEMS = (
    ("Genel Bakış", "overview"),
    ("Canlı Tarama", "live_scan"),
    ("Sinyaller", "signals"),
    ("Açık Pozisyonlar", "positions"),
    ("İşlem Geçmişi", "trade_history"),
    ("Grafikler", "charts"),
    ("Strateji", "strategy"),
    ("Risk", "risk"),
    ("Sistem Sağlığı", "system_health"),
    ("Raporlar", "report_center"),
    ("Bildirimler", "notifications"),
)

REPORT_TAB_KEYS = {
    "Rapor Merkezi": "report_center",
    "Portföy Analiz Raporu": "portfolio_report",
    "Performans Analizi": "performance_report",
    "İşlem Analizi": "trade_analysis",
    "Risk Merkezi": "risk_center",
    "Strateji Raporları": "strategy_reports",
    "Özel Raporlar": "custom_reports",
}

SCREEN_KEYS = {
    "Genel Bakış": "overview",
    "Canlı Tarama": "live_scan",
    "Sinyaller": "signals",
    "Açık Pozisyonlar": "positions",
    "İşlem Geçmişi": "trade_history",
    "Grafikler": "charts",
    "Strateji": "strategy",
    "Risk": "risk",
    "Sistem Sağlığı": "system_health",
    "Bildirimler": "notifications",
}

PLACEHOLDER_HEALTH = (
    ("API Bağlantısı", "PASS"),
    ("Piyasa Verisi", "PASS"),
    ("Recovery", "PASS"),
    ("Live Lock", "LOCKED"),
)
