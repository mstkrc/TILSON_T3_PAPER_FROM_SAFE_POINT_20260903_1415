"""Reusable, side-effect-free HTML components for Control Center screens."""

from __future__ import annotations

from html import escape
from typing import Iterable


def section_header(title: str, meta: str = "") -> str:
    suffix = f"<small>{escape(meta)}</small>" if meta else ""
    return f'<header class="section-header"><h2>{escape(title)}</h2>{suffix}</header>'


def badge(label: str, tone: str = "neutral") -> str:
    return f'<span class="badge badge-{escape(tone)}">{escape(label)}</span>'


def display_button(label: str, tone: str = "neutral", active: bool = False) -> str:
    state = " is-active" if active else ""
    return (
        f'<button class="display-button tone-{escape(tone)}{state}" '
        f'data-ui-intent="display-only" disabled>{escape(label)}</button>'
    )


def toggle(label: str, enabled: bool = False) -> str:
    state = "ON" if enabled else "OFF"
    return (
        f'<span class="toggle" data-state="{state}" data-ui-intent="display-only">'
        f'<b>{escape(label)}</b><i>{state}</i></span>'
    )


def status_dot(label: str, state: str = "ok", value: str = "") -> str:
    metric = f"<strong>{escape(value)}</strong>" if value else ""
    return (
        f'<span class="status-dot status-{escape(state)}"><i></i>'
        f"<b>{escape(label)}</b>{metric}</span>"
    )


def mini_value_row(label: str, value: str, tone: str = "neutral") -> str:
    return (
        '<div class="mini-value-row">'
        f"<span>{escape(label)}</span>"
        f'<strong class="value-{escape(tone)}">{escape(value)}</strong>'
        "</div>"
    )


def card(title: str, content: str, css_class: str = "") -> str:
    return (
        f'<section class="cc-card {escape(css_class)}">'
        f"{section_header(title)}<div class=\"cc-card-body\">{content}</div></section>"
    )


def table(headers: Iterable[str], rows: Iterable[Iterable[object]], css_class: str = "") -> str:
    head = "".join(f"<th>{escape(str(item))}</th>" for item in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(str(item))}</td>" for item in row) + "</tr>"
        for row in rows
    )
    return f'<table class="cc-table {escape(css_class)}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def scroll_container(content: str, label: str) -> str:
    return f'<div class="scroll-container" aria-label="{escape(label)}">{content}</div>'


def placeholder_panel(title: str, reference_file: str) -> str:
    content = (
        f"{badge('PAPER ONLY', 'paper')} {badge('LIVE LOCKED', 'locked')}"
        f'<p class="placeholder-reference">Referans: {escape(reference_file)}</p>'
        '<p>Bu ekranın görsel uygulaması henüz başlatılmadı. Modüler route güvenli biçimde hazırdır.</p>'
        '<p>Karar, emir, ledger veya execution davranışı üretilmez.</p>'
    )
    return card(title, content, "placeholder-card")
