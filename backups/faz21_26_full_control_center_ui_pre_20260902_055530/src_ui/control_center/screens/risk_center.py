"""Safe route shell for 14_RISK_MERKEZI; visual implementation is deferred."""

from ..layout import render_placeholder_screen


def render_risk_center_screen(model=None) -> str:
    return render_placeholder_screen("Risk Merkezi", "14_RISK_MERKEZI.png", "Raporlar")
