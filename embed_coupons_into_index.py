#!/usr/bin/env python3
"""combinations_latest.csv (15 sütun) → index.html içindeki EMBEDDED_COUPON_ROWS güncellenir."""
import csv
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV_PATH = BASE / "combinations_latest.csv"
INDEX_PATH = BASE / "index.html"


def main():
    rows = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        r = csv.reader(f, delimiter=";")
        next(r)
        for row in r:
            if len(row) < 15:
                continue
            rows.append([int(str(x).strip().replace("*", "")) for x in row[:15]])
    blob = json.dumps(rows, separators=(",", ":"))
    text = INDEX_PATH.read_text(encoding="utf-8")
    pat = re.compile(
        r"(const EMBEDDED_COUPON_ROWS = )\[[\s\S]*?\](;)",
        re.MULTILINE,
    )
    m = pat.search(text)
    if not m:
        raise SystemExit("index.html içinde EMBEDDED_COUPON_ROWS bulunamadı")
    new_text = pat.sub(r"\1" + blob + r"\2", text, count=1)
    INDEX_PATH.write_text(new_text, encoding="utf-8")
    print(f"Güncellendi: {len(rows)} kupon → {INDEX_PATH.name}")


if __name__ == "__main__":
    main()
