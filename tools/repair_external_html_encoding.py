"""Repair reversible UTF-8 mojibake into a separate external-source directory."""
from pathlib import Path
import re

SOURCE = Path(r"D:\Masaustu\TILSON_T3_EXTERNAL_UI_11_17_HTML")
DEST = Path(r"D:\Masaustu\TILSON_T3_EXTERNAL_UI_11_17_HTML_UTF8_REPAIRED")
FILES = ["11_portfoy_analiz_raporu.html", "12_performans_analizi.html", "13_islem_analizi.html", "14_risk_merkezi.html", "15_strateji_raporlari.html", "16_ozel_raporlar.html", "17_bildirimler.html"]
PATTERN = re.compile(r"Ãƒ|Ã‚|Ã„|Ã…|Ã¢|Ã|Â|â|ï¿½|�")

def score(s: str) -> int:
    return len(PATTERN.findall(s)) + s.count("�") * 10

def repair(s: str) -> str:
    best = s
    for enc in ("latin1", "cp1252"):
        try:
            candidate = best.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if score(candidate) < score(best):
            best = candidate
    replacements = {"Ã‚": "", "Ãƒâ€¡": "Ç", "ÃƒÂ§": "ç", "Ãƒâ€“": "Ö", "ÃƒÂ¶": "ö", "ÃƒÅ“": "Ü", "ÃƒÂ¼": "ü", "Ã„Â°": "İ", "Ã„Â±": "ı", "Ã…Å¾": "Ş", "Ã…Å¸": "ş", "Ã„Å¾": "Ğ", "Ã„Å¸": "ğ"}
    for old, new in replacements.items():
        best = best.replace(old, new)
    return best

def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    results = []
    for name in FILES:
        text = (SOURCE / name).read_text(encoding="utf-8")
        if "�" in text:
            raise SystemExit(f"replacement character in source: {name}")
        fixed = repair(text)
        (DEST / name).write_text(fixed, encoding="utf-8", newline="\n")
        strict = (DEST / name).read_text(encoding="utf-8")
        results.append((name, score(text), score(strict), "�" not in strict))
    for row in results:
        print(f"{row[0]} mojibake_before={row[1]} mojibake_after={row[2]} replacement_free={row[3]}")
    if any(after or not ok for _, _, after, ok in results):
        raise SystemExit("STOP_AND_REPORT_EXTERNAL_HTML_MOJIBAKE_REMAINS")

if __name__ == "__main__":
    main()
