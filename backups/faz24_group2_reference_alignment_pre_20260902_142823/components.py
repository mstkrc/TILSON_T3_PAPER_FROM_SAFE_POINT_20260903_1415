"""Reusable, side-effect-free HTML components for Control Center screens."""

from __future__ import annotations

from html import escape
from typing import Iterable, Sequence


def semantic_class(value: object) -> str:
    text = str(value).strip().upper()
    if text.startswith("+") or any(token in text for token in ("LONG", "PASS", "AKTİF", "SAĞLIKLI", "BAŞARILI", "KÂR", "YEŞİL", " ON")):
        return "is-positive"
    if text.startswith("-") or any(token in text for token in ("SHORT", "BLOCKED", "ZARAR", "BAŞARISIZ", "KRİTİK", "KIRMIZI", "SİL")):
        return "is-negative"
    if any(token in text for token in ("UYARI", "WARNING", "BEKLEYEN", "KUYRUKTA", "YÜKSEK", "OFF")):
        return "is-warning"
    if any(token in text for token in ("AÇIK", "BİLGİ", "PAPER", "DEĞİŞİM", "GİRİŞ")):
        return "is-info"
    return ""


def section_header(title: str, meta: str = "") -> str:
    suffix = f"<small>{escape(meta)}</small>" if meta else ""
    return f'<header class="section-header"><h2>{escape(title)}</h2>{suffix}</header>'


def badge(label: str, tone: str = "neutral") -> str:
    return f'<span class="badge badge-{escape(tone)}">{escape(label)}</span>'


def display_button(label: str, tone: str = "neutral", active: bool = False, css_class: str = "") -> str:
    state = " is-active" if active else ""
    return (
        f'<button class="display-button tone-{escape(tone)}{state} {escape(css_class)}" '
        f'data-ui-intent="display-only" aria-disabled="true" disabled>{escape(label)}</button>'
    )


def toggle(label: str = "", enabled: bool = False) -> str:
    state = "ON" if enabled else "OFF"
    return f'<span class="toggle" data-state="{state}" data-ui-intent="display-only"><b>{escape(label)}</b><i>{state}</i></span>'


def status_dot(label: str, state: str = "ok", value: str = "") -> str:
    metric = f"<strong>{escape(value)}</strong>" if value else ""
    return f'<span class="status-dot status-{escape(state)}"><i></i><b>{escape(label)}</b>{metric}</span>'


def mini_value_row(label: str, value: str, tone: str = "") -> str:
    css = tone or semantic_class(value)
    return f'<div class="mini-value-row"><span>{escape(label)}</span><strong class="{escape(css)}">{escape(value)}</strong></div>'


def panel(title: str, content: str, css_class: str = "", meta: str = "") -> str:
    return f'<section class="cc-panel {escape(css_class)}">{section_header(title, meta)}<div class="panel-body">{content}</div></section>'


def metric_card(title: str, value: str, sub: str = "", tone: str = "", icon: str = "") -> str:
    css = tone or semantic_class(value)
    icon_html = f'<span class="metric-icon">{escape(icon)}</span>' if icon else ""
    return f'<article class="metric-card"><div><small>{escape(title)}</small><strong class="{escape(css)}">{escape(value)}</strong><span>{escape(sub)}</span></div>{icon_html}</article>'


def table(headers: Sequence[str], rows: Iterable[Sequence[object]], css_class: str = "", action_last: bool = False) -> str:
    head = "".join(f"<th>{escape(str(item))}</th>" for item in headers)
    rendered = []
    for row in rows:
        cells = []
        for index, item in enumerate(row):
            if action_last and index == len(row) - 1:
                cells.append(f'<td>{display_button(str(item), "danger", css_class="table-action")}</td>')
            else:
                cells.append(f'<td class="{semantic_class(item)}">{escape(str(item))}</td>')
        rendered.append("<tr>" + "".join(cells) + "</tr>")
    return f'<table class="cc-table {escape(css_class)}"><thead><tr>{head}</tr></thead><tbody>{"".join(rendered)}</tbody></table>'


