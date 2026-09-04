"""09_SISTEM_SAGLIGI: reference-aligned, display-only diagnostic screen."""

from __future__ import annotations

from html import escape

from ..components import display_button, kv_list, panel, progress, table
from ..layout import render_screen


def _health_card(title: str, value: str, detail: str, icon: str, tone: str = "is-positive") -> str:
    return (
        '<article class="cc-panel group2-health-card">'
        f'<div><h3>{escape(title)}</h3><strong class="{escape(tone)}">{escape(value)}</strong>'
        f'<p>{escape(detail)}</p></div><span class="group2-health-icon">{escape(icon)}</span></article>'
    )


def _top_metrics() -> str:
    cards = (
        _health_card("SİSTEM DURUMU", "SAĞLIKLI", "Tüm sistemler normal çalışıyor.", "🛡"),
        _health_card("ÇALIŞMA SÜRESİ", "2g 14sa 32dk", "Son yeniden başlatma: 17.05.2026 05:09:46", "◷", "is-positive"),
        _health_card("ORTALAMA YANIT SÜRESİ", "92 ms", "API: 78 ms · DB: 12 ms · UI: 94 ms", "◔", "is-positive"),
        _health_card("SİSTEM YÜKÜ", "23%", "CPU: 23% · RAM: 46% · Disk: 31%", "▣", "is-positive"),
        _health_card("AKTİF BAĞLANTILAR", "8 / 20", "API: 3 · DB: 2 · Market: 3", "⌘", "is-info"),
        _health_card("VERİ GECİKMESİ", "92 ms", "Piyasa Verisi: 92 ms · Veritabanı: 4 ms", "◷", "is-positive"),
    )
    return '<div class="group2-health-top">' + "".join(cards) + "</div>"


def _services() -> str:
    rows = (
        ("○", "API Bağlantısı", "SAĞLIKLI", "78 ms", "19:42:16"),
        ("○", "Piyasa Verisi Akışı", "SAĞLIKLI", "92 ms", "19:42:16"),
        ("○", "Veritabanı", "SAĞLIKLI", "12 ms", "19:42:16"),
        ("○", "Strateji Motoru", "SAĞLIKLI", "94 ms", "19:42:16"),
        ("○", "Emir Yönetim Servisi", "SAĞLIKLI", "81 ms", "19:42:16"),
        ("○", "Risk Kontrol Servisi", "SAĞLIKLI", "68 ms", "19:42:15"),
        ("○", "Bildirim Servisi", "SAĞLIKLI", "105 ms", "19:42:15"),
        ("○", "Yedekleme Servisi", "SAĞLIKLI", "134 ms", "19:42:14"),
        ("○", "Dosya Sistemi", "SAĞLIKLI", "6 ms", "19:42:16"),
    )
    return panel(
        "HİZMET DURUMLARI",
        table(("", "HİZMET", "DURUM", "YANIT SÜRESİ", "SON KONTROL"), rows, "dense"),
        "fill",
    )


def _sparkline(color: str, points: str, value: str, label: str) -> str:
    return (
        '<article class="group2-perf-card">'
        f'<header><span>{escape(label)}</span><b style="color:{escape(color)}">{escape(value)}</b></header>'
        '<svg viewBox="0 0 300 100" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M0 25H300M0 50H300M0 75H300" stroke="#183440" fill="none"/>'
        f'<polyline points="{escape(points)}" fill="none" stroke="{escape(color)}" stroke-width="3"/>'
        "</svg><small>19:42 &nbsp;&nbsp; 01:42 &nbsp;&nbsp; 07:42 &nbsp;&nbsp; 13:42 &nbsp;&nbsp; 19:42</small></article>"
    )


def _performance() -> str:
    cpu = _sparkline("#78d326", "0,72 20,67 40,60 60,69 80,59 100,63 120,54 140,58 160,64 180,51 200,56 220,47 240,54 260,42 280,48 300,39", "23%", "CPU KULLANIMI (%)")
    ram = _sparkline("#39aeea", "0,65 20,60 40,51 60,56 80,47 100,52 120,41 140,49 160,43 180,35 200,44 220,32 240,40 260,34 280,46 300,39", "46%", "RAM KULLANIMI (%)")
    disk = _sparkline("#b844c1", "0,69 20,63 40,66 60,54 80,62 100,58 120,64 140,55 160,60 180,49 200,57 220,50 240,61 260,52 280,59 300,53", "31%", "DİSK KULLANIMI (%)")
    network_in = _sparkline("#6fcf2c", "0,64 20,53 40,59 60,45 80,56 100,47 120,61 140,51 160,58 180,43 200,55 220,48 240,59 260,46 280,54 300,49", "Gelen: 128 KB/s", "AĞ TRAFİĞİ")
    network_out = _sparkline("#27b4e6", "0,74 20,66 40,70 60,57 80,68 100,60 120,71 140,62 160,68 180,55 200,65 220,59 240,70 260,58 280,66 300,61", "Giden: 96 KB/s", "AĞ ÇIKIŞI")
    delay = _sparkline("#ffb814", "0,58 20,42 40,55 60,39 80,62 100,47 120,71 140,54 160,63 180,58 200,49 220,57 240,44 260,52 280,47 300,53", "92 ms", "VERİ AKIŞI GECİKMESİ")
    return panel(
        "SİSTEM PERFORMANS GRAFİKLERİ",
        f'<div class="group2-perf-grid">{cpu}{ram}{disk}{network_in}{network_out}{delay}</div>',
        "fill",
        "SON 24 SAAT",
    )


