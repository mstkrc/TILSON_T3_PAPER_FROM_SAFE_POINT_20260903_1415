"""16_OZEL_RAPORLAR display-only report builder."""

from ..components import action_stack, field, kv_list, metric_card, panel, table, toggle
from .report_common import render_report_page


def render_custom_reports_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Kayıtlı Şablon", "6"), metric_card("Son Üretim", "19:30"), metric_card("Kaynak", "LEDGER"), metric_card("Otomatik Plan", "OFF"), metric_card("Üretim", "DISPLAY"))) + '</div>'
    builder = panel("ÖZEL RAPOR OLUŞTURUCU", '<div class="field-grid grid-4">' + field("Tarih aralığı", "01.09 – 02.09") + field("Semboller", "TÜMÜ") + field("Yön", "LONG + SHORT") + field("Format", "XLSX") + '</div><div class="screen-grid grid-3 custom-builder-row">' + panel("ALANLAR", kv_list((("PnL detay", "ON"), ("Karar detay", "ON"), ("İndikatör", "ON"), ("Config snapshot", "ON"))), "compact") + panel("FİLTRELER", kv_list((("Min PnL", "YOK"), ("Sonuç", "TÜMÜ"), ("Mode", "PAPER"), ("Candle", "CLOSED"))), "compact") + panel("GÜVENLİK", kv_list((("Ledger source", "ZORUNLU"), ("PnL mismatch", "BLOCKING"), ("Missing ledger", "WARNING"), ("Live data", "YOK"))), "compact") + '</div>', "fill")
    secondary = panel("RAPOR ÇIKTI / GEÇMİŞ", '<div class="screen-grid grid-3 custom-output-row">' + panel("KAYITLI ŞABLONLAR", table(("Şablon", "Kapsam", "Durum"), (("Günlük Ledger", "Bugün", "HAZIR"), ("Risk Özeti", "7 Gün", "HAZIR"), ("Strateji Detay", "30 Gün", "HAZIR")), "dense"), "fill") + panel("ÖNİZLEME / FORMAT", kv_list((("Önizleme", "DISPLAY"), ("XLSX", "HAZIR"), ("PDF", "DISABLED"), ("Email", "OFF"))), "fill") + panel("ÜRETİM GEÇMİŞİ", table(("Saat", "Rapor", "Durum"), (("19:30", "Günlük Ledger", "PASS"), ("18:30", "Risk Özeti", "PASS")), "dense"), "fill") + '</div>' + action_stack((("RAPOR OLUŞTUR · DISPLAY", "info"), ("ŞABLON KAYDET · DISABLED", "locked"))), "event-panel")
    return render_report_page("ÖZEL RAPORLAR", "custom_reports", metrics, builder, secondary, "Ledger tabanlı, güvenli özel rapor tanımı")
