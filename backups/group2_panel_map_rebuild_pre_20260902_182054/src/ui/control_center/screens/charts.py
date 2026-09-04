"""06_GRAFIKLER: reference-aligned, display-only market workspace."""

from __future__ import annotations

from ..components import display_button, field, kv_list, panel, scroll_container, table
from ..layout import render_screen


def _toolbar() -> str:
    return (
        '<div class="group2-toolbar" aria-label="Grafik kontrol satırı">'
        + field("SEMBOL", "BTC/USDT")
        + field("ZAMAN ARALIĞI", "1H")
        + field("GÖSTERGELER", "T3 (6), DMI/ADX (24)")
        + '<span class="toolbar-spacer"></span>'
        + display_button("GÖSTERGE AYARLARI  ⚙", "neutral")
        + "</div>"
    )


def _market_workspace() -> str:
    candles = []
    volumes = []
    for index in range(72):
        direction = "down" if index % 7 in (0, 1) else "up"
        height = 14 + (index * 17) % 38
        bottom = 42 + (index * 13) % 116
        left = 1.4 + index * 1.36
        candles.append(
            f'<i class="group2-candle {direction}" '
            f'style="left:{left:.2f}%;height:{height}px;bottom:{bottom}px"></i>'
        )
        volumes.append(
            f'<i class="group2-volume {direction}" '
            f'style="left:{left:.2f}%;height:{10 + (index * 19) % 42}px"></i>'
        )

    slope_bars = []
    for index in range(52):
        positive = index % 13 < 8
        height = 7 + (index * 9) % 31
        slope_bars.append(
            f'<i class="group2-volume {"up" if positive else "down"}" '
            f'style="left:{1.4 + index * 1.86:.2f}%;height:{height}px"></i>'
        )

    tools = "".join(f"<span>{icon}</span>" for icon in ("＋", "╱", "⌁", "◇", "▦", "T", "☺", "⌕", "∿", "⌁", "⌫"))
    price_axis = "".join(f"<span>{price:,}.00</span>" for price in (72000, 70000, 68000, 66000, 64000, 62000, 60000, 58000))
    times = "".join(f"<span>{label}</span>" for label in ("10 May", "12 May", "14 May", "16 May", "18 May", "19 May", "12:00"))
    return (
        '<div class="group2-chart-shell" aria-label="BTC USDT teknik analiz grafiği">'
        '<div class="group2-chart-head"><b>BTC/USDT · 1H · BINANCE USDT-M FUTURES</b>'
        '<span class="ohlc">A 68,102.45 &nbsp; Y 68,420.00 &nbsp; D 67,853.10 &nbsp; K 68,302.54 &nbsp; +200.09 (+0.29%)</span></div>'
        f'<div class="group2-drawing-tools" aria-label="Grafik araçları">{tools}</div>'
        '<div class="group2-market-stack">'
        '<div class="group2-price-stage"><span class="group2-band-label">Hacim 2.35K</span>'
        + "".join(candles)
        + '<svg viewBox="0 0 1000 300" preserveAspectRatio="none" aria-hidden="true">'
        '<polyline points="0,205 42,214 78,201 116,220 154,188 192,202 230,162 268,151 306,139 344,126 382,145 420,133 458,190 496,212 534,225 572,183 610,161 648,120 686,132 724,153 762,108 800,101 838,126 876,111 914,80 952,96 1000,104" fill="none" stroke="#34b961" stroke-width="7" opacity=".24"/>'
        '<polyline points="0,205 42,214 78,201 116,220 154,188 192,202 230,162 268,151 306,139 344,126 382,145 420,133 458,190 496,212 534,225 572,183 610,161 648,120 686,132 724,153 762,108 800,101 838,126 876,111 914,80 952,96 1000,104" fill="none" stroke="#45ce70" stroke-width="3"/>'
        '<polyline points="0,214 42,221 78,211 116,228 154,201 192,214 230,178 268,168 306,156 344,142 382,159 420,150 458,203 496,221 534,238 572,198 610,178 648,137 686,148 724,168 762,123 800,116 838,141 876,126 914,97 952,112 1000,112" fill="none" stroke="#287d47" stroke-width="2"/>'
        '</svg>'
        '<span class="group2-chart-marker sell" style="left:19%;top:52%">S</span>'
        '<span class="group2-chart-marker buy" style="left:23%;top:70%">B</span>'
        '<span class="group2-chart-marker sell" style="left:67%;top:30%">S</span>'
        '<span class="group2-chart-marker buy" style="left:66%;top:58%">B</span>'
        '<span class="group2-chart-marker sell" style="left:86%;top:19%">S</span>'
        f'<div class="group2-price-axis">{price_axis}</div></div>'
        '<div class="group2-volume-stage"><span class="group2-band-label">HACİM</span>'
        + "".join(volumes)
        + "</div>"
        '<div class="group2-indicator-stage"><span class="group2-band-label">DMI / ADX (24) &nbsp; '
        '<b class="is-positive">+DI 28.4</b> &nbsp; <b class="is-negative">-DI 14.9</b> &nbsp; <b class="is-warning">ADX 23.7</b></span>'
        '<svg viewBox="0 0 1000 160" preserveAspectRatio="none" aria-hidden="true">'
        '<polyline points="0,100 42,91 84,106 126,82 168,108 210,67 252,76 294,56 336,88 378,79 420,96 462,68 504,111 546,85 588,100 630,77 672,93 714,70 756,94 798,54 840,72 882,55 924,76 966,63 1000,49" fill="none" stroke="#49b657" stroke-width="3"/>'
        '<polyline points="0,75 42,83 84,103 126,85 168,105 210,74 252,98 294,104 336,67 378,80 420,98 462,72 504,109 546,76 588,101 630,103 672,83 714,68 756,89 798,64 840,88 882,52 924,72 966,58 1000,84" fill="none" stroke="#df4239" stroke-width="3"/>'
        '<polyline points="0,117 42,103 84,96 126,108 168,91 210,66 252,43 294,38 336,82 378,70 420,48 462,66 504,92 546,70 588,62 630,63 672,84 714,96 756,74 798,43 840,61 882,75 924,52 966,66 1000,58" fill="none" stroke="#e2b515" stroke-width="3"/>'
        "</svg></div>"
        '<div class="group2-volume-stage"><span class="group2-band-label">ADX SLOPE (N=6) &nbsp; <b class="is-positive">+2.10</b></span>'
        + "".join(slope_bars)
        + f'<div class="group2-time-axis">{times}</div></div>'
        "</div></div>"
    )


