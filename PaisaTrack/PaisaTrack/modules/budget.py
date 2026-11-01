from datetime import date, datetime
from .storage import DATA_DIR, BUDGET_FIELDS, read_rows, write_rows, ensure_csv


class BudgetManager:
    def __init__(self):
        self.path = DATA_DIR / "budgets.csv"
        ensure_csv(self.path, BUDGET_FIELDS)

    @staticmethod
    def current_month():
        return date.today().strftime("%Y-%m")

    def set_budget(self, category, amount, month=None):
        month = month or self.current_month()
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            raise ValueError("Month must use YYYY-MM format.")
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Budget must be greater than zero.")
        category = category.strip().title()
        if not category:
            raise ValueError("Category cannot be empty.")
        rows = self.get_all()
        updated = False
        for row in rows:
            if row["month"] == month and row["category"].lower() == category.lower():
                row["amount"] = f"{amount:.2f}"
                updated = True
                break
        if not updated:
            rows.append({"month": month, "category": category, "amount": f"{amount:.2f}"})
        write_rows(self.path, BUDGET_FIELDS, rows)

    def get_all(self):
        return read_rows(self.path, BUDGET_FIELDS)

    def get_budgets(self, month=None):
        month = month or self.current_month()
        return [row for row in self.get_all() if row["month"] == month]
