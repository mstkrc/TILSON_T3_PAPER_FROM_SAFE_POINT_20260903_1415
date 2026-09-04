"""10_RAPOR_MERKEZI display-only report hub."""

from ..components import bar_chart, metric_card, panel, scroll_container, table
from .report_common import render_report_page


def render_report_center_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-5 top-band">' + ''.join((metric_card("Toplam İşlem", "128"), metric_card("Net PnL", "+$486.20"), metric_card("Win Rate", "%64.1"), metric_card("Profit Factor", "1.84"), metric_card("Ledger", "PASS"))) + '</div>'
    primary = panel("RAPOR MERKEZİ", '<div class="screen-grid grid-3">' + panel("GÜNLÜK ÖZET", bar_chart((18, -7, 24, 14, -11, 31, 22), labels=("Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz")), "compact") + panel("SON RAPORLAR", scroll_container(table(("Rapor", "Tarih", "Durum"), (("Portföy Analizi", "19.05", "PASS"), ("Performans", "19.05", "PASS"), ("Risk Merkezi", "19.05", "PASS")), "dense"), "Son raporlar"), "compact") + panel("VERİ DURUMU", table(("Kaynak", "Durum"), (("Ledger", "PASS"), ("PnL", "PASS"), ("Config Snapshot", "PASS"), ("Excel", "PASS")), "dense"), "compact") + '</div>', "fill")
    secondary = panel("RAPOR OLAY AKIŞI", table(("Saat", "Olay", "Sonuç"), (("19:40", "Ledger aggregate", "PASS"), ("19:35", "PnL consistency", "PASS"), ("19:30", "XLSX validation", "PASS")), "dense"), "event-panel")
    return render_report_page("RAPOR MERKEZİ", "report_center", metrics, primary, secondary, "Ledger kaynaklı rapor merkezi")
