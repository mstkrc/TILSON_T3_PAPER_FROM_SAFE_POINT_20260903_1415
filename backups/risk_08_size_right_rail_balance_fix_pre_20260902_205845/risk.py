"""08_RISK: reference-aligned, display-only risk operations screen."""

from __future__ import annotations

from html import escape

from ..components import bar_chart, display_button, kv_list, line_chart, panel, progress, table
from ..layout import render_screen


def _risk_card(title: str, value: str, sub: str, detail: str, gauge: int | None = None, tone: str = "") -> str:
    gauge_html = ""
    if gauge is not None:
        color = "#55be64" if gauge < 30 else "#f2ad16"
        gauge_html = f'<i class="group2-gauge" style="--gauge-value:{gauge}%;--gauge-color:{color}"></i>'
    return (
        '<article class="cc-panel group2-risk-card">'
        f'<h3>{escape(title)}</h3><strong class="{escape(tone)}">{escape(value)}</strong>'
        f'<p>{escape(sub)}</p><p>{escape(detail)}</p>{gauge_html}</article>'
    )


def _top_metrics() -> str:
    cards = (
        _risk_card("PORTFÖY RİSK KULLANIMI", "24.15%", "200 USDT / 829.01 USDT", "Kullanılabilir Risk 629.01 USDT", 24, "is-positive"),
        _risk_card("GÜNLÜK RİSK KULLANIMI", "18.32%", "151.67 USDT / 829.01 USDT", "Günlük Limit 300 USDT", 18, "is-warning"),
        _risk_card("TOPLAM AÇIK POZİSYON RİSKİ", "201.24 USDT", "24.15%", "Max Risk Limiti 829.01 USDT", None, "is-positive"),
        _risk_card("MAKS. TEK POZİSYON RİSKİ", "66.94 USDT", "8.06%", "Kural Limiti 100 USDT", None, "is-positive"),
        _risk_card("RİSK / REWARD ORT.", "2.31", "Ağırlıklı Ortalama", "Açık pozisyonlar", None, ""),
        _risk_card("HESAP ÖZETİ", "1,268.32 USDT", "Özsermaye (Equity) 1,324.18", "Kullanılabilir Bakiye 8,642.10", None, ""),
    )
    return '<div class="group2-risk-top">' + "".join(cards) + "</div>"


def _position_risk_table() -> str:
    rows = (
        ("1", "BTC/USDT", "LONG", "68,302.54", "0.0321", "66.94", "8.06%", "66,936.49", "70,390.62", "2.15", "AÇIK"),
        ("2", "ETH/USDT", "LONG", "2,604.18", "0.2100", "56.23", "6.78%", "2,552.10", "2,761.35", "2.02", "AÇIK"),
        ("3", "SOL/USDT", "SHORT", "178.45", "4.2500", "31.22", "3.77%", "182.02", "167.30", "1.88", "AÇIK"),
        ("4", "XRP/USDT", "LONG", "0.5265", "1,400", "20.14", "2.42%", "0.5160", "0.5370", "1.64", "AÇIK"),
        ("5", "MATIC/USDT", "SHORT", "0.4915", "2,000", "18.41", "2.22%", "0.5013", "0.4768", "1.63", "AÇIK"),
        ("6", "DOT/USDT", "LONG", "6.24", "6.42", "8.30", "1.00%", "6.00", "6.80", "1.80", "AÇIK"),
    )
    return panel(
        "AÇIK POZİSYON RİSK DAĞILIMI",
        table(("#", "SEMBOL", "YÖN", "GİRİŞ FİYATI", "MİKTAR", "RİSK USDT", "RİSK %", "STOP LOSS", "KÂR HEDEFİ", "R:R", "DURUM"), rows, "dense"),
        "fill",
    )


def _risk_timeline() -> str:
    return panel(
        "RİSK KULLANIM ZAMAN GRAFİĞİ",
        line_chart(
            ((24, 23, 22, 23, 22, 24, 25, 24, 26, 27, 26, 28, 29, 28, 30, 31, 30, 29, 31), (18, 17, 16, 17, 16, 18, 19, 18, 20, 21, 20, 22, 23, 22, 24, 25, 24, 23, 21), (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)),
            ("#63bd4d", "#f2ad16", "#e24b43"),
            ("Portföy Risk (%)", "Günlük Risk (%)", "Limit"),
        ),
        "fill",
        "SON 7 GÜN",
    )


def _daily_performance() -> str:
    summary = kv_list(
        (
            ("Bugünkü PnL (USDT)", "+52.43"), ("Bugünkü PnL (%)", "+4.21%"),
            ("Bugünkü İşlem Sayısı", "3"), ("Kârlı İşlem", "2 (66.67%)"),
            ("Zararlı İşlem", "1 (33.33%)"), ("En Büyük Kazanç", "+21.87 USDT"),
            ("En Büyük Zarar", "-8.64 USDT"), ("Ortalama Kazanç", "+21.25 USDT"),
            ("Profit Factor", "2.46"), ("Sharpe Ratio", "1.18"),
        )
    )
    chart = bar_chart((37, 52, 41, 21, -12, 19, 24), labels=("13", "14", "15", "16", "17", "18", "19"))
    return panel("GÜNLÜK PERFORMANS & RİSK", f'<div class="screen-grid grid-2 fill">{summary}{chart}</div>', "fill", "GÜNLÜK PnL · SON 7 GÜN")