def _event_log() -> str:
    rows = (
        ("19:42:16", "INFO", "API Service", "Bağlantı Kontrolü", "API bağlantısı başarılı"),
        ("19:42:15", "INFO", "Market Data", "Veri Akışı", "Piyasa verisi akışı normal"),
        ("19:42:15", "INFO", "Database", "Senkronizasyon", "Veritabanı senkronizasyonu tamamlandı"),
        ("19:42:14", "INFO", "Backup Service", "Yedekleme", "Otomatik yedekleme tamamlandı"),
        ("19:42:13", "INFO", "Risk Service", "Risk Kontrol", "Risk kontrolleri çalıştırıldı"),
        ("19:42:12", "WARN", "Strategy Engine", "Performans", "Strateji hesaplama süresi yüksek (156ms)"),
        ("19:42:11", "INFO", "Order Service", "Emir Yönetimi", "Emir yönetim servisi hazır"),
        ("19:42:10", "INFO", "Notification", "Bildirim", "Bildirim servisi aktif"),
    )
    return panel(
        "SİSTEM OLAY GÜNLÜĞÜ",
        table(("ZAMAN", "SEVİYE", "KAYNAK", "OLAY", "AÇIKLAMA"), rows, "dense"),
        "fill",
        "SON 20",
    )


def _backup_status() -> str:
    return panel(
        "YEDEKLEME DURUMU",
        kv_list(
            (
                ("Son Yedekleme Zamanı", "19.05.2026 18:42:14"),
                ("Sonraki Yedekleme", "19.05.2026 20:42:14"),
                ("Yedekleme Durumu", "BAŞARILI"),
                ("Yedekleme Boyutu", "2.34 GB"),
                ("Yedekleme Türü", "Tam Yedekleme"),
                ("Yedekleme Konumu", "/backups/daily/"),
            )
        )
        + display_button("HEMEN YEDEKLE · UIINTENT", "info"),
        "fill",
        "DISPLAY-ONLY",
    )


def _system_info() -> str:
    return panel(
        "SİSTEM BİLGİLERİ",
        kv_list(
            (
                ("Uygulama Versiyonu", "v1.6.4"), ("Çalışma Modu", "PAPER MODE"),
                ("Sunucu", "FRA-1"), ("İşletim Sistemi", "Linux 5.15.0"),
                (".NET Versiyonu", ".NET 8.0.5"), ("Başlangıç Zamanı", "17.05.2026 05:09:46"),
                ("Toplam İşlem Sayısı", "12,568"),
            )
        ),
        "fill",
    )


def _right_rail() -> str:
    alerts = panel(
        "AKTİF UYARILAR",
        '<div class="group2-note info"><b class="is-positive">✓ Aktif uyarı bulunmuyor.</b><br><br>Tüm sistemler normal çalışıyor.</div>',
        "fill",
    )
    resources = panel(
        "KAYNAK KULLANIMI",
        '<div class="group2-resource-list">'
        + progress("CPU Kullanımı", 23, "green", "23%")
        + progress("RAM Kullanımı", 46, "blue", "3.7 GB / 8 GB")
        + progress("Disk Kullanımı", 31, "purple", "156 GB / 500 GB")
        + progress("Ağ Bandwidth", 29, "yellow", "285 Mbps / 1 Gbps")
        + "</div>",
        "fill",
    )
    quality = panel(
        "VERİ KALİTESİ ÖZETİ",
        kv_list(
            (
                ("Piyasa Verisi", "SAĞLIKLI · 92 ms"), ("Tarihsel Veri", "SAĞLIKLI · 125 ms"),
                ("Hesap Verisi", "SAĞLIKLI · 45 ms"), ("Pozisyon Senkronizasyonu", "SAĞLIKLI · 38 ms"),
                ("Closed Candle", "PASS"), ("Ledger Consistency", "PASS"),
            )
        ),
        "fill",
    )
    return f'<aside class="stack fill">{alerts}{resources}{quality}</aside>'


def render_system_health_screen(model=None) -> str:
    middle = f'<div class="group2-health-middle">{_services()}{_performance()}</div>'
    lower = f'<div class="group2-health-lower">{_event_log()}{_backup_status()}{_system_info()}</div>'
    body = (
        '<div class="group2-panel-map group2-health-map" data-panel-map="09_SISTEM_SAGLIGI">'
        + '<div class="group2-health-layout"><div class="group2-health-left">'
        + _top_metrics() + f'<div class="group2-health-main">{middle}{lower}</div>'
        + '</div>' + _right_rail() + '</div></div>'
    )
    return render_screen(
        "SİSTEM SAĞLIĞI",
        "Sistem Sağlığı",
        body,
        "Servis, performans, veri kalitesi ve recovery görünümü",
        "group2-screen group2-health-screen",
    )
