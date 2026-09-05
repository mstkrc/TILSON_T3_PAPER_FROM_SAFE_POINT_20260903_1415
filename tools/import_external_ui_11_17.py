"""Import validated repaired report/notification screens into outputs root."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"D:\Masaustu\TILSON_T3_EXTERNAL_UI_11_17_HTML_UTF8_REPAIRED")
TARGET = ROOT / "outputs" / "control_center"
SCREENS = {"11_portfoy_analiz_raporu.html":"report_portfolio", "12_performans_analizi.html":"report_performance", "13_islem_analizi.html":"report_trade_analysis", "14_risk_merkezi.html":"report_risk", "15_strateji_raporlari.html":"report_strategy", "16_ozel_raporlar.html":"report_custom", "17_bildirimler.html":"notifications"}

def main() -> None:
    for name, screen in SCREENS.items():
        source = SOURCE / name
        if not source.is_file(): raise SystemExit(f"missing source: {name}")
        text = source.read_text(encoding="utf-8")
        title = re.search(r"(?is)<title>(.*?)</title>", text)
        if not title or re.search(r"Ã|Â|â|ï¿½|�", title.group(1)): raise SystemExit(f"critical title encoding: {name}")
        if re.search(r"/api/(live|order|binance)|api[_-]?key|secret", text, re.I): raise SystemExit(f"safety risk: {name}")
        text = re.sub(r"<html([^>]*)>", lambda m: '<html' + m.group(1) + f' data-screen="{screen}" data-paper-only="true" data-live-locked="true" data-live-order-sending-allowed="false">', text, count=1, flags=re.I)
        text = text.replace("</head>", '<script src="../assets/control_center_state_bridge.js"></script></head>', 1)
        text = text.replace("<body", '<body data-action="refresh_view_model" data-bind="wallet.equity_usd"', 1)
        text = re.sub(r"<button(?![^>]*data-action=)", '<button data-action="open_detail"', text, flags=re.I)
        (TARGET / name).write_text(text, encoding="utf-8", newline="\n")
    print(f"imported={len(SCREENS)}")

if __name__ == "__main__": main()