def _right_rail() -> str:
    selected_coin = panel(
        "SEÇİLİ COİN ÖZETİ",
        kv_list(
            (
                ("Sembol", "BTC/USDT"), ("Fiyat (USDT)", "68,302.54"),
                ("24H Hacim", "2.35B"), ("Yön", "LONG"),
                ("T3 Entry Mode", "DEVAM"), ("T3 Renk", "YEŞİL"),
                ("+DI / -DI", "28.4 / 14.9"), ("ADX (24)", "23.7"),
                ("ADX Slope (N=6)", "+2.10"), ("Sinyal", "STRONG"),
                ("Son Sinyal", "LONG"), ("Son Sinyal Zamanı", "19.05.2026 18:56"),
                ("Strateji", "EMA Model Trade v1.6"),
            )
        ),
        "fill",
    )
    strategy = panel(
        "STRATEJİ ÖZETİ",
        kv_list(
            (
                ("T3 Entry Mode", "DEVAM"), ("ADX Slope", "ON (N=6)"),
                ("Volume Filter", "ON (> 5M USDT)"), ("Stop Loss", "ON (%2)"),
                ("Closed Candle", "1H"), ("UI Refresh", "2 dk"),
                ("T3 Factor", "0.7"), ("T3 Period", "4"),
                ("DMI Length", "24"), ("ADX Smoothing", "24"),
                ("ADX Threshold", "20"), ("Max Coin", "5"), ("Leverage", "1x"),
            )
        ),
        "fill",
    )
    trend = panel(
        "T3 GÖSTERGE · TREND MODE",
        '<div class="screen-grid grid-2">'
        + kv_list((("T3 RENK DURUMU", "YEŞİL"), ("DEVAM MODE", "Trend Devam Ediyor")))
        + kv_list((("T3 FACTOR", "0.7"), ("KARAR", "CLOSED CANDLE")))
        + "</div>",
        "fill",
    )
    position = panel(
        "AÇIK POZİSYON BİLGİSİ",
        kv_list(
            (
                ("Yön", "LONG"), ("Giriş Fiyatı", "68,102.45"),
                ("Miktar", "0.0321 BTC"), ("Yatırım", "2,195.68 USDT"),
                ("Güncel Fiyat", "68,302.54"), ("PnL (USDT)", "+6.42 (+0.29%)"),
                ("Stop Loss (%2)", "66,936.49"), ("Kâr Hedefi", "70,390.62"),
                ("Süre", "1H 42m"),
            )
        )
        + display_button("POZİSYONU KAPAT · UIINTENT", "danger"),
        "fill",
    )
    return f'<aside class="group2-chart-rail">{selected_coin}{strategy}{trend}{position}</aside>'


