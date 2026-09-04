"""07_STRATEJI: reference-aligned, display-only strategy management screen."""

from __future__ import annotations

from html import escape

from ..components import display_button, kv_list, panel, table
from ..layout import render_screen


def _choice(left: str, right: str, selected: str = "left") -> str:
    return (
        '<div class="group2-option-row">'
        + display_button(left, "info" if selected == "left" else "neutral", selected == "left")
        + display_button(right, "info" if selected == "right" else "neutral", selected == "right")
        + "</div>"
    )


def _stepper(label: str, value: str, note: str = "") -> str:
    suffix = f"<small>{escape(note)}</small>" if note else ""
    return (
        f'<div class="group2-field"><span>{escape(label)}</span>'
        f'<div class="group2-stepper"><b>{escape(value)}</b>'
        + display_button("−", "neutral")
        + display_button("+", "neutral")
        + f"</div>{suffix}</div>"
    )


def _checks(items: tuple[tuple[str, str], ...]) -> str:
    return '<ul class="group2-checks">' + "".join(
        f'<li><b class="{tone}">{escape(label)}</b></li>' for label, tone in items
    ) + "</ul>"


def _management_bar() -> str:
    return panel(
        "STRATEJİ YÖNETİMİ",
        '<div class="group2-toolbar" style="height:100%;border:0;padding:0">'
        '<div class="group2-note" style="border:0;background:transparent;padding:0">'
        'Tüm parametreler yalnız yeni giriş adaylarını etkiler. Açık pozisyonlar etkilenmez.</div>'
        '<span class="toolbar-spacer"></span>'
        '<span>Strateji Profili</span><span class="display-field"><b>EMA Model Trade v1.6⌄</b></span>'
        + display_button("KAYDET", "info")
        + display_button("FARKLI KAYDET", "neutral")
        + display_button("SIFIRLA", "danger")
        + "</div>",
        "compact group2-strategy-management",
        "DISPLAY-ONLY · CONFIG MUTATION YOK",
    )


def _parameter_cards() -> str:
    t3 = panel(
        "1. T3 TREND FİLTRESİ",
        '<div class="group2-field"><span>T3 Entry Mode</span>'
        + _choice("DEĞİŞİM", "DEVAM", "left")
        + "</div>"
        '<div class="group2-note info"><b>DEĞİŞİM:</b> Fiyat T3 yönüne geçtiğinde sinyal üretir.<br>'
        '<b>DEVAM:</b> Fiyat T3 yönünde kaldığı sürece sinyal üretir.</div>'
        + _stepper("T3 Period", "6")
        + '<div class="group2-field"><span>T3 Renk Kriteri</span>'
        + _checks((("YEŞİL (LONG)", "is-positive"), ("KIRMIZI (SHORT)", "is-negative")))
        + "</div>",
        "fill group2-parameter-card group2-strategy-parameter t3-card",
        "?",
    )
    dmi = panel(
        "2. DMI / ADX TREND FİLTRESİ",
        '<div class="group2-field"><span>+DI / -DI Yön</span>'
        + _checks((("LONG: +DI > -DI", "is-positive"), ("SHORT: -DI > +DI", "is-negative")))
        + "</div>"
        + _stepper("ADX Threshold", "20")
        + '<div class="group2-field"><span>ADX Slope Filter</span>'
        + _choice("ON", "OFF", "left")
        + "</div>"
        + _stepper("ADX Slope N (mum)", "6")
        + '<div class="group2-field"><span>ADX Slope Kriteri</span><small>Yukarı eğim pozitif olmalı.</small></div>',
        "fill group2-parameter-card group2-strategy-parameter dmi-card",
        "?",
    )
    volume = panel(
        "3. HACİM FİLTRESİ",
        '<div class="group2-field"><span>Volume Filter</span>'
        + _choice("ON", "OFF", "left")
        + "</div>"
        + _stepper("Minimum 24H Hacim", "5,000,000 USDT")
        + '<div class="group2-field"><span>Hacim Kaynağı</span><div class="display-field"><b>Binance USDT-M Futures⌄</b></div></div>'
        + '<div class="group2-field"><span>Hacim Güncellik</span><div class="group2-note info"><b class="is-positive">PASS</b> &nbsp; (&lt; 15 dk)</div></div>'
        + '<div class="group2-note">Hacim filtresi yalnız closed-candle aday değerlendirmesinde okunur.</div>',
        "fill group2-parameter-card group2-strategy-parameter volume-card",
        "?",
    )
    risk = panel(
        "4. RİSK & GİRİŞ KURALLARI",
        _stepper("Max Coin (Eşzamanlı)", "5")
        + _stepper("Coin Başı Allocation", "200 USDT")
        + '<div class="group2-field"><span>Leverage</span><div class="display-field"><b>1x⌄</b></div></div>'
        + '<div class="group2-field"><span>Stop Loss</span>'
        + _choice("ON", "OFF", "left")
        + "</div>"
        + _stepper("Stop Loss Oranı", "% 2")
        + '<div class="group2-note warning"><b>Closed Candle Kuralı</b><br>1H kapanışı olmadan sinyal üretimi yapılmaz.</div>',
        "fill group2-parameter-card group2-strategy-parameter risk-card",
        "?",
    )
    return f'<div class="screen-grid group2-strategy-top" data-reference-screen="07_STRATEJI">{t3}{dmi}{volume}{risk}</div>'


