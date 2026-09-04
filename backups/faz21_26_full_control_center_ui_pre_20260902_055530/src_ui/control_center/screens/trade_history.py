"""Safe route shell for 05_ISLEM_GECMISI; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_trade_history_screen(model=None) -> str:
    return render_placeholder_screen("İşlem Geçmişi", "05_ISLEM_GECMISI.png", "İşlem Geçmişi")
