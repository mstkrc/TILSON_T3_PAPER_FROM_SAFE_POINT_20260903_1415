from pathlib import Path
import re

D=Path(__file__).resolve().parents[1]/'outputs/control_center'
FILES=['10_rapor_merkezi.html','11_portfoy_analiz_raporu.html','12_performans_analizi.html','13_islem_analizi.html','14_risk_merkezi.html','15_strateji_raporlari.html','16_ozel_raporlar.html']
def main():
    for name in FILES:
        p=D/name; s=p.read_text(encoding='utf-8')
        # Remove legacy duplicate report navigation only; preserve report-subtabs and panels.
        s=re.sub(r'<div[^>]*class="tabs"[^>]*>.*?</div>', '', s, flags=re.I|re.S)
        if name=='10_rapor_merkezi.html':
            s=re.sub(r'<td class="action">.*?</td>', '<td class="action">Görüntüle</td>', s, flags=re.I|re.S)
            s=re.sub(r'^[^<]*(?:ã€€|â|Ã)[^<]*', '', s, flags=re.M)
            s=s.replace('90 günã€€„','90 gün').replace('365 günã€€„','365 gün')
            s=re.sub(r'<div>(?:£|³|§)[^<]*(Günlük|Haftalık|Aylık|Risk|Sistem)', r'<div>\1', s)
        p.write_text(s,encoding='utf-8',newline='\n')
if __name__=='__main__': main()