def _signal_flow() -> str:
    long_rules = (
        '<div class="group2-flow-column is-positive"><div class="group2-flow-title">LONG KURALLARI</div>'
        '<div class="group2-flow-node">T3: DEĞİŞİM veya DEVAM</div><div class="group2-flow-node">+DI &gt; -DI</div>'
        '<div class="group2-flow-node">ADX ≥ 20</div><div class="group2-flow-node">ADX Slope (N=6) Yukarı</div>'
        '<div class="group2-flow-node">24H Hacim ≥ 5M USDT</div><div class="group2-flow-arrow">↓</div>'
        '<div class="group2-flow-title">LONG SİNYAL</div></div>'
    )
    chain = (
        '<div class="group2-flow-column"><div class="group2-flow-node">T3 Trend</div>'
        '<div class="group2-flow-node">DMI Yön</div><div class="group2-flow-node">ADX Seviyesi</div>'
        '<div class="group2-flow-node">ADX Slope</div><div class="group2-flow-node">Hacim Filtresi</div></div>'
    )
    short_rules = (
        '<div class="group2-flow-column is-negative"><div class="group2-flow-title">SHORT KURALLARI</div>'
        '<div class="group2-flow-node">T3: DEĞİŞİM veya DEVAM</div><div class="group2-flow-node">-DI &gt; +DI</div>'
        '<div class="group2-flow-node">ADX ≥ 20</div><div class="group2-flow-node">ADX Slope (N=6) Yukarı</div>'
        '<div class="group2-flow-node">24H Hacim ≥ 5M USDT</div><div class="group2-flow-arrow">↓</div>'
        '<div class="group2-flow-title">SHORT SİNYAL</div></div>'
    )
    return panel("SİNYAL ÜRETİM KURALLARI", f'<div class="group2-flow">{long_rules}{chain}{short_rules}</div>', "fill group2-strategy-flow-panel", "CLOSED CANDLE")


def _signal_states() -> str:
    rows = (
        ("#76df45", "LONG", "Tüm LONG kuralları sağlandı."),
        ("#ff5148", "SHORT", "Tüm SHORT kuralları sağlandı."),
        ("#c7bca9", "NO SIGNAL", "Kuralların tamamı sağlanmadı."),
        ("#ff5148", "BLOCKED", "Risk veya güvenlik kısıtı."),
        ("#ffb81c", "WATCH", "Kısmi filtre, izleme listesinde."),
    )
    content = '<div class="group2-state-list">' + "".join(
        f'<div class="group2-state"><i style="background:{color}"></i><b>{name}</b><span>{text}</span></div>'
        for color, name, text in rows
    ) + "</div>"
    return panel("SİNYAL DURUMLARI", content, "fill group2-strategy-states-panel", "AÇIKLANABİLİR KARAR")


def _change_rule() -> str:
    return panel(
        "STRATEJİ DEĞİŞİKLİK KURALI",
        '<div class="group2-note info">Strateji değişikliği mevcut açık pozisyonları etkilemez.<br><br>'
        'Değişiklikler yalnız sonraki 1H kapanışından itibaren yeni tarama ve yeni entry adaylarını etkiler.</div>'
        + kv_list((("SON DEĞİŞİKLİK", "19.05.2026 19:30:12"), ("Değiştiren", "Kullanıcı"), ("Açıklama", "ADX Slope ON (N=6)"))),
        "fill group2-strategy-change-panel",
        "OPEN POSITION IMMUTABLE",
    )


def _right_rail() -> str:
    summary = panel(
        "STRATEJİ ÖZETİ",
        kv_list(
            (
                ("T3 Entry Mode", "DEĞİŞİM"), ("T3 Period", "6"),
                ("T3 Renk", "YEŞİL / KIRMIZI"), ("+DI / -DI Yön", "AKTİF"),
                ("ADX Threshold", "20"), ("ADX Slope", "ON (N=6)"),
                ("Volume Filter (24H)", "ON (> 5M USDT)"), ("Max Coin", "5"),
                ("Allocation / Coin", "200 USDT"), ("Leverage", "1x"),
                ("Stop Loss", "ON (%2)"), ("Closed Candle", "1H"),
                ("UI Refresh", "2 dk"), ("Strateji Sürümü", "v1.6"),
            )
        ),
        "fill group2-strategy-summary",
    )
    ready = panel(
        "HAZIR STRATEJİLER",
        table(
            ("PROFİL", "DURUM"),
            (("EMA Model Trade v1.6", "AKTİF"), ("Trend Following v1.2", "BEKLEYEN"), ("Breakout Scout v1.1", "BEKLEYEN"), ("Scalp ShortTerm v1.0", "BEKLEYEN")),
            "dense",
        ),
        "fill group2-strategy-ready",
    )
    actions = panel(
        "STRATEJİ YÖNETİMİ",
        '<div class="group2-actions">'
        + display_button("YENİ STRATEJİ OLUŞTUR", "info")
        + display_button("STRATEJİYİ KOPYALA", "neutral")
        + display_button("STRATEJİYİ SİL", "danger")
        + "</div>",
        "compact group2-strategy-actions",
        "TÜMÜ DISABLED",
    )
    return f'<aside class="stack fill">{summary}{ready}{actions}</aside>'


def render_strategy_screen(model=None) -> str:
    lower = f'<div class="group2-strategy-main" data-layout="isolated-panel-coordinate"><div class="group2-strategy-content">{_signal_flow()}{_signal_states()}{_change_rule()}</div>{_right_rail()}</div>'
    body = (
        '<div class="group2-panel-map group2-strategy-map" data-panel-map="07_STRATEJI">'
        + _management_bar() + _parameter_cards() + lower + "</div>"
    )
    return render_screen(
        "STRATEJİ",
        "Strateji",
        body,
        "Parametre ve sinyal kural görünümü · direct apply yok",
        "group2-screen group2-strategy-screen",
    )