def scroll_container(content: str, label: str, css_class: str = "") -> str:
    return f'<div class="scroll-container {escape(css_class)}" aria-label="{escape(label)}">{content}</div>'


def kv_list(rows: Iterable[tuple[str, str]], css_class: str = "") -> str:
    return f'<div class="kv-list {escape(css_class)}">' + "".join(mini_value_row(k, v) for k, v in rows) + "</div>"


def progress(label: str, value: int, color: str = "green", meta: str = "") -> str:
    return f'<div class="progress-row"><div><span>{escape(label)}</span><b>{escape(meta or str(value) + "%")}</b></div><div class="progress-track"><i class="bar-{escape(color)}" style="width:{max(0,min(value,100))}%"></i></div></div>'


def donut(segments: Sequence[tuple[str, int, str]], center: str = "") -> str:
    total = max(sum(v for _, v, _ in segments), 1)
    cursor = 0.0
    stops, legend = [], []
    for label, value, color in segments:
        start = cursor
        cursor += value / total * 100
        stops.append(f"{color} {start:.2f}% {cursor:.2f}%")
        legend.append(f'<li><i style="background:{escape(color)}"></i><span>{escape(label)}</span><b>{value} ({value/total*100:.1f}%)</b></li>')
    return '<div class="donut-wrap"><div class="donut" style="background:conic-gradient(' + ",".join(stops) + f')"><span>{escape(center)}</span></div><ul class="donut-legend">{"".join(legend)}</ul></div>'


def line_chart(series: Sequence[Sequence[int]], colors: Sequence[str], labels: Sequence[str] = ()) -> str:
    paths = []
    width, height = 640, 210
    for values, color in zip(series, colors):
        if not values:
            continue
        max_v, min_v = max(values), min(values)
        spread = max(max_v - min_v, 1)
        points = " ".join(f"{i*(width/(len(values)-1)):.1f},{height-((v-min_v)/spread*(height-30)+15):.1f}" for i, v in enumerate(values))
        paths.append(f'<polyline points="{points}" fill="none" stroke="{escape(color)}" stroke-width="3"/>')
    legend = "".join(f'<span><i style="background:{escape(color)}"></i>{escape(label)}</span>' for label, color in zip(labels, colors))
    return f'<div class="chart"><div class="chart-legend">{legend}</div><svg viewBox="0 0 {width} {height}" preserveAspectRatio="none"><g class="chart-grid"><path d="M0 42H640M0 84H640M0 126H640M0 168H640"/></g>{"".join(paths)}</svg></div>'


def bar_chart(values: Sequence[int], colors: Sequence[str] | None = None, labels: Sequence[str] = ()) -> str:
    max_v = max((abs(v) for v in values), default=1)
    bars = []
    for i, value in enumerate(values):
        color = colors[i] if colors else ("#48bd67" if value >= 0 else "#e34f49")
        height = max(6, abs(value) / max_v * 85)
        bars.append(f'<div class="bar-item"><b class="{semantic_class(value)}">{value:+d}</b><i style="height:{height}%;background:{escape(color)}"></i><span>{escape(labels[i] if i < len(labels) else str(i+1))}</span></div>')
    return f'<div class="bar-chart">{"".join(bars)}</div>'


def report_tabs(active_key: str) -> str:
    from .data import REPORT_TABS, SCREEN_BY_KEY
    return '<nav class="report-tabs">' + "".join(f'<a class="{"active" if key == active_key else ""}" href="{escape(SCREEN_BY_KEY[key].output_file)}">{escape(label)}</a>' for label, key in REPORT_TABS) + "</nav>"


def field(label: str, value: str, css_class: str = "") -> str:
    return f'<label class="display-field"><span>{escape(label)}</span><b class="{escape(css_class)}">{escape(value)}</b></label>'


def action_stack(labels: Sequence[tuple[str, str]]) -> str:
    return '<div class="action-stack">' + "".join(display_button(label, tone) for label, tone in labels) + "</div>"
