"""Reference-aligned V7 Control Center HTML renderer.

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

from .control_center import ControlCenterModel, build_control_center

def render_screen_shell(screen: str, model: ControlCenterModel | None = None, report_tab: str | None = None) -> str:
    """Safe route shell for non-overview screens; no execution side effects."""
    model = model or build_control_center()
    if screen not in model.screens:
        raise ValueError(f"Unknown Control Center screen: {screen}")
    tab = report_tab or model.active_report_tab
    if screen == "Raporlar" and tab not in model.report_tabs:
        raise ValueError(f"Unknown report tab: {tab}")
    title = f"{screen} — {tab}" if screen == "Raporlar" else screen
    return (f'<section class="screen-shell" data-screen="{escape(screen)}" data-paper-only="true" '
            f'data-live-locked="true"><h1>{escape(title)}</h1>'
            f'<p>USER APPROVED VISUAL REFERENCE SET · {escape(screen)}.png</p>'
            '<strong>PAPER ONLY · LIVE LOCKED</strong><p>Uygulama bekliyor; güvenli screen shell.</p></section>')


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


def _status_dot(label: str, cls: str = "ok") -> str:
    return (
        '<div class="health-item">'
        f'<i class="{escape(cls)}"></i>'
        f"<span>{escape(label)}</span>"
        "</div>"
    )


def _action_button(label: str) -> str:
    return f'<button class="row-action" disabled>{escape(label)}</button>'


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
        color = "#39c765" if direction == "up" else "#ff4b38"
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

      <polyline fill="none" stroke="#64be46" stroke-width="3"
        points="28,156 82,128 136,104 190,88 244,72 298,84 352,108 406,76 460,88 514,74 568,92 622,76 676,64 730,66 784,56 838,60"/>

      {"".join(candle_svg)}

      <text x="330" y="58" class="sell">S</text>
      <polygon points="336,66 327,84 345,84" fill="#ff4438"/>
      <text x="462" y="148" class="buy">B</text>
      <polygon points="468,136 458,154 478,154" fill="#3bc365"/>
      <text x="672" y="58" class="sell">S</text>
      <polygon points="678,66 669,84 687,84" fill="#ff4438"/>
      <text x="778" y="142" class="buy">B</text>
      <polygon points="784,130 774,148 794,148" fill="#3bc365"/>

      <text x="770" y="95" class="price">68,302.54</text>
      <text x="770" y="130" class="axis">68,200</text>
      <text x="770" y="168" class="axis">68,000</text>
      <text x="770" y="206" class="axis">67,800</text>

      <line x1="0" y1="214" x2="860" y2="214" stroke="#263b49"/>
      <text x="12" y="238" class="chart-label">Hacim</text>
      {"".join(volume_svg)}
      <polyline fill="none" stroke="#12a7d8" stroke-width="2"
        points="28,252 82,242 136,258 190,236 244,248 298,230 352,244 406,226 460,238 514,232 568,246 622,228 676,236 730,224 784,232 838,226"/>

      <line x1="0" y1="286" x2="860" y2="286" stroke="#263b49"/>
      <text x="12" y="314" class="chart-label">DMI / ADX</text>
      <polyline fill="none" stroke="#4caf50" stroke-width="2"
        points="126,314 172,306 218,318 264,300 310,308 356,296 402,304 448,310 494,298 540,304 586,294 632,302 678,296 724,300 790,294"/>
      <polyline fill="none" stroke="#ff3f31" stroke-width="2"
        points="126,330 172,322 218,326 264,318 310,324 356,320 402,330 448,322 494,324 540,316 586,322 632,328 678,320 724,326 790,322"/>
      <polyline fill="none" stroke="#f0b429" stroke-width="2"
        points="126,322 172,318 218,314 264,316 310,310 356,312 402,308 448,306 494,310 540,304 586,306 632,302 678,304 724,300 790,302"/>

      <text x="170" y="344" class="axis">06:00</text>
      <text x="335" y="344" class="axis">09:00</text>
      <text x="500" y="344" class="axis">12:00</text>
      <text x="665" y="344" class="axis">15:00</text>
    </svg>
    """


