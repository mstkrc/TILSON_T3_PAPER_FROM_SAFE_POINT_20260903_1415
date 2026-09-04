"""Safe route shell for 07_STRATEJI; no config mutation is exposed."""

from ..layout import render_placeholder_screen


def render_strategy_screen(model=None) -> str:
    return render_placeholder_screen("Strateji", "07_STRATEJI.png", "Strateji")
