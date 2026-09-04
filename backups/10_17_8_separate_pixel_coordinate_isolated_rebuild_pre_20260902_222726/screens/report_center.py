"""10_RAPOR_MERKEZI display-only report hub."""

from ..components import donut, kv_list, line_chart, metric_card, panel, scroll_container, table
from .report_common import render_report_page


def render_report_center_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band report-center-metrics">' + ''.join((
        metric_card("Toplam Rapor", "128", "Son 30 günde oluşturulan rapor"), metric_card("Planlanan Rapor", "24", "Yaklaşan rapor"),
        metric_card("Başarılı Rapor", "117", "%91.41 başarı oranı"), metric_card("Başarısız Rapor", "11", "%8.59 hata oranı"),
        metric_card("Ort. Oluşum Süresi", "8.42 sn", "Rapor başına ortalama süre"))) + '</div>'
    report_rows = ((str(i), name, kind, period, created, "BAŞARILI", size, "VIEW / XLSX") for i, name, kind, period, created, size in (
        (1, "Günlük Performans Raporu", "Performans", "Günlük", "19.05.2026 19:30:12", "245 KB"),
        (2, "Strateji Etkinlik Raporu", "Strateji", "Günlük", "19.05.2026 19:30:08", "187 KB"),
        (3, "Risk Analiz Raporu", "Risk", "Günlük", "19.05.2026 19:30:05", "156 KB"),
        (4, "İşlem Özeti Raporu", "İşlem", "Günlük", "19.05.2026 19:30:01", "198 KB"),
        (5, "Haftalık Performans Raporu", "Performans", "Haftalık", "19.05.2026 09:00:15", "326 KB"),
        (6, "Aylık Performans Raporu", "Performans", "Aylık", "01.05.2026 09:00:22", "412 KB"),
        (7, "Portföy Analiz Raporu", "Analiz", "Günlük", "19.05.2026 19:29:58", "267 KB"),
        (8, "Sistem Sağlık Raporu", "Sistem", "Günlük", "19.05.2026 19:29:55", "143 KB"),
        (9, "Korelasyon Analiz Raporu", "Analiz", "Haftalık", "19.05.2026 09:15:30", "289 KB"),
        (10, "Özel Strateji Raporu", "Özel", "Özel", "19.05.2026 18:45:12", "334 KB")))
    recent = table(("#", "Rapor Adı", "Tür", "Periyot", "Oluşturma Zamanı", "Durum", "Boyut", "İşlemler"), report_rows, "dense")
    primary = panel("RAPOR MERKEZİ", '<div class="screen-grid grid-2 report-primary-row report-center-map">' +
        panel("SON RAPORLAR", scroll_container(recent, "Son raporlar"), "fill") +
        panel("RAPOR TÜRÜ DAĞILIMI / RAPOR OLUŞUM TRENDİ", '<div class="stack report-center-charts">' +
            panel("RAPOR TÜRÜ DAĞILIMI", donut((("Performans", 32, "#1687d9"), ("İşlem", 28, "#4fa05b"), ("Risk", 24, "#e3ad17"), ("Strateji", 20, "#a44dc1"), ("Analiz", 16, "#32a8b8"), ("Sistem", 8, "#d84840")), "128"), "fill") +
            panel("RAPOR OLUŞUM TRENDİ (SON 30 GÜN)", line_chart(((8, 10, 9, 14, 17, 12, 18, 16, 21, 19, 22, 20, 24),), ("#1687d9",), ("Oluşturulan Rapor Sayısı",)), "fill") + '</div>', "fill") +
        '</div><div class="screen-grid grid-3 report-lower-row report-center-lower">' +
        panel("RAPOR İSTATİSTİKLERİ", kv_list((("Bu Ay Oluşturulan", "68"), ("Bu Hafta Oluşturulan", "24"), ("Bugün Oluşturulan", "8"), ("En Büyük Rapor", "2.34 MB"), ("En Küçük Rapor", "45 KB"), ("Toplam Boyut", "45.67 MB"))), "fill") +
        panel("RAPOR HATA LOGU (SON 10)", table(("Zaman", "Rapor Adı", "Hata Türü", "Hata Açıklaması", "Durum"), (("19.05 18:45", "Özel Analiz", "Veri Hatası", "Eksik veri noktaları", "BAŞARISIZ"), ("19.05 17:30", "Portföy Raporu", "API Hatası", "API timeout hatası", "BAŞARISIZ"), ("19.05 16:15", "Korelasyon", "Hesaplama Hatası", "Matematiksel hata", "BAŞARISIZ"), ("19.05 15:00", "Risk Raporu", "Veri Hatası", "Geçersiz veri formatı", "BAŞARISIZ")), "dense"), "fill") +
        panel("EN ÇOK İNDİRİLEN RAPORLAR", table(("#", "Rapor", "İndirme"), (("1", "Günlük Performans Raporu", "45"), ("2", "İşlem Özeti Raporu", "38"), ("3", "Risk Analiz Raporu", "32"), ("4", "Portföy Analiz Raporu", "28"), ("5", "Strateji Etkinlik Raporu", "25")), "dense"), "fill") + '</div>', "fill")
    secondary = panel("RAPOR OLAY AKIŞI", table(("Saat", "Olay", "Sonuç"), (("19:40", "Ledger aggregate", "PASS"), ("19:35", "PnL consistency", "PASS"), ("19:30", "XLSX validation", "PASS"), ("19:25", "Report checksum", "PASS")), "dense"), "event-panel")
    return render_report_page("RAPOR MERKEZİ", "report_center", metrics, primary, secondary, "Ledger kaynaklı rapor merkezi")
