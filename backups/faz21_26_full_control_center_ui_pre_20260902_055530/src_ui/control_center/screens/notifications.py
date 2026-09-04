"""Safe route shell for 17_BILDIRIMLER; no network connection is exposed."""

from ..layout import render_placeholder_screen


def render_notifications_screen(model=None) -> str:
    return render_placeholder_screen("Bildirimler", "17_BILDIRIMLER.png", "Bildirimler")
