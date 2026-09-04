"""Shared document shell for modular Control Center screens."""

from __future__ import annotations

from html import escape

from .components import display_button, panel, status_dot
from .data import NAVIGATION_ITEMS, PLACEHOLDER_HEALTH, SCREEN_BY_KEY
from .theme import COMMON_THEME_CSS


def render_sidebar(active_label: str) -> str:
    links = []
    for icon, label, key in NAVIGATION_ITEMS:
        item = SCREEN_BY_KEY[key]
        links.append(f'<a class="{"active" if label == active_label else ""}" href="{escape(item.output_file)}" data-route="{escape(key)}"><span class="nav-icon">{escape(icon)}</span><span>{escape(label)}</span></a>')
    return '<aside class="cc-sidebar"><div class="cc-brand">EMA MODEL TRADE<small>ALGORİTMA TİCARET SİSTEMİ</small></div>' + f'<nav class="cc-nav">{"".join(links)}</nav>' + '<div class="sidebar-meta"><span>MOD</span><b>PAPER MODE</b><span>HESAP TÜRÜ</span><b class="account">OKX (TESTNET)</b><span>API</span><b>Bağlı</b><span>v1.6.4</span></div></aside>'


def render_topbar() -> str:
    controls = "".join((display_button("SİSTEMİ DURDUR", "danger"), display_button("SİSTEMİ ÇALIŞTIR", "success"), display_button("YENİ GİRİŞLERİ DURDUR", "warning"), display_button("ACİL DURDUR", "danger"), display_button("PAPER AKTİF", "paper", True), display_button("LIVE HAZIR 🔒", "locked")))
    return f'<header class="cc-topbar"><div class="command-row">{controls}</div><div class="system-info"><span>Sistem: v1.6.4</span><span>Sunucu: FRA-1</span><span>Saat: 19:42:18</span><span>UTC+3</span><span>Çalışma Süresi: 2g 14sa 32dk</span></div></header>'


def render_healthbar() -> str:
    items = "".join(status_dot(label, "warning" if value == "WARNING" else "ok", value if value == "92 ms" else "") for label, value in PLACEHOLDER_HEALTH)
    return f'<footer class="cc-healthbar"><b>SİSTEM SAĞLIĞI</b>{items}</footer>'


def render_document(title: str, active_label: str, content: str) -> str:
    return '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + f'<title>{escape(title)} · Tilson T3 Control Center</title>\n<style>{COMMON_THEME_CSS}</style>\n</head>\n<body>\n' + '<div class="cc-document" data-target-viewport="1920x1080" data-paper-only="true" data-live-locked="true" data-live-order-sending-allowed="false">' + f'{render_sidebar(active_label)}{render_topbar()}<main class="cc-main">{content}</main>{render_healthbar()}' + '<span class="safety-footer">LIVE_TRADING=false · live_order_sending_allowed=false · real_order_endpoint=none</span></div>\n</body>\n</html>\n'


def render_screen(title: str, active_label: str, body: str, subtitle: str = "", css_class: str = "") -> str:
    title_html = f'<div class="screen-title"><h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>'
    return render_document(title, active_label, f'<section class="screen-content {escape(css_class)}">{title_html}{body}</section>')


def render_placeholder_screen(title: str, reference_file: str, active_label: str) -> str:
    return render_screen(title, active_label, panel(title, f'<p>Referans: {escape(reference_file)}</p><p>PAPER ONLY · LIVE LOCKED</p>', "fill"), "Güvenli screen shell")