def _correlation() -> str:
    labels = ("", "BTC", "ETH", "SOL", "XRP", "MATIC", "DOT")
    values = (
        ("BTC/USDT", "1.00", "0.62", "0.45", "0.38", "0.41", "0.34"),
        ("ETH/USDT", "0.62", "1.00", "0.55", "0.44", "0.46", "0.37"),
        ("SOL/USDT", "0.45", "0.55", "1.00", "0.48", "0.51", "0.42"),
        ("XRP/USDT", "0.38", "0.44", "0.48", "1.00", "0.56", "0.47"),
        ("MATIC", "0.41", "0.46", "0.51", "0.56", "1.00", "0.58"),
        ("DOT/USDT", "0.34", "0.37", "0.42", "0.47", "0.58", "1.00"),
    )
    cells = [f"<span>{escape(label)}</span>" for label in labels]
    for row in values:
        cells.append(f"<span>{escape(row[0])}</span>")
        for value in row[1:]:
            tone = "hot" if float(value) >= 0.70 else "warm" if float(value) >= 0.50 else ""
            cells.append(f'<span class="{tone}">{escape(value)}</span>')
    return panel(
        "POZİSYON KORELASYON MATRİSİ",
        '<div class="group2-correlation">' + "".join(cells) + '</div><div class="group2-note">0.70 üzeri korelasyon yüksek kabul edilir.</div>',
        "fill",
    )


def _risk_events() -> str:
    rows = (
        ("19:41:58", "Risk Limit Güncelleme", "BİLGİ", "Portföy risk 24.15%"),
        ("19:41:23", "Yeni Pozisyon Açıldı", "BİLGİ", "ETH/USDT LONG"),
        ("19:40:42", "Stop Loss Güncelleme", "BİLGİ", "BTC/USDT"),
        ("19:39:17", "Risk Kontrol", "PASS", "Tüm kontroller PASS"),
        ("19:38:05", "Günlük Risk Sınırı", "UYARI", "%60 seviyesine ulaştı"),
        ("19:35:50", "Pozisyon Boyutu", "BİLGİ", "XRP/USDT azaltıldı"),
        ("19:33:28", "Korelasyon Uyarısı", "UYARI", "MATIC/DOT korelasyon"),
        ("19:30:12", "Volatilite Artışı", "UYARI", "SOL/USDT volatilite ↑"),
    )
    return panel(
        "RİSK OLAYLARI",
        table(("ZAMAN", "OLAY", "SEVİYE", "AÇIKLAMA"), rows, "dense"),
        "fill",
        "SON 20",
    )


def _right_rail() -> str:
    limits = panel(
        "RİSK LİMİTLERİ",
        kv_list(
            (
                ("Portföy Risk Limit", "200 USDT · 24.15%"), ("Günlük Risk Limit", "300 USDT · 18.32%"),
                ("Max Tek Pozisyon Risk", "100 USDT · 8.06%"), ("Max Coin Limiti", "6 / 50"),
                ("Kaldıraç Limiti", "1x"), ("Min R/R Oranı", "1.50"),
                ("Günlük Zarar Limiti", "-10.00%"), ("Aylık Zarar Limiti", "-25.00%"),
            )
        ),
        "fill",
        "GLOBAL",
    )
    controls = panel(
        "POZİSYON RİSK KONTROLLERİ",
        kv_list(
            (
                ("Risk Hesaplama Metodu", "Sabit % (Equity)"), ("Stop Loss Zorunlu", "AKTİF"),
                ("Risk Limit Aşıldığında", "Yeni Girişleri Engelle"), ("Max Korelasyon", "3 Pozisyon"),
                ("Volatilite Koruması", "AKTİF"), ("News Koruması", "AKTİF"), ("Likidite Filtresi", "AKTİF"),
            )
        ),
        "fill",
    )
    actions = panel(
        "RİSK HIZLI AKSİYONLAR",
        '<div class="group2-actions">'
        + display_button("TÜM POZİSYONLARI KAPAT", "danger")
        + display_button("RİSKLERİ YENİDEN HESAPLA", "info")
        + display_button("STOP LOSS GÜNCELLE", "info")
        + display_button("BREAK EVEN'E TAŞI", "info")
        + display_button("YENİ GİRİŞLERİ DURDUR", "warning")
        + "</div>",
        "compact",
        "DISPLAY-ONLY",
    )
    emergency = panel(
        "ACİL DURDURMA",
        '<div class="group2-note danger">Tüm pozisyonları kapat ve yeni girişleri engelle. Bu ekranda execution bağlantısı yoktur.</div>'
        + display_button("ACİL DURDUR · UIINTENT", "danger"),
        "compact group2-emergency",
        "ÇİFT ONAY GEREKİR",
    )
    return f'<aside class="stack fill">{limits}{controls}{actions}{emergency}</aside>'


def render_risk_screen(model=None) -> str:
    middle = f'<div class="group2-risk-middle">{_position_risk_table()}{_risk_timeline()}</div>'
    lower = f'<div class="group2-risk-lower">{_daily_performance()}{_correlation()}{_risk_events()}</div>'
    body = (
        '<div class="group2-panel-map group2-risk-map" data-panel-map="08_RISK">'
        + '<div class="group2-risk-layout"><div class="group2-risk-left">'
        + _top_metrics() + f'<div class="group2-risk-main">{middle}{lower}</div>'
        + '</div>' + _right_rail() + '</div></div>'
    )
    return render_screen(
        "RİSK",
        "Risk",
        body,
        "Risk kullanımı, limitler ve güvenli aksiyon görünümü",
        "group2-screen group2-risk-screen",
    )
