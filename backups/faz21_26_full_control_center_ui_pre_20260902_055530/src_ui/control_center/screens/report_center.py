"""Safe route shell for 10_RAPOR_MERKEZI; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_report_center_screen(model=None) -> str:
    return render_placeholder_screen("Rapor Merkezi", "10_RAPOR_MERKEZI.png", "Raporlar")
