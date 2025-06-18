import csv
import json
import sys
from pathlib import Path

def csv_to_json(csv_path, json_path):
    with csv_path.open(newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(rows)} rows -> {json_path}")

def main():
    csv_file = Path(sys.argv[1]).expanduser().resolve()
    json_file = Path(sys.argv[2]).expanduser().resolve()

    csv_to_json(csv_file, json_file)

if __name__ == "__main__":
    main()
