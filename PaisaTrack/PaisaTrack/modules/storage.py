import csv
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CHARTS_DIR = ROOT_DIR / "charts"
REPORTS_DIR = ROOT_DIR / "reports"

TRANSACTION_FIELDS = ["id", "date", "type", "title", "category", "amount"]
BUDGET_FIELDS = ["month", "category", "amount"]


def ensure_directories():
    for folder in (DATA_DIR, CHARTS_DIR, REPORTS_DIR):
        folder.mkdir(parents=True, exist_ok=True)


def ensure_csv(path, fields):
    ensure_directories()
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()


def read_rows(path, fields):
    ensure_csv(path, fields)
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_rows(path, fields, rows):
    ensure_directories()
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
