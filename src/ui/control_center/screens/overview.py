"""Reference-aligned Control Center General Overview HTML renderer.

Rules:
- DOKUMANTASYON/CONTROL CENTER/ is the user-approved visual reference set.
- Fit the visible browser viewport at 100% zoom using 100vw / 100vh.
- No global page scroll.
- General Overview is the active paper operation cockpit.
- Start Readiness is not a General Overview panel.
- Market / Candidates detail table is not a General Overview panel; it belongs to Live Scan.
- Strategy Summary is the main decision-control panel.
- Paper-only / live-locked / no real order endpoint.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Iterable

from ..model import ControlCenterModel, build_control_center


OUTPUT_ENCODING = "utf-8"
REFERENCE_TARGET = "1920x1080"


def _td(values: Iterable[object]) -> str:
    return "".join(f"<td>{escape(str(v))}</td>" for v in values)


def _th(values: Iterable[object]) -> str:
    return "".join(f"<th>{escape(str(v))}</th>" for v in values)


def _tr(values: Iterable[object], raw_last: bool = False) -> str:
    items = list(values)
    if not raw_last or not items:
        return "<tr>" + _td(items) + "</tr>"
    safe = "".join(f"<td>{escape(str(v))}</td>" for v in items[:-1])
    return "<tr>" + safe + f"<td>{items[-1]}</td></tr>"


def _kv(label: str, value: str, cls: str = "") -> str:
    return (
        '<div class="kv">'
        f"<span>{escape(label)}</span>"
        f'<b class="{escape(cls)}">{escape(value)}</b>'
        "</div>"
    )


def _cmd(line1: str, line2: str, cls: str) -> str:
    return (
        f'<button class="cmd {escape(cls)}" disabled>'
        f"<span>{escape(line1)}</span>"
        f"<strong>{escape(line2)}</strong>"
        "</button>"
    )


def _status_dot(label: str, cls: str = "ok", value: str = "") -> str:
    metric = f"<strong>{escape(value)}</strong>" if value else ""
    return (
        '<div class="health-item">'
        f'<i class="{escape(cls)}"></i>'
        f"<span>{escape(label)}</span>"
        f"{metric}"
        "</div>"
    )


def _action_button(label: str) -> str:
    return (
        '<button class="row-action" data-ui-intent="display-only" '
        f'aria-label="{escape(label)} — yalnız görsel UIIntent" disabled>{escape(label)}</button>'
    )


def _display_control(label: str, cls: str = "", active: bool = False) -> str:
    state = " is-active" if active else ""
    return (
        f'<button class="display-control {escape(cls)}{state}" '
        f'data-ui-intent="display-only" disabled>{escape(label)}</button>'
    )


def _display_value(value: str) -> str:
    return f'<span class="display-value">{escape(value)}</span>'


def _position_row(values: Iterable[object]) -> str:
    items = [str(value) for value in values]
    cells: list[str] = []
    for index, value in enumerate(items[:-1]):
        cls = ""
        if index == 1:
            cls = "dir-long" if value == "LONG" else "dir-short"
        elif index in (5, 6):
            cls = "pnl-pos" if value.startswith("+") else "pnl-neg" if value.startswith("-") else ""
        cells.append(f'<td class="{cls}">{escape(value)}</td>')
    cells.append(f"<td>{items[-1]}</td>")
    return "<tr>" + "".join(cells) + "</tr>"


def _trade_history_row(values: Iterable[object]) -> str:
    items = [str(value) for value in values]
    cells: list[str] = []
    for index, value in enumerate(items):
        cls = ""
        if index == 2:
            cls = "dir-long" if value == "LONG" else "dir-short"
        elif index == 3:
            cls = {"AÇIK": "status-open", "ZARAR": "status-loss", "KAPAT": "status-closed"}.get(value, "")
        elif index in (4, 5):
            cls = "pnl-pos" if value.startswith("+") else "pnl-neg" if value.startswith("-") else ""
        cells.append(f'<td class="{cls}">{escape(value)}</td>')
    return "<tr>" + "".join(cells) + "</tr>"


def _event_row(values: Iterable[object]) -> str:
    items = [str(value) for value in values]
    cells: list[str] = []
    for index, value in enumerate(items):
        cls = ""
        if index == 4:
            cls = "dir-long" if value == "LONG" else "dir-short" if value == "SHORT" else ""
        elif index == 6:
            cls = {"GİRİŞ": "status-open", "KAPAT": "status-closed", "ZARAR": "status-loss"}.get(value, "")
        elif index == 8:
            cls = "pnl-pos" if value.startswith("+") else "pnl-neg" if value.startswith("-") else ""
        cells.append(f'<td class="{cls}">{escape(value)}</td>')
    return "<tr>" + "".join(cells) + "</tr>"


def _chart_svg() -> str:
    candles = [
        (28, 156, 132, "up"), (55, 142, 116, "up"), (82, 128, 138, "down"),
        (109, 126, 94, "up"), (136, 106, 72, "up"), (163, 78, 104, "down"),
        (190, 92, 64, "up"), (217, 70, 96, "down"), (244, 82, 58, "up"),
        (271, 56, 86, "down"), (298, 80, 112, "down"), (325, 108, 138, "down"),
        (352, 126, 92, "up"), (379, 102, 68, "up"), (406, 76, 56, "up"),
        (433, 62, 88, "down"), (460, 84, 108, "down"), (487, 102, 78, "up"),
        (514, 86, 62, "up"), (541, 70, 58, "up"), (568, 66, 80, "down"),
        (595, 76, 56, "up"), (622, 62, 50, "up"), (649, 58, 74, "down"),
        (676, 78, 60, "up"), (703, 68, 50, "up"), (730, 56, 72, "down"),
        (757, 76, 58, "up"), (784, 66, 48, "up"), (811, 54, 64, "down"),
    ]

    candle_svg: list[str] = []
    volume_svg: list[str] = []

    for idx, (x, open_y, close_y, direction) in enumerate(candles):
        color = "#42b965" if direction == "up" else "#dc554d"
        high = min(open_y, close_y) - 18
        low = max(open_y, close_y) + 18
        y = min(open_y, close_y)
        h = max(abs(close_y - open_y), 8)
        candle_svg.append(
            f'<line x1="{x}" y1="{high}" x2="{x}" y2="{low}" stroke="{color}" stroke-width="2"/>'
            f'<rect x="{x - 6}" y="{y}" width="12" height="{h}" rx="1" fill="{color}"/>'
        )
        vh = 18 + ((idx * 9) % 52)
        volume_svg.append(
            f'<rect x="{x - 7}" y="{270 - vh}" width="14" height="{vh}" fill="{color}" opacity=".82"/>'
        )

    grid_x = "".join(
        f'<line x1="{x}" y1="0" x2="{x}" y2="350" class="gridline"/>'
        for x in range(0, 861, 54)
    )
    grid_y = "".join(
        f'<line x1="0" y1="{y}" x2="860" y2="{y}" class="gridline"/>'
        for y in range(36, 340, 36)
    )

    return f"""
    <svg class="chart-svg" viewBox="0 0 860 350" preserveAspectRatio="none" aria-label="Display-only market chart">
      <defs>
        <linearGradient id="gridFade" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#0d2633"/>
          <stop offset="100%" stop-color="#061923"/>
        </linearGradient>
      </defs>

      <rect x="0" y="0" width="860" height="350" fill="url(#gridFade)"/>
      {grid_x}
      {grid_y}

      <polyline fill="none" stroke="#68b04f" stroke-width="3"
        points="28,156 82,128 136,104 190,88 244,72 298,84 352,108 406,76 460,88 514,74 568,92 622,76 676,64 730,66 784,56 838,60"/>

      {"".join(candle_svg)}

      <text x="330" y="58" class="sell">S</text>
      <polygon points="336,66 327,84 345,84" fill="#dc554d"/>
      <text x="462" y="148" class="buy">B</text>
      <polygon points="468,136 458,154 478,154" fill="#42b965"/>
      <text x="672" y="58" class="sell">S</text>
      <polygon points="678,66 669,84 687,84" fill="#dc554d"/>
      <text x="778" y="142" class="buy">B</text>
      <polygon points="784,130 774,148 794,148" fill="#42b965"/>

      <text x="770" y="95" class="price">68,302.54</text>
      <text x="770" y="130" class="axis">68,200</text>
      <text x="770" y="168" class="axis">68,000</text>
      <text x="770" y="206" class="axis">67,800</text>

      <line x1="0" y1="214" x2="860" y2="214" stroke="#263b49"/>
      <text x="12" y="238" class="chart-label">Hacim</text>
      {"".join(volume_svg)}
      <polyline fill="none" stroke="#2b9fc8" stroke-width="2"
        points="28,252 82,242 136,258 190,236 244,248 298,230 352,244 406,226 460,238 514,232 568,246 622,228 676,236 730,224 784,232 838,226"/>

      <line x1="0" y1="286" x2="860" y2="286" stroke="#263b49"/>
      <text x="12" y="314" class="chart-label">DMI / ADX</text>
      <polyline fill="none" stroke="#49c86a" stroke-width="2"
        points="126,314 172,306 218,318 264,300 310,308 356,296 402,304 448,310 494,298 540,304 586,294 632,302 678,296 724,300 790,294"/>
      <polyline fill="none" stroke="#ef5a50" stroke-width="2"
        points="126,330 172,322 218,326 264,318 310,324 356,320 402,330 448,322 494,324 540,316 586,322 632,328 678,320 724,326 790,322"/>
      <polyline fill="none" stroke="#d4a62e" stroke-width="2"
        points="126,322 172,318 218,314 264,316 310,310 356,312 402,308 448,306 494,310 540,304 586,306 632,302 678,304 724,300 790,302"/>

      <text x="170" y="344" class="axis">06:00</text>
      <text x="335" y="344" class="axis">09:00</text>
      <text x="500" y="344" class="axis">12:00</text>
      <text x="665" y="344" class="axis">15:00</text>
    </svg>
    """


def render_overview_screen(
    model: ControlCenterModel | None = None,
    output: str | Path | None = None,
) -> str:
    model = model or build_control_center()

    nav_items = [
        ("▦", "Genel Bakış"),
        ("⚡", "Canlı Tarama"),
        ("◎", "Sinyaller"),
        ("⬡", "Açık Pozisyonlar"),
        ("↺", "İşlem Geçmişi"),
        ("▥", "Grafikler"),
        ("◌", "Strateji"),
        ("⬟", "Risk"),
        ("♨", "Sistem Sağlığı"),
        ("▣", "Raporlar"),
        ("✉", "Bildirimler"),
    ]

    open_positions = [
        ("BTC/USDT", "LONG", "0.0321", "68,200.00", "68,302.54", "+102.54", "+1.82%", _action_button("KAPAT")),
        ("ETH/USDT", "LONG", "0.2100", "2,576.10", "2,604.18", "+61.78", "+1.95%", _action_button("KAPAT")),
        ("BNB/USDT", "LONG", "0.8400", "592.00", "596.20", "+18.32", "+0.88%", _action_button("KAPAT")),
        ("SOL/USDT", "SHORT", "4.2500", "178.45", "175.84", "-27.61", "-1.61%", _action_button("KAPAT")),
        ("ADA/USDT", "SHORT", "1.2500", "0.4985", "0.4951", "-8.64", "-0.63%", _action_button("KAPAT")),
        ("XRP/USDT", "LONG", "1.4000", "0.5250", "0.5265", "+2.10", "+0.40%", _action_button("KAPAT")),
        ("MATIC/USDT", "LONG", "0.8000", "0.4721", "0.4721", "+0.00", "0.00%", _action_button("KAPAT")),
        ("AVAX/USDT", "LONG", "2.0000", "37.21", "37.21", "+0.00", "0.00%", _action_button("KAPAT")),
        ("LINK/USDT", "SHORT", "5.0000", "14.80", "14.80", "+0.00", "0.00%", _action_button("KAPAT")),
        ("DOT/USDT", "LONG", "6.0000", "6.24", "6.24", "+0.00", "0.00%", _action_button("KAPAT")),
    ]

    trade_history = [
        ("19:42:18", "ETH/USDT", "LONG", "KAPAT", "+12.45", "+0.98%"),
        ("19:41:58", "SOL/USDT", "SHORT", "KAPAT", "+21.87", "+1.74%"),
        ("19:41:47", "BNB/USDT", "LONG", "KAPAT", "+8.32", "+0.63%"),
        ("19:41:33", "ADA/USDT", "SHORT", "ZARAR", "-8.64", "-0.63%"),
        ("19:41:21", "MATIC/USDT", "LONG", "KAPAT", "+6.71", "+0.51%"),
        ("19:41:09", "AVAX/USDT", "LONG", "KAPAT", "+7.12", "+0.55%"),
        ("19:40:55", "LINK/USDT", "SHORT", "KAPAT", "+5.21", "+0.42%"),
        ("19:40:42", "DOT/USDT", "LONG", "KAPAT", "+4.21", "+0.34%"),
        ("19:40:30", "XRP/USDT", "LONG", "KAPAT", "+6.05", "+0.49%"),
        ("19:40:18", "ETH/USDT", "LONG", "AÇIK", "—", "—"),
    ]

    event_rows = [
        ("19:42:23", "YAKLAŞAN SİNYAL", "GİRİŞ", "LTC/USDT", "LONG", "GİRİŞ", "—", "—", "—", "ADX 18.2 < 20, trend zayıf"),
        ("19:42:18", "YAKLAŞAN SİNYAL", "GİRİŞ", "ETH/USDT", "LONG", "GİRİŞ", "—", "—", "—", "ADX 27.4, DI+ > DI-, T3 ↑, Hacim OK"),
        ("19:41:58", "ÇIKIŞ", "ETH/USDT", "LONG", "LONG", "KAPAT", "2,604.18", "+21.87", "+21.87", "Hedef kâr seviyesi gerçekleşti"),
        ("19:41:47", "ÇIKIŞ", "SOL/USDT", "SHORT", "SHORT", "KAPAT", "178.45", "+8.32", "+8.32", "ADX 23.1, DI+ > DI-, T3 ↑"),
        ("19:41:33", "ÇIKIŞ", "BNB/USDT", "LONG", "LONG", "KAPAT", "596.20", "+8.32", "+8.32", "Stop-loss tetiklendi"),
        ("19:41:21", "GİRİŞ", "ADA/USDT", "SHORT", "SHORT", "RED", "0.4951", "-8.64", "-8.64", "ADX 25.6, DI- > DI+, T3 ↓"),
        ("19:41:09", "GİRİŞ", "MATIC/USDT", "LONG", "LONG", "GİRİŞ", "0.4721", "+6.71", "+6.71", "ADX 31.2, hacim güçlü"),
        ("19:40:55", "GİRİŞ", "AVAX/USDT", "LONG", "LONG", "GİRİŞ", "37.21", "+7.12", "+7.12", "Trailing stop ile çıkış"),
        ("19:40:42", "ÇIKIŞ", "LINK/USDT", "SHORT", "SHORT", "KAPAT", "14.80", "+5.21", "+5.21", "ADX 26.8, hacim OK"),
        ("19:40:30", "ÇIKIŞ", "DOT/USDT", "LONG", "LONG", "KAPAT", "6.24", "+4.21", "+4.21", "DI+ > DI-, T3 ↑"),
    ]

    strategy_rows = [
        ("Aktif Profil", "PAPER TRADE"),
        ("Aktif Strateji", "Tilson T3 + DMI/ADX"),
        ("Trade Mode", "LONG/SHORT"),
        ("Max Coin", "10"),
        ("Açık Coin", "5"),
        ("Kalan Coin Hakkı", "5"),
        ("Coin Başı Allocation", "100 USDT"),
        ("Cüzdan Kullanımı", "10%"),
        ("Kaldıraç", "10x"),
        ("Margin", "Isolated"),
        ("T3 Entry", "Color Change"),
        ("Continuation", "OFF"),
        ("T3 Faktörü", "0.7"),
        ("T3 Uzunluğu", "6"),
        ("DMI Uzunluğu", "24"),
        ("ADX Uzunluğu", "24"),
        ("ADX Eşiği", "35"),
        ("ADX Slope", "OK"),
        ("24s Hacim Filtresi", "5M USDT"),
        ("Ranking", "ADX→Slope→Vol→T3"),
        ("Signal Result", "LONG CANDIDATE"),
        ("Final Decision", "READY"),
        ("Block Reason", "—"),
        ("Closed Candle", "1H ONLY"),
        ("UI Refresh", "2dk / no decision"),
        ("Position Config", "Entry Snapshot"),
        ("Manual Close", "UIIntent only"),
        ("Panic", "Safe Mode"),
        ("Optimization", "Ayrı Sekme"),
        ("Auto Apply", "YASAK"),
        ("Live Lock", "LIVE_TRADING=false"),
    ]

    risk_rows = [
        ("PAPER EXECUTION / LEDGER", "display metadata"),
        ("Ledger Source", "TRUE"),
        ("Gross PnL", "+263.24"),
        ("Net PnL", "+248.39"),
        ("Commission", "-14.85"),
        ("Funding", "+0.00"),
        ("Slippage", "-0.00"),
        ("Max coin", "5 / 10"),
        ("Free balance", "8,642.10"),
        ("Allocation", "100 USDT"),
        ("Same-symbol lock", "ON"),
        ("No hedge", "ON"),
        ("No auto reversal", "ON"),
        ("Risk permission", "ALLOW"),
        ("Gerçek emir", "YOK"),
    ]

    css = """
