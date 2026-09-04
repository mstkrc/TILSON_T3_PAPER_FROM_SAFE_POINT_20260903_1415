"""Thin orchestrator for the modular, paper-only Control Center renderer."""

from __future__ import annotations

from pathlib import Path

from .control_center import ControlCenterModel, build_control_center
from .control_center.screens import render_overview_screen, render_screen

OUTPUT_ENCODING = "utf-8"
DEFAULT_OUTPUT = Path("outputs/faz21_control_center.html")


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


def write_default_output() -> Path:
    """Write the standard HTML artifact without triggering runtime behavior."""
    render_control_center(output=DEFAULT_OUTPUT)
    return DEFAULT_OUTPUT


if __name__ == "__main__":
    write_default_output()


__all__ = ["DEFAULT_OUTPUT", "OUTPUT_ENCODING", "render_control_center", "render_screen_shell", "write_default_output"]
