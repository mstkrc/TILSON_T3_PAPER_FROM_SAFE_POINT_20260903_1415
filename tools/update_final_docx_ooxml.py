from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as ET
import tempfile

ROOT = Path(__file__).parents[1]
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", W)
ADDENDUM = [
    "FINAL HANDOFF / DOCUMENTATION CLOSURE",
    "Faz-0 → Faz-20: PASS / LOCKED.",
    "KONU-1 → KONU-49: LOCKED. KONU-49: openpyxl 3.1.5 yalnız Faz-14 Report/Excel Export için onaylıdır.",
    "Faz-19 full regression: 77/77 PASS.",
    "Live: LIVE_TRADING=false; aktif LIVE_TRADING=true yok; gerçek emir ve Binance order endpoint yok.",
    "Paper-only korunur; Ledger single source of truth olarak kalır.",
    "Faz-20 final handoff/documentation closure tamamlandı.",
    "Final Word/DOC paketinin güncel kapanış kayıtlarıyla toplu güncellenmesi sonraki kullanıcı onaylı adımdır.",
]

def paragraph(text, bold=False):
    p = ET.Element(f"{{{W}}}p")
    r = ET.SubElement(p, f"{{{W}}}r")
    if bold: ET.SubElement(r, f"{{{W}}}rPr")
    t = ET.SubElement(r, f"{{{W}}}t")
    t.text = text
    return p

for path in sorted((ROOT / "DOKUMANTASYON").glob("*.docx")):
    with ZipFile(path, "r") as source:
        entries = {name: source.read(name) for name in source.namelist()}
    root = ET.fromstring(entries["word/document.xml"])
    body = root.find(f"{{{W}}}body")
    sect = body.find(f"{{{W}}}sectPr")
    if sect is None:
        sect = ET.SubElement(body, f"{{{W}}}sectPr")
    for i, text in enumerate(ADDENDUM):
        body.insert(list(body).index(sect), paragraph(text, i == 0))
    entries["word/document.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False, dir=path.parent) as temp:
        temp_path = Path(temp.name)
    with ZipFile(temp_path, "w", ZIP_DEFLATED) as target:
        for name, data in entries.items():
            target.writestr(name, data)
    temp_path.replace(path)
print("UPDATED=12")
