"""07_STRATEJI display-only configuration review screen."""

from ..components import action_stack, display_button, field, kv_list, panel, table, toggle
from ..layout import render_screen


def _controls() -> str:
    return '<div class="control-grid">' + ''.join((display_button("DEĞİŞİM", "info", True), display_button("DEVAM", "neutral"), display_button("ON", "success", True), display_button("OFF", "neutral"), display_button("N = 6", "warning"), display_button("%2", "warning"))) + '</div>'


def render_strategy_screen(model=None) -> str:
    management = panel("STRATEJİ YÖNETİMİ", '<div class="field-grid grid-4">' + field("Aktif strateji", "Tilson T3 Slope") + field("Profil", "PAPER DEFAULT") + field("Config source", "LOCKED SNAPSHOT") + field("Apply", "DISABLED") + '</div>', "compact", "AUTO APPLY YOK")
    params = '<div class="screen-grid grid-4 strategy-panels">' + ''.join((
        panel("TILSON T3", kv_list((("Factor", "0.70"), ("Period", "8"), ("Entry Mode", "DEĞİŞİM"))) + _controls(), "fill"),
        panel("DMI / ADX", kv_list((("DMI Length", "14"), ("ADX Smoothing", "14"), ("Threshold", "20"), ("Slope", "ON / N=6"))) + _controls(), "fill"),
        panel("VOLUME / CANDLE", kv_list((("Volume Filter", "ON"), ("Closed Candle", "ZORUNLU"), ("UI Refresh", "2 dk"), ("Decision", "REFRESH'TE YOK"))) + toggle("Open candle", False), "fill"),
        panel("RİSK PARAMETRELERİ", kv_list((("Max Coin", "10"), ("Allocation", "%10"), ("Leverage", "3x"), ("Stop Loss", "ON / %2"))) + _controls(), "fill"),
    )) + '</div>'
    summary = panel("STRATEJİ ÖZETİ", kv_list((("Ad", "Tilson T3 Slope"), ("Durum", "PAPER / PASS"), ("Sinyal", "CLOSED CANDLE"), ("Direct apply", "YASAK"), ("Optimization transfer", "YOK"), ("Live enable", "LOCKED"))), "fill")
    ready = panel("HAZIR STRATEJİLER", table(("Profil", "Mode", "Durum"), (("PAPER DEFAULT", "Slope", "AKTİF"), ("CONSERVATIVE", "Slope", "BEKLEYEN"), ("RESEARCH", "Display", "KİLİTLİ")), "dense"), "fill")
    actions = panel("KONTROLLER", action_stack((("DEĞİŞİKLİĞİ KAYDET · DISABLED", "locked"), ("CONFIG SNAPSHOT", "info"), ("GERİ AL · DISABLED", "neutral"))), "compact")
    rules = panel("SİNYAL KURAL AKIŞI", table(("Adım", "Kural", "Durum"), (("1", "Closed candle", "PASS"), ("2", "T3 değişim/devam", "PASS"), ("3", "DMI direction", "PASS"), ("4", "ADX threshold/slope", "PASS"), ("5", "Volume filter", "PASS"), ("6", "Risk permission", "PASS")), "dense"), "event-panel")
    body = management + params + f'<div class="screen-grid with-rail fill"><div class="stack fill">{rules}</div><aside class="stack fill">{summary}{ready}{actions}</aside></div>'
    return render_screen("STRATEJİ", "Strateji", body, "Parametre görünümü · config mutation ve auto apply yok", "strategy-screen")
