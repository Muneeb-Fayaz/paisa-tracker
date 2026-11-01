import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .storage import CHARTS_DIR


class ChartGenerator:
    def __init__(self, analytics):
        self.analytics = analytics

    def generate_all(self, month=None):
        month = month or self.analytics.current_month()
        categories = self.analytics.expenses_by_category(month)
        if not categories:
            return []

        CHARTS_DIR.mkdir(parents=True, exist_ok=True)
        paths = []

        plt.figure(figsize=(8, 6))
        plt.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=90)
        plt.title(f"Expenses by Category — {month}")
        plt.tight_layout()
        path = CHARTS_DIR / f"category_expenses_{month}.png"
        plt.savefig(path, dpi=140)
        plt.close()
        paths.append(path)

        summary = self.analytics.summary(month)
        plt.figure(figsize=(7, 5))
        labels = ["Income", "Expenses"]
        values = [summary["income"], summary["expenses"]]
        plt.bar(labels, values)
        plt.title(f"Income vs Expenses — {month}")
        plt.ylabel("Amount (INR)")
        plt.tight_layout()
        path = CHARTS_DIR / f"income_vs_expenses_{month}.png"
        plt.savefig(path, dpi=140)
        plt.close()
        paths.append(path)

        monthly = self.analytics.monthly_totals()
        if not monthly.empty:
            plt.figure(figsize=(9, 5))
            plt.plot(monthly["month"], monthly["income"], marker="o", label="Income")
            plt.plot(monthly["month"], monthly["expenses"], marker="o", label="Expenses")
            plt.title("Monthly Income and Expenses")
            plt.xlabel("Month")
            plt.ylabel("Amount (INR)")
            plt.xticks(rotation=35)
            plt.legend()
            plt.tight_layout()
            path = CHARTS_DIR / "monthly_trend.png"
            plt.savefig(path, dpi=140)
            plt.close()
            paths.append(path)

        budgets = self._budget_data(month)
        if budgets:
            names = [row[0] for row in budgets]
            spent = [row[1] for row in budgets]
            limits = [row[2] for row in budgets]
            plt.figure(figsize=(8, 5))
            positions = range(len(names))
            plt.bar(positions, limits, label="Budget")
            plt.bar(positions, spent, label="Spent")
            plt.xticks(list(positions), names, rotation=25, ha="right")
            plt.title(f"Budget vs Spending — {month}")
            plt.ylabel("Amount (INR)")
            plt.legend()
            plt.tight_layout()
            path = CHARTS_DIR / f"budget_vs_spending_{month}.png"
            plt.savefig(path, dpi=140)
            plt.close()
            paths.append(path)

        return paths

    def _budget_data(self, month):
        from .budget import BudgetManager
        budgets = BudgetManager().get_budgets(month)
        spent_by_category = self.analytics.expenses_by_category(month)
        return [
            (row["category"], spent_by_category.get(row["category"], 0.0), float(row["amount"]))
            for row in budgets
        ]