def _bottom_panels() -> str:
    time_buttons = "".join(display_button(label, "info" if label == "1H" else "neutral", label == "1H") for label in ("15m", "30m", "1H", "2H", "4H", "6H", "12H", "1D"))
    tools = "".join(display_button(label, "neutral") for label in ("↖", "╱", "⌁", "◇", "▦", "T", "SIFIRLA"))
    indicators = "".join(f"<label><i></i>{label}</label>" for label in ("T3 (6)", "DMI / ADX (24)", "ADX Slope (N=6)", "Hacim"))
    upper = (
        '<div class="group2-chart-bottom-a">'
        + panel("ZAMAN ARALIĞI HIZLI GEÇİŞ", f'<div class="group2-inline-buttons">{time_buttons}</div>', "fill")
        + panel("GRAFİK ARAÇLARI", f'<div class="group2-tool-grid">{tools}</div>', "fill")
        + panel("GÖSTERGE KONTROLÜ", f'<div class="group2-indicator-grid">{indicators}</div>', "fill", "display-only")
        + "</div>"
    )
    events = panel(
        "GRAFİK OLAY AKIŞI",
        scroll_container(
            table(
                ("ZAMAN", "SEMBOL", "OLAY", "DETAY"),
                (
                    ("19:42:16", "BTC/USDT", "GRAFİK YENİLENDİ", "1H kapanış verisi işlendi"),
                    ("19:41:58", "BTC/USDT", "T3 DEVAM", "T3 yeşil devam"),
                    ("19:41:47", "BTC/USDT", "LONG SİNYAL", "Yeni LONG sinyali üretildi"),
                    ("19:40:34", "BTC/USDT", "ADX SLOPE UP", "ADX slope +2.10"),
                    ("19:40:18", "BTC/USDT", "HACİM GÜNCELLENDİ", "1H hacim 2.35K"),
                ),
                "dense",
            ),
            "Grafik olay akışı",
            "group2-scroll",
        ),
        "fill",
        "SON 20",
    )
    values = panel(
        "GÖSTERGE DEĞERLERİ",
        table(
            ("GÖSTERGE", "DEĞER"),
            (("T3 (6)", "68,104.21"), ("+DI (24)", "28.4"), ("-DI (24)", "14.9"), ("ADX (24)", "23.7"), ("ADX Slope", "+2.10"), ("Hacim (1H)", "2.35K")),
            "dense",
        ),
        "fill",
        "ANLIK",
    )
    notes = panel(
        "HIZLI NOTLAR",
        '<div class="group2-note info">T3 yeşil devam modunda.<br>+DI &gt; -DI ve ADX 20 üzeri.<br>Trend gücü yeterli.<br>Sinyal üretimi closed candle ile devam ediyor.</div>',
        "fill",
    )
    return upper + f'<div class="group2-chart-bottom-b">{events}{values}{notes}</div>'


def render_charts_screen(model=None) -> str:
    body = _toolbar() + f'<div class="group2-chart-main">{_market_workspace()}{_right_rail()}</div>' + _bottom_panels()
    return render_screen(
        "GRAFİKLER",
        "Grafikler",
        body,
        "Teknik analiz çalışma alanı · display-only",
        "group2-screen group2-chart-screen",
    )
