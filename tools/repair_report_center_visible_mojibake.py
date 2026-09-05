from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'outputs' / 'control_center'
FILES = ['10_rapor_merkezi.html','11_portfoy_analiz_raporu.html','12_performans_analizi.html','13_islem_analizi.html','14_risk_merkezi.html','15_strateji_raporlari.html','16_ozel_raporlar.html']
BAD = re.compile(r'Ãƒ|Ã‚|Ã„|Ã…|Ã¢|Ã°|Ã¯|ï¿½|�|Â·')
MAP = {'Ã‚Â·':'·','Ã‚':'','Ãƒâ€¡':'Ç','ÃƒÂ§':'ç','Ãƒâ€“':'Ö','ÃƒÂ¶':'ö','ÃƒÅ“':'Ü','ÃƒÂ¼':'ü','Ã„Â°':'İ','Ã„Â±':'ı','Ã…Å¾':'Ş','Ã…Å¸':'ş','Ã„Å¾':'Ğ','Ã„Å¸':'ğ','Ã¢â‚¬â€œ':'–','Ã¢â‚¬â€':'—','Ã¢â‚¬â„¢':'’','Ã¢â‚¬Å“':'“','Ã¢â‚¬Â':'”','Ã¯Â¿Â½':'�','Ã¶':'ö','Ã¼':'ü','Ã–':'Ö','Ãœ':'Ü','Ã‡':'Ç','Ã§':'ç','Ä°':'İ','Ä±':'ı','Åž':'Ş','ÅŸ':'ş','Äž':'Ğ','ÄŸ':'ğ','Â·':'·'}
def score(s): return len(BAD.findall(s))
def fix_fragment(s):
    best=s
    for _ in range(3):
        old=best
        for a,b in MAP.items(): best=best.replace(a,b)
        for enc in ('cp1252','latin1'):
            try: cand=best.encode(enc,errors='ignore').decode('utf-8',errors='ignore')
            except Exception: continue
            if score(cand)<score(best): best=cand
        if score(best)>=score(old): break
    return best
def main():
    for name in FILES:
        p=DIR/name; s=p.read_text(encoding='utf-8')
        parts=re.split(r'(<(?:style|script)\b.*?</(?:style|script)>)',s,flags=re.I|re.S)
        for i in range(0,len(parts),2):
            chunks=re.split(r'(<[^>]+>)',parts[i])
            for j in range(0,len(chunks),2): chunks[j]=fix_fragment(chunks[j])
            parts[i]=''.join(chunks)
        p.write_text(''.join(parts),encoding='utf-8',newline='\n')
if __name__=='__main__': main()
