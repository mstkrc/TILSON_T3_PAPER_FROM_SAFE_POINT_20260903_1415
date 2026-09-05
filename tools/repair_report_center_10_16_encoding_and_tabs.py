from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "outputs" / "control_center"
FILES = ["10_rapor_merkezi.html", "11_portfoy_analiz_raporu.html", "12_performans_analizi.html", "13_islem_analizi.html", "14_risk_merkezi.html", "15_strateji_raporlari.html", "16_ozel_raporlar.html"]
SCREEN = {"10_rapor_merkezi.html": "report_center", "11_portfoy_analiz_raporu.html": "report_portfolio", "12_performans_analizi.html": "report_performance", "13_islem_analizi.html": "report_trade_analysis", "14_risk_merkezi.html": "report_risk", "15_strateji_raporlari.html": "report_strategy", "16_ozel_raporlar.html": "report_custom"}
TABS = [("10_rapor_merkezi.html", "RAPORLAR"), ("11_portfoy_analiz_raporu.html", "PORTFÖY ANALİZİ"), ("12_performans_analizi.html", "PERFORMANS ANALİZİ"), ("13_islem_analizi.html", "İŞLEM ANALİZİ"), ("14_risk_merkezi.html", "RİSK RAPORLARI"), ("15_strateji_raporlari.html", "STRATEJİ RAPORLARI"), ("16_ozel_raporlar.html", "ÖZEL RAPORLAR")]
BAD = re.compile(r"Ãƒ|Ã‚|Ã„|Ã…|Ã¢|Ã°|Ã¯|Â|â|ï¿½|�")
MAP = {"Ã‚Â·":"·", "Ã‚":"", "Ãƒâ€¡":"Ç", "ÃƒÂ§":"ç", "Ãƒâ€“":"Ö", "ÃƒÂ¶":"ö", "ÃƒÅ“":"Ü", "ÃƒÂ¼":"ü", "Ã„Â°":"İ", "Ã„Â±":"ı", "Ã…Å¾":"Ş", "Ã…Å¸":"ş", "Ã„Å¾":"Ğ", "Ã„Å¸":"ğ", "Ã¢â‚¬â€œ":"–", "Ã¢â‚¬â€":"—", "Ã¢â‚¬â„¢":"’", "Ã¢â‚¬Å“":"“", "Ã¢â‚¬Â":"”", "Ã¯Â¿Â½":"�", "Ã¶":"ö", "Ã¼":"ü", "Ã–":"Ö", "Ãœ":"Ü", "Ã‡":"Ç", "Ã§":"ç", "Ä°":"İ", "Ä±":"ı", "Åž":"Ş", "ÅŸ":"ş", "Äž":"Ğ", "ÄŸ":"ğ", "Â·":"·", "Ã":""}

def score(s): return len(BAD.findall(s))
def repair(s):
    for _ in range(4):
        old = s
        for a, b in MAP.items(): s = s.replace(a, b)
        if score(s) >= score(old): break
    return s
def bar(active):
    links = "".join(f'<a href="{href}" class="{"active" if href == active else ""}" data-action="open_report">{label}</a>' for href, label in TABS)
    return f'<nav class="report-subtabs" data-action="open_report" aria-label="Report Center tabs">{links}</nav>'

def main():
    before, after = {}, {}
    for name in FILES:
        p = DIR / name; s = p.read_text(encoding="utf-8"); before[name] = score(s); s = repair(s)
        s = re.sub(r'<nav class="report-subtabs".*?</nav>', '', s, flags=re.I | re.S)
        s = re.sub(r'<nav class="report-tabs".*?</nav>', '', s, flags=re.I | re.S)
        s = s.replace('<script src="../assets/control_center_state_bridge.js"></script>', '<script src="../assets/control_center_state_bridge.js"></script>', 1)
        s = re.sub(r'<html([^>]*)>', lambda m: '<html' + m.group(1) + f' data-screen="{SCREEN[name]}"', s, count=1, flags=re.I) if 'data-screen=' not in s[:s.find('</head>')+7] else s
        s = s.replace('</head>', '<style>.report-subtabs{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 14px}.report-subtabs a{display:inline-flex;align-items:center;justify-content:center;min-height:30px;padding:7px 14px;border:1px solid rgba(78,184,255,.45);border-radius:4px;background:rgba(4,22,32,.9);color:#d8f3ff;text-decoration:none;font-weight:700;font-size:12px}.report-subtabs a.active{background:rgba(0,137,204,.65);border-color:rgba(90,210,255,.9);color:#fff}</style></head>', 1)
        marker = '<main' if '<main' in s else '<body'
        pos = s.find(marker)
        if pos >= 0:
            end = s.find('>', pos) + 1; s = s[:end] + bar(name) + s[end:]
        p.write_text(s, encoding='utf-8', newline='\n'); after[name] = score(s)
    for name in FILES: print(f'{name} mojibake_before={before[name]} after={after[name]}')

if __name__ == '__main__': main()
