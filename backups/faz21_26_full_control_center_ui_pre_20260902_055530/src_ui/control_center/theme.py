"""Common Control Center theme tokens and safe screen-shell styles."""

COMMON_THEME_CSS = """
:root {
  --cc-bg: #06131b;
  --cc-panel: #0a1b25;
  --cc-panel-2: #0d2230;
  --cc-border: #2a4655;
  --cc-text: #f2ead8;
  --cc-muted: #a7b2b7;
  --cc-green: #43cf72;
  --cc-red: #e96862;
  --cc-yellow: #e3b64f;
  --cc-blue: #4aa9d0;
  --cc-radius: 5px;
  --cc-sidebar: 250px;
  --cc-topbar: 72px;
  --cc-healthbar: 48px;
  --cc-font: "Segoe UI", Arial, sans-serif;
  --cc-scroll-track: #102a38;
  --cc-scroll-thumb: #4d94ad;
}
* { box-sizing: border-box; }
html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }
body { background: var(--cc-bg); color: var(--cc-text); font: 14px/1.4 var(--cc-font); }
.cc-document { width: 100vw; height: 100vh; display: grid; grid-template-columns: var(--cc-sidebar) 1fr; overflow: hidden; }
.cc-sidebar { grid-row: 1 / span 3; background: #071923; border-right: 1px solid var(--cc-border); padding: 20px 12px; overflow: hidden; }
.cc-brand { font-size: 22px; font-weight: 800; letter-spacing: .08em; margin: 0 8px 22px; }
.cc-brand small { display: block; margin-top: 7px; color: var(--cc-muted); font-size: 10px; letter-spacing: .12em; }
.cc-nav { display: grid; gap: 4px; }
.cc-nav a { padding: 9px 11px; color: var(--cc-muted); border: 1px solid transparent; border-radius: var(--cc-radius); text-decoration: none; }
.cc-nav a.active { color: var(--cc-text); border-color: var(--cc-blue); background: #102b39; }
.cc-topbar { height: var(--cc-topbar); border-bottom: 1px solid var(--cc-border); display: flex; align-items: center; justify-content: space-between; padding: 12px 18px; background: #071923; }
.cc-main { min-width: 0; min-height: 0; padding: 16px; overflow: hidden; }
.cc-healthbar { height: var(--cc-healthbar); display: flex; align-items: center; gap: 18px; padding: 0 18px; border-top: 1px solid var(--cc-border); background: #071923; }
.screen-shell { height: 100%; min-height: 0; display: grid; align-content: center; justify-content: center; }
.cc-card { width: min(820px, 80vw); border: 1px solid var(--cc-border); border-radius: var(--cc-radius); background: var(--cc-panel); }
.section-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--cc-border); }
.section-header h2 { margin: 0; font-size: 16px; letter-spacing: .06em; }
.cc-card-body { padding: 20px; }
.badge { display: inline-flex; padding: 4px 8px; border: 1px solid var(--cc-border); border-radius: 4px; margin-right: 6px; font-size: 11px; font-weight: 700; }
.badge-paper { color: var(--cc-blue); border-color: var(--cc-blue); }
.badge-locked { color: var(--cc-yellow); border-color: var(--cc-yellow); }
.placeholder-reference { color: var(--cc-blue); }
.status-dot { display: inline-flex; align-items: center; gap: 6px; color: var(--cc-muted); font-size: 11px; }
.status-dot i { width: 8px; height: 8px; border-radius: 50%; background: var(--cc-green); }
.status-locked i { background: var(--cc-yellow); }
.display-button { border: 1px solid var(--cc-border); color: var(--cc-muted); background: var(--cc-panel-2); padding: 6px 10px; }
.scroll-container { overflow-y: scroll; scrollbar-color: var(--cc-scroll-thumb) var(--cc-scroll-track); scrollbar-width: auto; }
.scroll-container::-webkit-scrollbar { width: 11px; }
.scroll-container::-webkit-scrollbar-track { background: var(--cc-scroll-track); }
.scroll-container::-webkit-scrollbar-thumb { background: var(--cc-scroll-thumb); border: 2px solid var(--cc-scroll-track); border-radius: 7px; }
"""
