from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'outputs/control_center'
FILES=['10_rapor_merkezi.html','11_portfoy_analiz_raporu.html','12_performans_analizi.html','13_islem_analizi.html','14_risk_merkezi.html','15_strateji_raporlari.html','16_ozel_raporlar.html']
def test_browser_reopen_failures_are_removed():
    for name in FILES:
        s=(D/name).read_text(encoding='utf-8')
        assert len(re.findall(r'class="report-subtabs"',s))==1
        bar=re.search(r'<nav[^>]*class="report-subtabs".*?</nav>',s,re.I|re.S).group(0)
        assert len(re.findall(r'<a\b',bar,re.I))==7
        assert len(re.findall(r'class="active"',bar))==1
        assert '<div class="tabs"' not in s
        assert 'height:300px' not in bar and 'width:100%' not in bar and 'flex:1 1 200px' not in bar
    s=(D/'10_rapor_merkezi.html').read_text(encoding='utf-8')
    for bad in ('%aÃ©','%Ã¦','Ã¢â‚¬','Ãƒ','Ã‚','Ã„','Ã…','90 günã€€','365 günã€€'):
        assert bad not in s
