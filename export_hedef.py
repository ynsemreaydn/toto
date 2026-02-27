"""
hedef.xlsx dosyasından maç bilgilerini (No, Tarih, Karşılaşma) okuyup hedef.json üretir.
index.html bu JSON ile maç isimleri ve tarihlerini yükler.
Hedef dosyasını güncelledikten sonra: python export_hedef.py
"""

import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent
HEDEF_XLSX = BASE / "hedef.xlsx"
HEDEF_JSON = BASE / "hedef.json"
NUM_MATCHES = 15


def main():
    df = pd.read_excel(HEDEF_XLSX)
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
    print(f"hedef.json yazıldı: {len(out)} maç")


if __name__ == "__main__":
    main()
