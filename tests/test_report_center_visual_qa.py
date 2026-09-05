from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FILES = ["10_rapor_merkezi.html", "11_portfoy_analiz_raporu.html", "12_performans_analizi.html", "13_islem_analizi.html", "14_risk_merkezi.html", "15_strateji_raporlari.html", "16_ozel_raporlar.html"]
HREFS = ["10_rapor_merkezi.html", "11_portfoy_analiz_raporu.html", "12_performans_analizi.html", "13_islem_analizi.html", "14_risk_merkezi.html", "15_strateji_raporlari.html", "16_ozel_raporlar.html"]

def bar(text):
    return re.search(r'<nav[^>]*class="report-subtabs".*?</nav>', text, re.I | re.S).group(0)

def test_report_center_visual_contract():
    for name in FILES:
        text = (ROOT / "outputs" / "control_center" / name).read_text(encoding="utf-8")
        assert text.count('class="report-subtabs"') == 1
        b = bar(text)
        assert all(href in b for href in HREFS)
        assert len(re.findall(r'<a\b', b, re.I)) == 7
        assert len(re.findall(r'class="active"', b)) == 1
        assert "../assets/control_center_state_bridge.js" in text
        assert "data-screen=" in text and "data-bind=" in text and "data-action=" in text
        visible = re.sub(r'<(?:style|script)\b.*?</(?:style|script)>', '', text, flags=re.I | re.S)
        visible = re.sub(r'<[^>]+>', '', visible)
        assert not re.search(r'Ãƒ|Ã‚|Ã„|Ã…|Ã¢â‚¬|Ã°Å¸|Ã¯Â¿Â½|ï¿½', visible)

def test_report_tab_css_is_horizontal_small_tab_style():
    for name in FILES:
        text = (ROOT / "outputs" / "control_center" / name).read_text(encoding="utf-8")
        css = re.search(r'\.report-subtabs\{.*?\.report-subtabs a\.active\{.*?\}', text, re.S).group(0)
        assert "display:flex" in css and "flex-wrap:wrap" in css
        assert "flex-direction:row" in css
        assert "height:300px" not in css and "width:100%" not in css and "flex:1 1 200px" not in css

def test_report_center_safety_and_08_14_separation():
    bridge = (ROOT / "outputs/assets/control_center_state_bridge.js").read_text(encoding="utf-8")
    assert "showStateDisconnectedBanner" in bridge and "document.body.innerHTML" not in bridge
    assert "/api/live/start" not in bridge and "/api/order/send-real" not in bridge
    risk8 = (ROOT / "outputs/control_center/08_risk.html").read_text(encoding="utf-8")
    risk14 = (ROOT / "outputs/control_center/14_risk_merkezi.html").read_text(encoding="utf-8")
    assert 'data-screen="risk_operation"' in risk8 and 'data-screen="report_risk"' in risk14
