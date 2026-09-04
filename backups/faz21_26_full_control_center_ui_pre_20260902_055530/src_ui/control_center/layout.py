"""Shared document shell for modular Control Center screens."""

from __future__ import annotations

from html import escape

from .components import display_button, placeholder_panel, status_dot
from .data import NAVIGATION_ITEMS, PLACEHOLDER_HEALTH
from .theme import COMMON_THEME_CSS


def render_sidebar(active_label: str) -> str:
    nav = "".join(
        f'<a class="{"active" if label == active_label else ""}" data-route="{escape(key)}">{escape(label)}</a>'
        for label, key in NAVIGATION_ITEMS
    )
    return (
        '<aside class="cc-sidebar"><div class="cc-brand">EMA MODEL<br>TRADE'
        '<small>ALGORİTMA TİCARET SİSTEMİ</small></div>'
        f'<nav class="cc-nav">{nav}</nav></aside>'
    )


def render_topbar(title: str) -> str:
    controls = "".join(
        (
            display_button("SİSTEMİ DURDUR", "danger"),
            display_button("SİSTEMİ ÇALIŞTIR", "success"),
            display_button("PAPER AKTİF", "paper", True),
            display_button("LIVE HAZIR 🔒", "locked"),
        )
    )
    return (
        f'<header class="cc-topbar"><div>{controls}</div><strong>{escape(title)}</strong>'
        '<span>LIVE_TRADING=false</span></header>'
    )


def render_healthbar() -> str:
    items = "".join(
        status_dot(label, "locked" if value == "LOCKED" else "ok", value)
        for label, value in PLACEHOLDER_HEALTH
    )
    return f'<footer class="cc-healthbar"><b>SİSTEM SAĞLIĞI</b>{items}</footer>'


def render_document(title: str, active_label: str, content: str) -> str:
    return (
        '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{escape(title)} · Tilson T3 Control Center</title>\n<style>{COMMON_THEME_CSS}</style>\n'
        '</head>\n<body>\n<div class="cc-document" data-paper-only="true" data-live-locked="true" '
        'data-live-order-sending-allowed="false">'
        f'{render_sidebar(active_label)}{render_topbar(title)}'
        f'<main class="cc-main">{content}</main>{render_healthbar()}'
        '</div>\n</body>\n</html>\n'
    )


def render_placeholder_screen(title: str, reference_file: str, active_label: str) -> str:
    content = (
        f'<section class="screen-shell" data-screen="{escape(title)}" data-paper-only="true" '
        f'data-live-locked="true">{placeholder_panel(title, reference_file)}</section>'
    )
    return render_document(title, active_label, content)
