"""Safe route shell for 04_ACIK_POZISYONLAR; no execution action is exposed."""

from ..layout import render_placeholder_screen


def render_positions_screen(model=None) -> str:
    return render_placeholder_screen("Açık Pozisyonlar", "04_ACIK_POZISYONLAR.png", "Açık Pozisyonlar")
