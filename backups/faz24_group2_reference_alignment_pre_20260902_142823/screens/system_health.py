"""09_SISTEM_SAGLIGI diagnostic display screen."""

from ..components import action_stack, bar_chart, kv_list, line_chart, metric_card, panel, progress, scroll_container, table
from ..data import HEALTH_SERVICES
from ..layout import render_screen


def render_system_health_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-6 top-band">' + ''.join((metric_card("Genel Sağlık", "GREEN", "tüm servisler"), metric_card("API Gecikme", "78 ms", "PASS"), metric_card("Veri Gecikme", "92 ms", "PASS"), metric_card("CPU", "%38", "normal"), metric_card("Bellek", "%54", "normal"), metric_card("Son Hata", "YOK", "19:42"))) + '</div>'
    services = panel("SERVİS DURUMLARI", scroll_container(table(("Servis", "Durum", "Gecikme", "Son kontrol"), HEALTH_SERVICES, "dense"), "Servis durumları"), "fill")
    perf = panel("SİSTEM PERFORMANSI", line_chart(((32, 38, 35, 42, 39, 48, 44, 54, 50), (47, 49, 51, 48, 52, 55, 54, 57, 56)), ("#55b98a", "#d9b95d"), ("CPU", "Bellek")) + bar_chart((18, 24, 21, 28, 22, 30, 26), labels=("12", "13", "14", "15", "16", "17", "18")), "event-panel")
    alerts = panel("AKTİF UYARILAR", table(("Seviye", "Kaynak", "Mesaj"), (("WARNING", "Yedekleme", "Planlı pencere yaklaşıyor"), ("BİLGİ", "Recovery", "Checkpoint doğrulandı"), ("PASS", "Live-lock", "Kilit sağlam")), "dense"), "fill")
    resources = panel("KAYNAKLAR", progress("CPU", 38, "green") + progress("Bellek", 54, "blue") + progress("Disk", 62, "yellow") + progress("Queue", 21, "green"), "fill")
    quality = panel("VERİ KALİTESİ", kv_list((("Closed candle", "PASS"), ("Timestamp UTC/TR", "PASS"), ("Missing data", "0"), ("Stale feed", "0"), ("Ledger consistency", "PASS"))), "fill")
    logs = panel("HATA / REPAIR / DIAGNOSTIC", scroll_container(table(("Saat", "Seviye", "Bileşen", "Olay", "Aksiyon"), (("19:42:16", "INFO", "Health", "Heartbeat", "PASS"), ("19:41:44", "WARNING", "Backup", "Window pending", "MONITOR"), ("19:40:08", "INFO", "Recovery", "Gate verified", "PASS"), ("19:38:54", "INFO", "Live-lock", "Policy checked", "PASS")), "dense"), "Diagnostic logları"), "event-panel")
    backup = panel("YEDEKLEME / RECOVERY", kv_list((("Son snapshot", "19:30:00"), ("Recovery gate", "PASS"), ("Repair Mode", "GREEN"), ("STOP_AND_REPORT", "AKTİF"))) + action_stack((("DIAGNOSTIC PACKAGE", "info"), ("REPAIR MODE · DISPLAY", "warning"))), "compact")
    info = panel("SİSTEM BİLGİSİ", kv_list((("Version", "v1.6.4"), ("Runtime", "Python"), ("Mode", "PAPER ONLY"), ("Live", "LOCKED"))), "compact")
    body = metrics + f'<div class="screen-grid with-rail fill"><div class="stack fill">{services}{perf}<div class="screen-grid grid-3 lower-row">{logs}{backup}{info}</div></div><aside class="stack fill">{alerts}{resources}{quality}</aside></div>'
    return render_screen("SİSTEM SAĞLIĞI", "Sistem Sağlığı", body, "Health, error, repair ve diagnostic görünümü", "health-screen")
