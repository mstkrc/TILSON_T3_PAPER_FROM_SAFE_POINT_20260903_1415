"""Safe route shell for 02_CANLI_TARAMA; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_live_scan_screen(model=None) -> str:
    return render_placeholder_screen("Canlı Tarama", "02_CANLI_TARAMA.png", "Canlı Tarama")
