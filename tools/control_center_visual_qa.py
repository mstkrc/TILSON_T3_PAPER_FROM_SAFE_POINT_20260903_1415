"""Create read-only local visual proof images for Control Center HTML routes."""

from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
ROUTES = {
    10: ("10_rapor_merkezi.html", "10_RAPOR_MERKEZI.png"),
    11: ("11_portfoy_analiz_raporu.html", "11_PORTFOY_ANALIZ_RAPORU.png"),
    12: ("12_performans_analizi.html", "12_PERFORMANS_ANALIZI.png"),
    13: ("13_islem_analizi.html", "13_ISLEM_ANALIZI.png"),
    14: ("14_risk_merkezi.html", "14_RISK_MERKEZI.png"),
    15: ("15_strateji_raporlari.html", "15_STRATEJI_RAPORLARI.png"),
    16: ("16_ozel_raporlar.html", "16_OZEL_RAPORLAR.png"),
    17: ("17_bildirimler.html", "17_BILDIRIMLER.png"),
}


def normalize(image: Image.Image) -> Image.Image:
    return image.convert("RGB").resize((1672, 941), Image.Resampling.LANCZOS)


def main() -> None:
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found: {CHROME}")
    output = ROOT / "outputs" / "control_center_visual_qa" / (
        "group3_group4_visual_proof_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    output.mkdir(parents=True, exist_ok=False)
    references = ROOT / "DOKUMANTASYON" / "CONTROL CENTER"
    html_root = ROOT / "outputs" / "control_center"
    profile = output / ".chrome_profile"
    profile.mkdir()
    for number, (html_name, reference_name) in ROUTES.items():
        reference = normalize(Image.open(references / reference_name))
        reference_path = output / f"reference_{number}.png"
        actual_path = output / f"actual_{number}.png"
        compare_path = output / f"compare_{number}.png"
        reference.save(reference_path, format="PNG")
        url = (html_root / html_name).resolve().as_uri()
        command = [
            str(CHROME), "--headless=new", "--disable-gpu", "--no-first-run",
            "--no-default-browser-check", "--disable-extensions",
            f"--user-data-dir={profile}", "--window-size=1672,941",
            f"--screenshot={actual_path}", url,
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0 or not actual_path.exists():
            raise SystemExit(f"Screenshot failed for {number}: {result.stderr.strip()}")
        actual = normalize(Image.open(actual_path))
        actual.save(actual_path, format="PNG")
        compare = Image.new("RGB", (3344, 981), "#101820")
        compare.paste(reference, (0, 40))
        compare.paste(actual, (1672, 40))
        draw = ImageDraw.Draw(compare)
        draw.text((16, 12), "REFERENCE", fill="#f0dfc5")
        draw.text((1688, 12), "ACTUAL", fill="#f0dfc5")
        compare.save(compare_path, format="PNG")
        print(f"{number}: {reference_path} | {actual_path} | {compare_path}")
    print(f"OUTPUT={output}")


if __name__ == "__main__":
    main()
