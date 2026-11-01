import uuid
from datetime import date, datetime
from pathlib import Path
from .storage import DATA_DIR, TRANSACTION_FIELDS, read_rows, write_rows, ensure_csv


class TransactionManager:
    def __init__(self):
        self.path = DATA_DIR / "transactions.csv"
        ensure_csv(self.path, TRANSACTION_FIELDS)

    def get_all(self):
        return read_rows(self.path, TRANSACTION_FIELDS)

    def get_by_id(self, transaction_id):
        return next((row for row in self.get_all() if row["id"] == transaction_id), None)

    def add_transaction(self, kind, title, amount, category, transaction_date=None):
        if kind not in ("income", "expense"):
            raise ValueError("Transaction type must be income or expense.")
        if not title.strip() or not category.strip():
            raise ValueError("Title and category are required.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        clean_date = transaction_date or date.today().isoformat()
        try:
            datetime.strptime(clean_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must use YYYY-MM-DD format.")
        transaction_id = uuid.uuid4().hex[:8].upper()
        rows = self.get_all()
        rows.append({
            "id": transaction_id,
            "date": clean_date,
            "type": kind,
            "title": title.strip(),
            "category": category.strip().title(),
            "amount": f"{amount:.2f}"
        })
        write_rows(self.path, TRANSACTION_FIELDS, rows)
        return transaction_id

    def update_transaction(self, transaction_id, title=None, category=None, amount=None, date=None):
        rows = self.get_all()
        found = False
        for row in rows:
            if row["id"] == transaction_id:
                found = True
                if title is not None:
                    if not title.strip():
                        raise ValueError("Title cannot be empty.")
                    row["title"] = title.strip()
                if category is not None:
                    if not category.strip():
                        raise ValueError("Category cannot be empty.")
                    row["category"] = category.strip().title()
                if amount is not None:
                    amount = float(amount)
                    if amount <= 0:
                        raise ValueError("Amount must be greater than zero.")
                    row["amount"] = f"{amount:.2f}"
                if date is not None:
                    datetime.strptime(date, "%Y-%m-%d")
                    row["date"] = date
                break
        if found:
            write_rows(self.path, TRANSACTION_FIELDS, rows)
        return found

    def delete_transaction(self, transaction_id):
        rows = self.get_all()
        remaining = [row for row in rows if row["id"] != transaction_id]
        if len(remaining) == len(rows):
            return False
        write_rows(self.path, TRANSACTION_FIELDS, remaining)
        return True
