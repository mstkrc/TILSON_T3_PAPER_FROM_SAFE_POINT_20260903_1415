"""Safe route shell for 03_SINYALLER; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_signals_screen(model=None) -> str:
    return render_placeholder_screen("Sinyaller", "03_SINYALLER.png", "Sinyaller")