<style>
:root {
  --bg:#050a0e;
  --panel:#09131a;
  --line:#3a5260;
  --soft:#9c927f;
  --text:#e7d7ba;
  --green:#49c86a;
  --red:#ef5a50;
  --blue:#25a7d4;
  --yellow:#e3b13f;
  --scroll-thumb:#4ca7c7;
  --scroll-track:#16272f;
}

* { box-sizing:border-box; }

html, body {
  margin:0;
  width:100%;
  height:100%;
  max-width:100%;
  max-height:100%;
  overflow:hidden!important;
  overscroll-behavior:none;
  background:var(--bg);
  color:var(--text);
  font-family:"Segoe UI", Arial, sans-serif;
  font-size:12.4px;
}

body {
  position:fixed;
  inset:0;
}

.terminal {
  position:fixed;
  inset:0;
  width:100%;
  height:100%;
  max-width:100%;
  max-height:100%;
  min-width:0;
  min-height:0;
  display:grid;
  grid-template-columns:220px 1fr;
  overflow:hidden;
  background:
    radial-gradient(circle at 30% 10%, rgba(88,126,139,.035), transparent 28%),
    linear-gradient(180deg, #081016 0%, #050b0f 100%);
}

.sidebar {
  min-width:0;
  max-width:100%;
  min-height:0;
  min-width:0;
  border-right:1px solid var(--line);
  background:linear-gradient(180deg,#09151c,#0a171d);
  display:grid;
  grid-template-rows:88px 1fr 186px;
  overflow:hidden;
}

.logo {
  padding:14px 18px 10px 18px;
  border-bottom:1px solid var(--line);
  overflow:hidden;
}

.logo .title {
  font-size:20px;
  font-weight:900;
  line-height:1.05;
  letter-spacing:.4px;
}

.logo .sub {
  margin-top:5px;
  color:#c2d0db;
  font-size:10.8px;
  line-height:1.2;
  white-space:nowrap;
}

.nav {
  padding:10px 0 6px;
  overflow:hidden;
}

.nav a {
  height:36px;
  display:flex;
  align-items:center;
  gap:12px;
  padding:0 19px;
  color:#ddc59f;
  text-decoration:none;
  border-left:4px solid transparent;
  font-size:12.8px;
}

.nav a:first-child {
  background:linear-gradient(90deg,#18333d,#13262e);
  border-left-color:var(--blue);
  color:#e5dac7;
}

.nav .ico {
  width:19px;
  text-align:center;
  color:#eaf7ff;
  font-size:15px;
}

.sidebar-foot {
  border-top:1px solid var(--line);
  padding:12px 18px;
  line-height:1.55;
  color:#91a8b8;
  font-size:11.2px;
}

.sidebar-foot b {
  color:#48df70;
}

.main {
  position:relative;
  width:100%;
  max-width:100%;
  min-width:0;
  min-height:0;
  padding:6px 8px;
  display:grid;
  grid-template-rows:56px 288px 352px minmax(0, 1fr) 42px;
  gap:6px;
  overflow:hidden;
}

.topbar {
  display:grid;
  grid-template-columns:auto 1fr auto;
  align-items:center;
  gap:12px;
  min-width:0;
}

.commands {
  display:flex;
  gap:8px;
  align-items:center;
  height:100%;
}

.cmd {
  min-width:92px;
  height:42px;
  padding:3px 9px;
  border-radius:4px;
  background:#0b1f2b;
  color:#fff;
  border:1px solid var(--line);
  font-weight:900;
  font-size:12px;
  line-height:1.05;
  letter-spacing:.25px;
  text-align:center;
  cursor:not-allowed;
}

.cmd span,
.cmd strong {
  display:block;
}

.cmd.red { border-color:#9d443f; color:var(--red); box-shadow:none; }
.cmd.green { border-color:#3d8d55; color:var(--green); }
.cmd.yellow { border-color:#987a31; color:var(--yellow); min-width:128px; }
.cmd.blue { border-color:#307f9c; color:var(--blue); }
.cmd.locked { border-color:#52606d; color:#aab4bf; }

.sysinfo {
  justify-self:end;
  color:#d3dde5;
  font-size:11.5px;
  white-space:nowrap;
}

.sysinfo span {
  margin-left:10px;
  padding-left:10px;
  border-left:1px solid #5c6871;
}

.cards {
  display:grid;
  grid-template-columns:.85fr .90fr .90fr .95fr 1.75fr;
  grid-auto-rows:minmax(0, 1fr);
  align-items:stretch;
  gap:6px;
  min-width:0;
  min-height:0;
  max-width:100%;
  overflow:hidden;
}

.cards > .panel {
  width:100%;
  height:100%;
  min-width:0;
  min-height:0;
  align-self:stretch;
}

.panel {
  background:linear-gradient(180deg,rgba(7,24,34,.99),rgba(4,16,23,.99));
  border:1px solid var(--line);
  border-radius:5px;
  box-shadow:0 0 0 1px rgba(0,0,0,.22);
  overflow:hidden;
}

.panel-title {
  height:25px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 9px;
  color:#e6f0f7;
  font-weight:900;
  letter-spacing:.45px;
  font-size:12.8px;
  border-bottom:1px solid #203744;
  text-transform:uppercase;
}

.sub-title {
  height:18px;
  padding:2px 9px;
  color:#f0b72f;
  font-size:9.5px;
  font-weight:900;
  letter-spacing:.4px;
  border-bottom:1px solid rgba(73,104,122,.35);
  text-transform:uppercase;
}

.card-body {
  padding:5px 9px;
  max-height:calc(100% - 25px);
  min-width:0;
  overflow:hidden;
}

.kv {
  height:20px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom:1px solid rgba(73,104,122,.35);
  color:#d3bc96;
  min-width:0;
}

.kv span,
.kv b {
  min-width:0;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.kv span { flex:1 1 auto; }
.kv b { flex:0 1 55%; text-align:right; }

.scan-summary .card-body {
  padding:4px 7px;
}

.scan-summary .kv {
  height:19px;
  font-size:10.2px;
  line-height:1;
}

.scan-summary .kv b {
  font-size:10px;
}

.kv b {
  font-size:10.6px;
  color:#dceaf3;
}

.ok { color:var(--green)!important; }
.bad { color:var(--red)!important; }
.warn { color:var(--yellow)!important; }
.blue { color:var(--blue)!important; }

.mid {
  display:grid;
  grid-template-columns:1.05fr 1fr;
  gap:6px;
  min-height:0;
  min-width:0;
  overflow:hidden;
}

.chart-panel {
  display:grid;
  grid-template-rows:29px 1fr;
  min-height:0;
}

.chart-head {
  height:29px;
  padding:0 10px;
  display:flex;
  align-items:center;
  gap:9px;
  border-bottom:1px solid var(--line);
  font-size:11.5px;
}

.select {
  border:1px solid #3e5c6e;
  padding:3px 7px;
  border-radius:4px;
  background:#0b1d28;
  color:#dce8f2;
}

.chart-svg {
  width:100%;
  height:100%;
  display:block;
}

.gridline {
  stroke:#173240;
  stroke-width:1;
}

.chart-label {
  fill:#d7e5ef;
  font-size:13px;
}

.axis {
  fill:#97aab8;
  font-size:12px;
}

.price {
  fill:#dff7e8;
  font-size:14px;
  font-weight:900;
}

.buy {
  fill:var(--green);
  font-size:21px;
  font-weight:900;
}

.sell {
  fill:var(--red);
  font-size:21px;
  font-weight:900;
}

.right-mid {
  display:grid;
  grid-template-columns:1.25fr .75fr;
  gap:6px;
  min-height:0;
  min-width:0;
  overflow:hidden;
}

.history-panel {
  display:grid;
  grid-template-rows:25px minmax(0, 1fr);
  min-height:0;
}

.trade-history-scroll {
  min-height:0;
  overflow-y:scroll;
  overflow-x:hidden;
  scrollbar-width:auto;
  scrollbar-color:var(--scroll-thumb) var(--scroll-track);
  scrollbar-gutter:stable;
}

.right-mid .table th,
.right-mid .table td {
  height:27px;
  font-size:10.7px;
}

.history-panel .table th:nth-child(1),
.history-panel .table td:nth-child(1) { width:16%; }
.history-panel .table th:nth-child(2),
.history-panel .table td:nth-child(2) { width:22%; }
.history-panel .table th:nth-child(3),
.history-panel .table td:nth-child(3) { width:14%; }
.history-panel .table th:nth-child(4),
.history-panel .table td:nth-child(4) { width:17%; }
.history-panel .table th:nth-child(5),
.history-panel .table td:nth-child(5) { width:16%; }
.history-panel .table th:nth-child(6),
.history-panel .table td:nth-child(6) { width:15%; }

.strategy {
  display:grid;
  grid-template-rows:25px 1fr;
  min-height:0;
}

.strategy-scroll {
  overflow-y:scroll;
  overflow-x:hidden;
  scrollbar-width:auto;
  scrollbar-color:var(--scroll-thumb) var(--scroll-track);
  scrollbar-gutter:stable;
}

.note {
  padding:4px 9px;
  color:#c4d1dc;
  font-size:9.4px;
  line-height:1.18;
  border-bottom:1px solid rgba(73,104,122,.35);
}

.param {
  display:grid;
  grid-template-columns:minmax(105px, .9fr) minmax(140px, 1.1fr);
  gap:5px;
  align-items:center;
  height:22px;
  padding:0 9px;
  border-bottom:1px solid rgba(73,104,122,.35);
  font-size:10.2px;
}

.control-group {
  display:flex;
  justify-content:flex-end;
  align-items:center;
  gap:3px;
  min-width:0;
}

.display-value,
.display-control {
  border:1px solid #52636d;
  border-radius:4px;
  min-width:48px;
  height:20px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  background:#101c22;
  color:#ddd3c3;
  font:inherit;
  font-size:9.8px;
  line-height:1;
  padding:0 5px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.display-value {
  min-width:60px;
  border-color:#9a7b3d;
  background:#282115;
  color:#f2d58f;
}

.display-control {
  cursor:not-allowed;
  opacity:1;
}

.display-control.is-active {
  border-color:#2bbbe4;
  color:#d4f7ff;
  background:#0a4052;
  box-shadow:none;
}

.lower {
  display:block;
  min-width:0;
  max-width:100%;
  min-height:0;
  overflow:hidden;
}

.event-panel {
  display:grid;
  grid-template-rows:25px minmax(0, 1fr);
  height:100%;
  min-height:0;
}

.event-scroll {
  min-height:0;
  overflow-y:scroll;
  overflow-x:hidden;
  scrollbar-width:auto;
  scrollbar-color:var(--scroll-thumb) var(--scroll-track);
  scrollbar-gutter:stable;
}

.table {
  width:100%;
  border-collapse:collapse;
  table-layout:fixed;
}

.table th,
.table td {
  height:20px;
  padding:1px 5px;
  border-bottom:1px solid rgba(73,104,122,.35);
  color:#d5e1ea;
  font-size:10.6px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.table th {
  color:#8fa2b0;
  font-size:10.3px;
  text-transform:uppercase;
  letter-spacing:.35px;
}

.event-panel .table th,
.event-panel .table td {
  height:21px;
  font-size:10.5px;
}

.positions-scroll {
  height:262px;
  overflow-y:scroll;
  overflow-x:hidden;
  scrollbar-width:auto;
  scrollbar-color:var(--scroll-thumb) var(--scroll-track);
  scrollbar-gutter:stable;
}

.positions-scroll .table th,
.positions-scroll .table td {
  height:22px;
  font-size:10px;
  padding:1px 4px;
}

.positions-scroll .table th,
.trade-history-scroll .table th,
.event-scroll .table th {
  position:sticky;
  top:0;
  z-index:2;
  background:#0b171e;
}

.row-action {
  border:1px solid #d65850;
  color:#ffd0cb;
  background:#4a1818;
  height:14px;
  padding:0 4px;
  border-radius:3px;
  font-size:8px;
  font-weight:800;
  cursor:not-allowed;
}

.dir-long,
.pnl-pos {
  color:var(--green)!important;
  font-weight:800;
}

.dir-short,
.pnl-neg {
  color:var(--red)!important;
  font-weight:800;
}

.status-open,
.status-loss,
.status-closed {
  font-weight:900;
  text-align:center;
  border-radius:3px;
}

.status-open {
  color:#d9f5ff!important;
  background:#0b526b;
  box-shadow:inset 0 0 0 1px #238db1;
}

.status-loss {
  color:#ffd4d0!important;
  background:#571d1d;
  box-shadow:inset 0 0 0 1px #c34e47;
}

.status-closed {
  color:#dcffe3!important;
  background:#164628;
  box-shadow:inset 0 0 0 1px #3b9b58;
}

.risk-list {
  list-style:none;
  padding:5px 9px;
  margin:0;
}

.risk-list li {
  height:13px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom:1px solid rgba(73,104,122,.35);
  font-size:9px;
}

.risk-list b {
  color:#e4edf5;
}

.risk-list span {
  color:var(--yellow);
  font-weight:900;
}

.healthbar {
  display:grid;
  grid-template-columns:190px repeat(7,1fr);
  align-items:center;
  padding:0 20px;
  gap:10px;
  min-width:0;
  overflow:hidden;
}

.health-title {
  font-size:15px;
  letter-spacing:1px;
  font-weight:900;
}

.health-item {
  display:flex;
  align-items:center;
  justify-content:center;
  gap:8px;
  color:#c8d6df;
  white-space:nowrap;
  font-size:10.5px;
}

.health-item i {
  width:14px;
  height:14px;
  border-radius:50%;
  display:inline-block;
  background:var(--green);
  box-shadow:none;
}

.health-item i.warn {
  background:var(--yellow);
  box-shadow:none;
}

.health-item strong {
  color:#90d82f;
  font-size:10px;
  margin-left:3px;
}

.footerline {
  position:absolute;
  left:10px;
  bottom:56px;
  color:#7a8e9b;
  font-size:9px;
  max-width:980px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.positions-scroll::-webkit-scrollbar,
.trade-history-scroll::-webkit-scrollbar,
.strategy-scroll::-webkit-scrollbar,
.event-scroll::-webkit-scrollbar {
  width:11px;
  height:11px;
}

.positions-scroll::-webkit-scrollbar-track,
.trade-history-scroll::-webkit-scrollbar-track,
.strategy-scroll::-webkit-scrollbar-track,
.event-scroll::-webkit-scrollbar-track {
  background:var(--scroll-track);
}

.positions-scroll::-webkit-scrollbar-thumb,
.trade-history-scroll::-webkit-scrollbar-thumb,
.strategy-scroll::-webkit-scrollbar-thumb,
.event-scroll::-webkit-scrollbar-thumb {
  background:var(--scroll-thumb);
  border:2px solid var(--scroll-track);
  border-radius:8px;
}

.positions-scroll::-webkit-scrollbar-thumb:hover,
.trade-history-scroll::-webkit-scrollbar-thumb:hover,
.strategy-scroll::-webkit-scrollbar-thumb:hover,
.event-scroll::-webkit-scrollbar-thumb:hover {
  background:#64bfdc;
}
</style>
"""

    head = (
        "<!doctype html>\n"
        '<html lang="tr">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        "<title>Tilson T3 Control Center</title>\n"
        f"{css}\n"
        "</head>\n"
    )

    nav_targets = (
        "faz21_control_center.html", "control_center/02_canli_tarama.html", "control_center/03_sinyaller.html",
        "control_center/04_acik_pozisyonlar.html", "control_center/05_islem_gecmisi.html",
        "control_center/06_grafikler.html", "control_center/07_strateji.html", "control_center/08_risk.html",
        "control_center/09_sistem_sagligi.html", "control_center/10_rapor_merkezi.html",
        "control_center/17_bildirimler.html",
    )
    nav_html = "".join(
        f'<a href="{escape(target)}"><span class="ico">{escape(icon)}</span><span>{escape(label)}</span></a>'
        for (icon, label), target in zip(nav_items, nav_targets)
    )

    command_html = "".join(
        [
            _cmd("SİSTEMİ", "DURDUR", "red"),
            _cmd("SİSTEMİ", "ÇALIŞTIR", "green"),
            _cmd("YENİ GİRİŞLERİ", "DURDUR", "yellow"),
            _cmd("ACİL", "DURDUR", "red"),
            _cmd("PAPER", "AKTİF", "blue"),
            _cmd("LIVE", "HAZIR 🔒", "locked"),
        ]
    )

    open_positions = [row[:-1] + (_action_button("KAPAT"),) for row in open_positions]

    positions_table = (
        '<table class="table">'
        f"<thead><tr>{_th(('SEMBOL', 'YÖN', 'MİKTAR', 'GİRİŞ', 'MEVCUT', 'PNL (USDT)', 'PNL (%)', 'KAPAT'))}</tr></thead>"
        "<tbody>"
        + "".join(_position_row(row) for row in open_positions)
        + "</tbody></table>"
    )

    trade_history_table = (
        '<table class="table">'
        f"<thead><tr>{_th(('ZAMAN', 'SEMBOL', 'YÖN', 'SONUÇ', 'PNL', 'PNL %'))}</tr></thead>"
        "<tbody>"
        + "".join(_trade_history_row(row) for row in trade_history)
        + "</tbody></table>"
    )

    event_table = (
        '<table class="table">'
        f"<thead><tr>{_th(('ZAMAN', 'TÜR', 'YAKLAŞAN SİNYAL', 'SEMBOL', 'YÖN', 'TFC/USDT', 'DURUM', 'FİYAT', 'PNL', 'NEDEN / AÇIKLAMA'))}</tr></thead>"
        "<tbody>"
        + "".join(_event_row(row) for row in event_rows)
        + "</tbody></table>"
    )

    # Genel Bakış onaylı Strateji Özeti: yalnız kullanıcı kontrollü alanlar.
    strategy_rows = [
        ("T3 Factor", _display_value("0.7")),
        ("T3 Period", _display_value("4")),
        ("T3 Entry Mode", _display_control("DEĞİŞİM", "mode", True) + _display_control("DEVAM", "mode")),
        ("DMI Length", _display_value("24")),
        ("ADX Smoothing", _display_value("24")),
        ("ADX Threshold", _display_value("30")),
        ("ADX Slope", _display_control("ON", "toggle", True) + _display_control("OFF", "toggle") + _display_value("N = 6")),
        ("Volume Filter", _display_control("ON", "toggle", True) + _display_control("OFF", "toggle")),
        ("Max Coin", _display_value("10")),
        ("Coin Başı Allocation", _display_value("200 USDT")),
        ("Leverage", _display_value("1x")),
        ("Stop Loss", _display_control("ON", "toggle", True) + _display_control("OFF", "toggle") + _display_value("%2")),
        ("Closed Candle", _display_value("1H")),
        ("UI Refresh", _display_value("2 dk")),
        ("Strateji Adı", _display_value("Tilson T3 Slope")),
    ]

    strategy_html = "".join(
        f'<div class="param"><span>{escape(label)}</span><div class="control-group">{controls}</div></div>'
        for label, controls in strategy_rows
    )

    risk_html = "".join(
        f"<li><b>{escape(k)}</b><span>{escape(v)}</span></li>"
        for k, v in risk_rows
    )

    body = f"""
<body>
<div class="terminal" data-target-viewport="1920x1080" data-paper-only="true" data-live-locked="true" data-display-only="true">

  <aside class="sidebar">
    <div class="logo">
      <div class="title">EMA MODEL<br>TRADE</div>
      <div class="sub">ALGORİTMA TİCARET SİSTEMİ</div>
    </div>

    <nav class="nav">
      {nav_html}
    </nav>

    <div class="sidebar-foot">
      <div>MOD</div>
      <b>PAPER MODE</b>
      <div style="margin-top:9px">HESAP TÜRÜ</div>
      <div>OKX (TESTNET)</div>
      <div style="margin-top:9px">API</div>
      <b>Bağlı</b>
      <div style="margin-top:9px">v1.6.4</div>
    </div>
  </aside>

  <main class="main">

    <section class="topbar">
      <div class="commands">{command_html}</div>
      <div></div>
      <div class="sysinfo">
        Sistem: v1.6.4
        <span>Sunucu: FRA-1</span>
        <span>Saat: 19:42:18</span>
        <span>UTC+3</span>
        <span>Çalışma Süresi: 2g 14sa 32dk</span>
      </div>
    </section>

    <section class="cards">
      <div class="panel">
        <div class="panel-title">CÜZDAN ÖZETİ <small>(USDT)</small></div>
        <div class="card-body">
          {_kv("Başlangıç Bakiyesi", "10,000.00")}
          {_kv("Anlık Equity", "10,248.62", "ok")}
          {_kv("Kullanılabilir Bakiye", "8,642.10")}
          {_kv("Kullanılan Teminat", "1,606.52")}
          {_kv("Açık Pozisyon Değeri", "6,621.34")}
          {_kv("Gerçekleşmiş PnL", "+2,356.78", "ok")}
          {_kv("Gerçekleşmemiş PnL", "+146.39", "ok")}
          {_kv("Toplam PnL", "+2,503.17", "ok")}
          {_kv("Günlük Değişim", "+146.39 · +1.43%", "ok")}
          {_kv("Son Güncelleme", "19:42:16")}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">PnL ÖZETİ <small>(USDT)</small></div>
        <div class="card-body">
          {_kv("Gerçekleşen PnL", "+146.39 · +1.43%", "ok")}
          {_kv("Gerçekleşmemiş PnL", "+102.54 · +1.01%", "ok")}
          {_kv("Komisyon", "-14.85", "bad")}
          {_kv("Finansman", "-2.36", "bad")}
          {_kv("Toplam Net PnL", "+248.39 · +2.48%", "ok")}
          {_kv("Günlük Değişim", "+146.39 · +1.43%", "ok")}
          {_kv("Haftalık Değişim", "+812.77 · +8.47%", "ok")}
          {_kv("Aylık Değişim", "+2,103.45 · +21.03%", "ok")}
          {_kv("Yıllık Değişim", "+8,974.21 · +89.74%", "ok")}
        </div>
      </div>

      <div class="panel scan-summary">
        <div class="panel-title">CANLI TARAMA ÖZETİ</div>
        <div class="card-body">
          {_kv("Tarama Durumu", "Çalışıyor", "ok")}
          {_kv("Son Tarama", "19:42:16")}
          {_kv("Tarama Süresi", "0.32s")}
          {_kv("Taranan Evren Sembol", "312")}
          {_kv("Erişilen Sembol", "18")}
          {_kv("Filtrelenen Sembol", "294")}
          {_kv("Sonuç Üreten Strateji", "3 / 5")}
          {_kv("Son Eşleşme", "SOL/USDT (SHORT)", "bad")}
          {_kv("Güven Skoru (Ortalama)", "75 / 100", "ok")}
          {_kv("Sinyal Yoğunluğu", "Orta")}
          {_kv("Piyasa Koşulları", "Nötr")}
          {_kv("Volatilite (7g)", "2.18%")}
          {_kv("Trend Gücü (ADX Ort.)", "23.7")}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">RAPOR ÖZETİ</div>
        <div class="card-body">
          {_kv("Rapor Türü", "Bugün / Toplam")}
          {_kv("Toplam İşlem", "69 / 1,324")}
          {_kv("Giriş İşlem", "33 (47.83%) / 642 (48.49%)")}
          {_kv("Kârlı İşlem", "41 (59.42%) / 816 (61.63%)")}
          {_kv("Zararlı İşlem", "28 (40.58%) / 508 (38.37%)")}
          {_kv("Toplam PnL", "+146.39 / +2,604.18", "ok")}
          {_kv("Ortalama PnL / İşlem", "+2.12 / +1.97", "ok")}
          {_kv("En Büyük Kâr", "+178.45 / +312.27", "ok")}
          {_kv("En Büyük Zarar", "-66.40 / -102.54", "bad")}
          {_kv("Kazanç Oranı", "59.42% / 61.63%", "ok")}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">AÇIK POZİSYONLAR (10)</div>
        <div class="positions-scroll">
          {positions_table}
        </div>
      </div>
    </section>

    <section class="mid">
      <div class="panel chart-panel">
        <div class="chart-head">
          <b>GRAFİK — Sembol</b>
          <span class="select">BTC/USDT</span>
          <span class="select">15d</span>
          <span>Gösterge</span>
          <span class="select">Tilson T3 (6)</span>
          <span class="select">Mum Grafiği</span>
        </div>
        {_chart_svg()}
      </div>

      <div class="right-mid">
        <div class="panel history-panel">
          <div class="panel-title">İŞLEM GEÇMİŞİ <small>(SON 10)</small></div>
          <div class="trade-history-scroll">
            {trade_history_table}
          </div>
        </div>

          <div class="panel strategy">
          <div class="panel-title">STRATEJİ ÖZETİ</div>
          <div class="strategy-scroll">
            {strategy_html}
          </div>
        </div>
      </div>
    </section>

    <section class="lower">
      <div class="panel event-panel">
        <div class="panel-title">GERÇEK ZAMANLI OLAY / EMİR AKIŞI</div>
        <div class="event-scroll">
          {event_table}
        </div>
      </div>

    </section>

    <section class="panel healthbar">
      <div class="health-title">SİSTEM SAĞLIĞI</div>
      {_status_dot("API Bağlantısı")}
      {_status_dot("Piyasa Verisi")}
      {_status_dot("Veritabanı")}
      {_status_dot("Recovery")}
      {_status_dot("Runtime Worker")}
      {_status_dot("Yedekleme", "warn")}
      {_status_dot("Veri Gecikmesi", value="92 ms")}
    </section>

    <div class="footerline">
      <span style="display:none" aria-label="PAPER EXECUTION / LEDGER" data-test="paper-execution-ledger">PAPER EXECUTION / LEDGER</span>LIVE_TRADING=false · live_order_sent=false · Gerçek emir endpoint yok · UI refresh 2 dakika / karar üretmez
    </div>

  </main>
</div>
</body>
</html>
"""

    html = head + body

    if output:
        Path(output).write_text(html, encoding=OUTPUT_ENCODING, newline="\n")

    return html
