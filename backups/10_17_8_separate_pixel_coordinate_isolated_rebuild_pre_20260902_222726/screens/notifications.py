"""17_BILDIRIMLER security-focused display-only screen."""

from ..components import action_stack, kv_list, metric_card, panel, scroll_container, table, toggle
from ..layout import render_screen


def render_notifications_screen(model=None) -> str:
    metrics = '<div class="metric-grid grid-6 top-band">' + ''.join((metric_card("Bugün", "42", "bildirim"), metric_card("Başarılı", "40", "%95.2"), metric_card("Kuyruk", "2", "bekliyor"), metric_card("Reddedilen", "3", "unauthorized"), metric_card("Kanal", "MODEL", "read-only"), metric_card("Ağ", "YOK", "security"))) + '</div>'
    channels = panel("KANAL DURUMU", kv_list((("Telegram model", "HAZIR"), ("Gerçek ağ", "YOK"), ("Whitelist", "AKTİF"), ("Unauthorized audit", "AKTİF"), ("Read-only commands", "AKTİF"))), "fill")
    rules = panel("BİLDİRİM KURALLARI", table(("Olay", "Kanal", "Durum"), (("Signal PASS", "Telegram", "ON"), ("Risk BLOCK", "Telegram", "ON"), ("Health CRITICAL", "Telegram", "ON"), ("Daily summary", "Telegram", "ON"), ("Live enable", "—", "DISABLED")), "dense"), "fill")
    whitelist = panel("WHITELIST / ROLLER", table(("Kimlik", "Rol", "Yetki"), (("user-001", "OWNER", "READ ONLY"), ("user-ops", "OPERATOR", "STATUS / PNL"), ("unknown", "NONE", "REJECT")), "dense"), "fill")
    latest = panel("SON BİLDİRİMLER", scroll_container(table(("Saat", "Seviye", "Olay", "Hedef", "Durum"), (("19:42:16", "INFO", "BTC signal PASS", "Whitelist", "BAŞARILI"), ("19:41:44", "WARNING", "Backup window", "Whitelist", "BAŞARILI"), ("19:40:18", "SECURITY", "Unauthorized command", "Audit", "REJECT"), ("19:39:05", "INFO", "Daily PnL", "Whitelist", "BAŞARILI")), "dense"), "Son bildirimler"), "fill")
    queued = panel("KUYRUKTA", scroll_container(table(("Sıra", "Olay", "Plan", "Durum"), (("1", "Health summary", "19:45", "BEKLEYEN"), ("2", "Ledger summary", "20:00", "BEKLEYEN")), "dense"), "Bildirim kuyruğu"), "fill")
    controls = panel("GÜVENLİK KONTROLLERİ", kv_list((("Manual close", "DISABLED"), ("Settings change", "DISABLED"), ("Live enable", "DISABLED"), ("Panic", "ÇİFT ONAY MODELİ"))) + '<div class="toggle-row">' + toggle("Telegram ağı", False) + toggle("Live komutu", False) + '</div>', "fill")
    actions = panel("HIZLI AKSİYONLAR", action_stack((("TEST BİLDİRİMİ · DISABLED", "neutral"), ("AUDIT GÖRÜNÜMÜ", "info"), ("PANIC ONAY AKIŞI · DISPLAY", "danger"))), "fill")
    mute = panel("SESSİZE ALMA KURALLARI", kv_list((("Info tekrar", "5 dk"), ("Warning tekrar", "1 dk"), ("Critical", "ASLA"))), "fill")
    body = metrics + f'<div class="screen-grid with-rail fill"><div class="stack fill"><div class="screen-grid grid-3">{channels}{rules}{whitelist}</div><div class="screen-grid grid-2 notifications-lower">{latest}{queued}</div></div><aside class="stack fill">{controls}{actions}{mute}</aside></div>'
    return render_screen("BİLDİRİMLER", "Bildirimler", body, "Whitelist, audit ve read-only Telegram güvenlik modeli", "notifications-screen")
