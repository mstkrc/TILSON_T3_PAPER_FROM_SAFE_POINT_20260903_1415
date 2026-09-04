"""16_OZEL_RAPORLAR display-only report builder."""

from ..components import action_stack, field, kv_list, metric_card, panel, table, toggle
from .report_common import render_report_page


def render_custom_reports_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-4 top-band">' + ''.join((metric_card("Kayıtlı Şablon", "6"), metric_card("Son Üretim", "19:30"), metric_card("Kaynak", "LEDGER"), metric_card("Otomatik Plan", "OFF"))) + '</div>'
    builder = panel("ÖZEL RAPOR OLUŞTURUCU", '<div class="field-grid grid-4">' + field("Tarih aralığı", "01.05 — 19.05") + field("Semboller", "TÜMÜ") + field("Yön", "LONG + SHORT") + field("Format", "XLSX") + '</div><div class="screen-grid grid-3">' + panel("ALANLAR", kv_list((("PnL detay", "ON"), ("Karar detay", "ON"), ("İndikatör", "ON"), ("Config snapshot", "ON"))), "compact") + panel("FİLTRELER", kv_list((("Min PnL", "YOK"), ("Sonuç", "TÜMÜ"), ("Mode", "PAPER"), ("Candle", "CLOSED"))), "compact") + panel("GÜVENLİK", kv_list((("Ledger source", "ZORUNLU"), ("PnL mismatch", "BLOCKING"), ("Missing ledger", "WARNING"), ("Live data", "YOK"))), "compact") + '</div>', "fill")
    templates = panel("KAYITLI ŞABLONLAR", table(("Şablon", "Kapsam", "Format", "Durum"), (("Günlük Ledger", "Bugün", "XLSX", "HAZIR"), ("Risk Özeti", "7 Gün", "XLSX", "HAZIR"), ("Strateji Detay", "30 Gün", "XLSX", "HAZIR"), ("Özel Filtre", "Kullanıcı", "XLSX", "BEKLEYEN")), "dense") + action_stack((("RAPOR OLUŞTUR · DISPLAY", "info"), ("ŞABLON KAYDET · DISABLED", "locked"))), "event-panel")
    return render_report_page("ÖZEL RAPORLAR", "custom_reports", metrics, builder, templates, "Ledger tabanlı, güvenli özel rapor tanımı")
