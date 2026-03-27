"""
hedef.xlsx dosyasından maç bilgilerini (No, Tarih, Karşılaşma) okuyup hedef.json üretir.
index.html bu JSON ile maç isimleri ve tarihlerini yükler.
Hedef dosyasını güncelledikten sonra: python export_hedef.py
(hedef.xlsx yoksa en güncel hedef*.xlsx kullanılır, örn. hedef (7).xlsx)
"""

import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
HEDEF_JSON = BASE / "hedef.json"
NUM_MATCHES = 15


def resolve_hedef_xlsx() -> Path:
    """Önce hedef.xlsx; yoksa hedef*.xlsx içinden en son değiştirileni kullan."""
    direct = BASE / "hedef.xlsx"
    if direct.is_file():
        return direct
    candidates = [p for p in BASE.glob("hedef*.xlsx") if p.is_file()]
    if not candidates:
        return direct
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main():
    hedef_path = resolve_hedef_xlsx()
    if not hedef_path.is_file():
        raise SystemExit(f"Hedef Excel bulunamadı: {BASE / 'hedef.xlsx'} veya hedef*.xlsx")
    df = pd.read_excel(hedef_path)
    df = df.head(NUM_MATCHES)
    out = []
    for _, row in df.iterrows():
        no = row.get("No")
        if pd.isna(no):
            continue
        try:
            no = int(no)
        except (TypeError, ValueError):
            continue
        if no not in range(1, NUM_MATCHES + 1):
            continue
        tarih = row.get("Tarih")
        if pd.isna(tarih):
            tarih = "01.01.2026 20:00"
        elif hasattr(tarih, "strftime"):
            tarih = tarih.strftime("%d.%m.%Y %H:%M")
        else:
            tarih = str(tarih).strip()
        k = row.get("Karşılaşma")
        if pd.isna(k):
            k = f"Maç {no}"
        else:
            k = str(k).strip()
        out.append({"no": no, "tarih": tarih, "karsilasma": k})
    out = sorted(out, key=lambda x: x["no"])
    HEDEF_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Kaynak: {hedef_path.name}")
    print(f"hedef.json yazıldı: {len(out)} maç")


if __name__ == "__main__":
    main()