def render_control_center(
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
        ("BTC/USDT", "LONG", "0.0321", "68,200.00", "68,302.54", "+102.54", "+1.82%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("ETH/USDT", "LONG", "0.2100", "2,576.10", "2,604.18", "+61.78", "+1.95%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("BNB/USDT", "LONG", "0.8400", "592.00", "596.20", "+18.32", "+0.88%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("SOL/USDT", "SHORT", "4.2500", "178.45", "175.84", "-27.61", "-1.61%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("ADA/USDT", "SHORT", "1.2500", "0.4985", "0.4951", "-8.64", "-0.63%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("MATIC/USDT", "LONG", "18.000", "0.4680", "0.4721", "+6.71", "+0.51%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("AVAX/USDT", "LONG", "0.920", "36.80", "37.21", "+7.12", "+0.55%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("LINK/USDT", "SHORT", "3.100", "14.95", "14.80", "+5.21", "+0.42%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("DOT/USDT", "LONG", "7.300", "6.19", "6.24", "+4.21", "+0.34%", "2%", "ENTRY CFG", _action_button("MANUEL")),
        ("XRP/USDT", "LONG", "80.00", "0.5180", "0.5265", "+6.05", "+0.49%", "2%", "ENTRY CFG", _action_button("MANUEL")),
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
  --bg:#061019;
  --panel:#0a1b26;
  --line:#284150;
  --soft:#88a0af;
  --text:#d8e7f2;
  --green:#39c765;
  --red:#ff4638;
  --blue:#00a9e8;
  --yellow:#f0b72f;
}

* { box-sizing:border-box; }

html, body {
  margin:0;
  width:100vw;
  height:100vh;
  overflow:hidden;
  background:var(--bg);
  color:var(--text);
  font-family:"Segoe UI", Arial, sans-serif;
  font-size:11px;
}

.terminal {
  width:100vw;
  height:100vh;
  display:grid;
  grid-template-columns:245px 1fr;
  overflow:hidden;
  background:
    radial-gradient(circle at 30% 10%, rgba(0,180,220,.07), transparent 28%),
    linear-gradient(180deg, #07121b 0%, #041018 100%);
}

.sidebar {
  min-width:0;
  border-right:1px solid var(--line);
  background:linear-gradient(180deg,#071722,#0a1a25);
  display:grid;
  grid-template-rows:76px 1fr 200px;
  overflow:hidden;
}

.logo {
  padding:13px 18px 6px 18px;
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
  margin-top:3px;
  color:#c2d0db;
  font-size:10px;
  white-space:nowrap;
}

.nav {
  padding:6px 0;
  overflow:hidden;
}

.nav a {
  height:36px;
  display:flex;
  align-items:center;
  gap:12px;
  padding:0 19px;
  color:#c6d4df;
  text-decoration:none;
  border-left:4px solid transparent;
  font-size:12px;
}

.nav a:first-child {
  background:linear-gradient(90deg,#063b51,#0b2633);
  border-left-color:#00d1ff;
  color:#fff;
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
  font-size:10.5px;
}

.sidebar-foot b {
  color:#48df70;
}

.main {
  position:relative;
  padding:6px 8px;
  display:grid;
  grid-template-rows:50px 126px minmax(0, 1fr) 226px 50px;
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
  font-size:11px;
  line-height:1.05;
  letter-spacing:.25px;
  text-align:center;
  cursor:not-allowed;
}

.cmd span,
.cmd strong {
  display:block;
}

.cmd.red { border-color:#ba3c3c; color:#ff5d50; box-shadow:inset 0 0 0 1px rgba(255,0,0,.18); }
.cmd.green { border-color:#1b8d5a; color:#36d176; }
.cmd.yellow { border-color:#ba950e; color:#ffd231; min-width:128px; }
.cmd.blue { border-color:#078ec1; color:#22d7ff; }
.cmd.locked { border-color:#52606d; color:#aab4bf; }

.sysinfo {
  justify-self:end;
  color:#d3dde5;
  font-size:10.5px;
  white-space:nowrap;
}

.sysinfo span {
  margin-left:10px;
  padding-left:10px;
  border-left:1px solid #5c6871;
}

.cards {
  display:grid;
  grid-template-columns:.92fr .92fr 1.18fr 1fr 1.78fr;
  gap:6px;
  min-height:0;
}

.panel {
  background:linear-gradient(180deg,rgba(13,35,49,.98),rgba(7,24,34,.98));
  border:1px solid var(--line);
  border-radius:5px;
  box-shadow:0 0 0 1px rgba(0,0,0,.32), inset 0 0 26px rgba(0,160,220,.03);
  overflow:hidden;
}

.panel-title {
  height:23px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 9px;
  color:#e6f0f7;
  font-weight:900;
  letter-spacing:.45px;
  font-size:11.5px;
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
  padding:4px 9px;
}

.kv {
  height:13px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  border-bottom:1px solid rgba(73,104,122,.35);
  color:#c8d4dc;
}

.kv b {
  font-size:9.8px;
  color:#dceaf3;
}

.ok { color:var(--green)!important; }
.bad { color:var(--red)!important; }
.warn { color:var(--yellow)!important; }
.blue { color:var(--blue)!important; }

.mid {
  display:grid;
  grid-template-columns:1.44fr 1fr;
  gap:6px;
  min-height:0;
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
  fill:#45cf65;
  font-size:21px;
  font-weight:900;
}

.sell {
  fill:#ff4b38;
  font-size:21px;
  font-weight:900;
}

.right-mid {
  display:grid;
  grid-template-columns:.82fr 1.18fr;
  gap:6px;
  min-height:0;
}

.strategy {
  display:grid;
  grid-template-rows:23px 1fr;
  min-height:0;
}

.strategy-scroll {
  overflow-y:auto;
  overflow-x:hidden;
  scrollbar-width:thin;
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
  grid-template-columns:1fr 92px 14px;
  gap:5px;
  align-items:center;
  height:15px;
  padding:0 9px;
  border-bottom:1px solid rgba(73,104,122,.35);
  font-size:9.2px;
}

.box {
  border:1px solid #466172;
  border-radius:4px;
  height:13px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:#0a1c27;
  color:#e2edf4;
  font-size:8.7px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.lower {
  display:grid;
  grid-template-columns:1.62fr .48fr;
  gap:6px;
  min-height:0;
}

.event-panel {
  min-height:0;
}

.table {
  width:100%;
  border-collapse:collapse;
  table-layout:fixed;
}

.table th,
.table td {
  height:18px;
  padding:1px 5px;
  border-bottom:1px solid rgba(73,104,122,.35);
  color:#d5e1ea;
  font-size:9.8px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.table th {
  color:#8fa2b0;
  font-size:9.5px;
  text-transform:uppercase;
  letter-spacing:.35px;
}

.event-panel .table th,
.event-panel .table td {
  height:19px;
  font-size:9.8px;
}

.positions-scroll {
  height:102px;
  overflow-y:auto;
  overflow-x:hidden;
  scrollbar-width:thin;
}

.positions-scroll .table th,
.positions-scroll .table td {
  height:17px;
  font-size:8.8px;
  padding:1px 4px;
}

.row-action {
  border:1px solid #a44747;
  color:#ff9999;
  background:#301b22;
  height:14px;
  padding:0 4px;
  border-radius:3px;
  font-size:8px;
  font-weight:800;
  cursor:not-allowed;
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
  grid-template-columns:220px repeat(7,1fr);
  align-items:center;
  padding:0 20px;
  gap:10px;
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
  box-shadow:0 0 10px rgba(57,199,101,.35);
}

.health-item i.warn {
  background:var(--yellow);
  box-shadow:0 0 10px rgba(240,183,47,.35);
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

    nav_html = "".join(
        f'<a><span class="ico">{escape(icon)}</span><span>{escape(label)}</span></a>'
        for icon, label in nav_items
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
        f"<thead><tr>{_th(('SEMBOL', 'YÖN', 'MİKTAR', 'GİRİŞ', 'MEVCUT', 'PNL', 'PNL %', 'STOP', 'CONFIG', 'KAPAT'))}</tr></thead>"
        "<tbody>"
        + "".join(_tr(row, raw_last=True) for row in open_positions)
        + "</tbody></table>"
    )

    trade_history_table = (
        '<table class="table">'
        f"<thead><tr>{_th(('ZAMAN', 'SEMBOL', 'YÖN', 'SONUÇ', 'PNL', 'PNL %'))}</tr></thead>"
        "<tbody>"
        + "".join(_tr(row) for row in trade_history)
        + "</tbody></table>"
    )

    event_table = (
        '<table class="table">'
        f"<thead><tr>{_th(('ZAMAN', 'TÜR', 'YAKLAŞAN SİNYAL', 'SEMBOL', 'YÖN', 'TFC/USDT', 'DURUM', 'FİYAT', 'PNL', 'NEDEN / AÇIKLAMA'))}</tr></thead>"
        "<tbody>"
        + "".join(_tr(row) for row in event_rows)
        + "</tbody></table>"
    )

    # Genel Bakış onaylı Strateji Özeti: yalnız kullanıcı kontrollü alanlar.
    strategy_rows = [
        ("T3 Factor", "0.7"), ("T3 Period", "4"), ("T3 Entry Mode", "DEĞİŞİM / DEVAM"),
        ("DMI Length", "24"), ("ADX Smoothing", "24"), ("ADX Threshold", "30"),
        ("ADX Slope ON/OFF + N", "ON / OFF · N = 6"), ("Volume Filter ON/OFF", "ON / OFF"),
        ("Max Coin", "10"), ("Coin Başı Allocation", "200 USDT"), ("Leverage", "1x"),
        ("Stop Loss ON/OFF + %2", "ON / OFF · %2"), ("Closed Candle", "1H"),
        ("UI Refresh", "2 dk"), ("Strateji Adı", "Tilson T3 Slope"),
    ]

    strategy_html = "".join(
        f'<div class="param"><span>{escape(k)}</span><div class="box">{escape(v)}</div><span>✎</span></div>'
        for k, v in strategy_rows
    )

    risk_html = "".join(
        f"<li><b>{escape(k)}</b><span>{escape(v)}</span></li>"
        for k, v in risk_rows
    )

    body = f"""
<body>
<div class="terminal" data-target-viewport="1920x1080" data-paper-only="true" data-live-locked="true">

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
          {_kv("Max Coin / Açık", "10 / 5")}
          {_kv("Coin Başı Allocation", "100 USDT")}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">PnL ÖZETİ <small>(USDT)</small></div>
        <div class="card-body">
          {_kv("Gross PnL", "+263.24", "ok")}
          {_kv("Net PnL", "+248.39  +2.48%", "ok")}
          {_kv("Commission", "-14.85", "bad")}
          {_kv("Funding", "+0.00")}
          {_kv("Slippage", "-0.00")}
          {_kv("Gerçekleşmemiş", "+102.54", "ok")}
          {_kv("Ledger Source", "TRUE", "ok")}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">CANLI TARAMA ÖZETİ</div>
        <div class="card-body">
          {_kv("Tarama Durumu", "Çalışıyor", "ok")}
          {_kv("Aktif Tarama Stratejisi", "Tilson T3 + DMI/ADX")}
          {_kv("Son Tarama", "19:42:16")}
          {_kv("Tarama Süresi", "0.32s")}
          {_kv("Taranan / Engellenen", "312 / 18")}
          {_kv("Filtrelenen", "294")}
          {_kv("Son Closed Candle", "19:00 UTC")}
          {_kv("Aday Detayı", "Canlı Tarama sekmesi", "warn")}
        </div>
      </div>

      <div class="panel">
        <div class="panel-title">RAPOR ÖZETİ</div>
        <div class="card-body">
          {_kv("Toplam İşlem Bugün", "69")}
          {_kv("Toplam İşlem Genel", "1,324")}
          {_kv("Giriş İşlem", "33 (47.83%)")}
          {_kv("Kârlı İşlem", "41 (59.42%)")}
          {_kv("Zararlı İşlem", "28 (40.58%)")}
          {_kv("Ortalama PnL", "+2.12", "ok")}
          {_kv("Ledger / Excel", "TRUE / Ayrı Tab", "ok")}
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
        <div class="panel">
          <div class="panel-title">İŞLEM GEÇMİŞİ <small>(SON 10)</small></div>
          {trade_history_table}
        </div>

        <div class="panel strategy">
          <div class="panel-title">STRATEJİ ÖZETİ</div>
          <div class="strategy-scroll">
            <div class="note">
              Kontrol edilmesi gereken karar zinciri bu paneldedir. Canlı Tarama sekmesinde strateji seçimi/tarama detayı bulunur.
            </div>
            {strategy_html}
          </div>
        </div>
      </div>
    </section>

    <section class="lower">
      <div class="panel event-panel">
        <div class="panel-title">GERÇEK ZAMANLI OLAY / EMİR AKIŞI</div>
        {event_table}
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
      {_status_dot("Veri Gecikmesi")}
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
