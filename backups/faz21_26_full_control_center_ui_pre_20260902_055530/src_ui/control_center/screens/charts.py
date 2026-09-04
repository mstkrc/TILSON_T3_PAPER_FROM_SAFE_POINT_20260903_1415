"""Safe route shell for 06_GRAFIKLER; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_charts_screen(model=None) -> str:
    return render_placeholder_screen("Grafikler", "06_GRAFIKLER.png", "Grafikler")
