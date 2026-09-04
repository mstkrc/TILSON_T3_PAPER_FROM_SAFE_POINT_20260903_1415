"""Shared report-page shell; all controls are display-only."""

from ..components import action_stack, kv_list, panel, report_tabs
from ..layout import render_screen


def render_report_page(title: str, active_key: str, metrics: str, primary: str, secondary: str, note: str) -> str:
    quick = panel("HIZLI RAPOR", action_stack((("BUGÜN", "info"), ("SON 7 GÜN", "neutral"), ("SON 30 GÜN", "neutral"), ("ÖZEL ARALIK", "neutral"))), "compact")
    plan = panel("RAPOR PLANI", kv_list((("Kaynak", "LEDGER"), ("Timezone", "UTC / TR"), ("Güncelleme", "DISPLAY ONLY"), ("Gerçek trade", "YOK"))), "fill")
    export = panel("DIŞA AKTARMA", action_stack((("XLSX · OPENPYXL", "success"), ("PDF · DISABLED", "locked"), ("OTOMATİK GÖNDERİM · OFF", "neutral"))), "compact")
    body = report_tabs(active_key) + metrics + f'<div class="screen-grid with-rail fill"><div class="stack fill">{primary}{secondary}</div><aside class="stack fill">{quick}{plan}{export}</aside></div>'
    return render_screen(title, "Raporlar", body, note, "reports-screen")
