"""Thin orchestrator for the modular, paper-only Control Center renderer."""

from __future__ import annotations

from pathlib import Path

from .control_center import ControlCenterModel, build_control_center
from .control_center.data import SCREEN_DEFINITIONS
from .control_center.screens import SCREEN_RENDERERS, render_overview_screen, render_screen

OUTPUT_ENCODING = "utf-8"
DEFAULT_OUTPUT = Path("outputs/faz21_control_center.html")
ROUTE_OUTPUT_DIR = Path("outputs/control_center")


def render_screen_shell(
    screen: str,
    model: ControlCenterModel | None = None,
    report_tab: str | None = None,
) -> str:
    """Render a safe modular route; no paper/live action is executed."""
    return render_screen(screen, model=model, report_tab=report_tab)


def render_control_center(
    model: ControlCenterModel | None = None,
    output: str | Path | None = None,
) -> str:
    """Render the approved General Overview through its dedicated screen module."""
    return render_overview_screen(model or build_control_center(), output=output)


def write_all_outputs(model: ControlCenterModel | None = None) -> tuple[Path, ...]:
    """Write all approved route artifacts without runtime or execution effects."""
    model = model or build_control_center()
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ROUTE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    render_overview_screen(model, output=DEFAULT_OUTPUT)
    written = [DEFAULT_OUTPUT]
    for definition in SCREEN_DEFINITIONS:
        if definition.key == "overview":
            continue
        target = ROUTE_OUTPUT_DIR / definition.output_file
        target.write_text(SCREEN_RENDERERS[definition.key](model), encoding=OUTPUT_ENCODING, newline="\n")
        written.append(target)
    return tuple(written)


def write_default_output() -> Path:
    """Write the overview and every modular route without triggering runtime behavior."""
    write_all_outputs()
    return DEFAULT_OUTPUT


if __name__ == "__main__":
    write_default_output()


__all__ = ["DEFAULT_OUTPUT", "OUTPUT_ENCODING", "ROUTE_OUTPUT_DIR", "render_control_center", "render_screen_shell", "write_all_outputs", "write_default_output"]
