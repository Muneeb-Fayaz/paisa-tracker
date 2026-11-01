from datetime import date
import pandas as pd


class FinanceAnalytics:
    def __init__(self, transaction_manager):
        self.transactions = transaction_manager

    @staticmethod
    def current_month():
        return date.today().strftime("%Y-%m")

    def dataframe(self):
        rows = self.transactions.get_all()
        columns = ["id", "date", "type", "title", "category", "amount"]
        frame = pd.DataFrame(rows, columns=columns)
        if frame.empty:
            frame["amount"] = pd.to_numeric(frame["amount"], errors="coerce")
            return frame
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
        frame["amount"] = pd.to_numeric(frame["amount"], errors="coerce").fillna(0)
        frame["type"] = frame["type"].str.lower()
        return frame

    def month_data(self, month=None):
        month = month or self.current_month()
        frame = self.dataframe()
        if frame.empty:
            return frame
        return frame[frame["date"].dt.strftime("%Y-%m") == month].copy()

    def expenses_by_category(self, month=None):
        frame = self.month_data(month)
        if frame.empty:
            return {}
        expenses = frame[frame["type"] == "expense"]
        if expenses.empty:
            return {}
        return expenses.groupby("category")["amount"].sum().to_dict()

    def average_expense(self, month=None):
        frame = self.month_data(month)
        if frame.empty:
            return 0.0
        expenses = frame[frame["type"] == "expense"]
        return float(expenses["amount"].mean()) if not expenses.empty else 0.0

    def summary(self, month=None):
        month = month or self.current_month()
        frame = self.month_data(month)
        if frame.empty:
            income = expenses = 0.0
            highest = None
            active_days = 0
        else:
            income = float(frame.loc[frame["type"] == "income", "amount"].sum())
            expense_frame = frame[frame["type"] == "expense"]
            expenses = float(expense_frame["amount"].sum())
            highest = expense_frame.loc[expense_frame["amount"].idxmax()].to_dict() if not expense_frame.empty else None
            active_days = max(1, expense_frame["date"].dt.date.nunique()) if not expense_frame.empty else 0
        balance = income - expenses
        savings_rate = (balance / income * 100) if income > 0 else 0.0
        return {
            "month": month, "income": income, "expenses": expenses,
            "balance": balance, "savings_rate": savings_rate,
            "average_daily_spend": expenses / active_days if active_days else 0.0,
            "highest_expense": highest
        }

    def monthly_totals(self):
        frame = self.dataframe()
        if frame.empty:
            return pd.DataFrame(columns=["month", "income", "expenses"])
        frame["month"] = frame["date"].dt.strftime("%Y-%m")
        grouped = frame.pivot_table(
            index="month", columns="type", values="amount", aggfunc="sum", fill_value=0
        )
        for column in ("income", "expense"):
            if column not in grouped:
                grouped[column] = 0.0
        grouped = grouped.rename(columns={"expense": "expenses"})
        return grouped[["income", "expenses"]].reset_index().sort_values("month")
