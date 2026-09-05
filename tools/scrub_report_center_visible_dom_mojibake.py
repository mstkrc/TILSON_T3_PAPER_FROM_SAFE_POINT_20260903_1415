from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'outputs/control_center'
FILES=['10_rapor_merkezi.html','11_portfoy_analiz_raporu.html','12_performans_analizi.html','13_islem_analizi.html','14_risk_merkezi.html','15_strateji_raporlari.html','16_ozel_raporlar.html']
BAD=set('ÃÂÄÅâ')
MAP={'Å\x9e':'Ş','Å\x9f':'ş','Ä\x9e':'Ğ','Ä\x9f':'ğ','Ä\xb0':'İ','Ä\xb1':'ı','Ã\x96':'Ö','Ã\x9c':'Ü','Ã\xa7':'ç','Ã\xb6':'ö','Ã\xbc':'ü','Ã\x87':'Ç','Â·':'·','Ã‚Â·':'·','Ã‚':'','Ã¶':'ö','Ã¼':'ü','Ã–':'Ö','Ãœ':'Ü','Ã‡':'Ç','Ã§':'ç','Ä°':'İ','Ä±':'ı','Åž':'Ş','ÅŸ':'ş','Äž':'Ğ','ÄŸ':'ğ'}
def clean(s):
    for a,b in MAP.items(): s=s.replace(a,b)
    # Remaining isolated mojibake is limited to broken icon glyphs in visible nodes.
    s=re.sub(r'[ÃÂÄÅâ](?:[^A-Za-z0-9İıŞşĞğÇçÖöÜü\s]|[A-Za-z])?', '', s)
    return s
def main():
    for name in FILES:
        p=D/name; s=p.read_text(encoding='utf-8'); parts=re.split(r'(<(?:style|script)\b.*?</(?:style|script)>)',s,flags=re.I|re.S)
        for i in range(0,len(parts),2):
            chunks=re.split(r'(<[^>]+>)',parts[i])
            for j in range(0,len(chunks),2): chunks[j]=clean(chunks[j])
            parts[i]=''.join(chunks)
        p.write_text(''.join(parts),encoding='utf-8',newline='\n')
if __name__=='__main__': main()
