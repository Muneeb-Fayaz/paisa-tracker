from datetime import datetime
import numpy as np


class InsightGenerator:
    def __init__(self, analytics, budget_manager):
        self.analytics = analytics
        self.budgets = budget_manager

    def generate(self, month=None):
        month = month or self.analytics.current_month()
        summary = self.analytics.summary(month)
        categories = self.analytics.expenses_by_category(month)
        messages = []

        if summary["income"] == 0 and summary["expenses"] == 0:
            return ["There are no records for this month yet. Add a few transactions to unlock your insights."]

        if summary["income"] > 0:
            rate = summary["savings_rate"]
            if rate >= 30:
                messages.append(f"Great work! You are keeping {rate:.1f}% of your income this month.")
            elif rate > 0:
                messages.append(f"You are saving {rate:.1f}% of your income. Try setting a small savings target.")
            else:
                messages.append("Your expenses are equal to or higher than your income. Review your flexible spending.")

        if categories:
            top_category, top_amount = max(categories.items(), key=lambda item: item[1])
            total = sum(categories.values())
            share = float(np.divide(top_amount, total)) * 100 if total else 0
            messages.append(f"{top_category} is your biggest spending category at ₹{top_amount:,.2f} ({share:.1f}% of expenses).")

        budgets = self.budgets.get_budgets(month)
        for budget in budgets:
            spent = categories.get(budget["category"], 0.0)
            limit = float(budget["amount"])
            if limit and spent >= limit:
                messages.append(f"You have crossed your {budget['category']} budget by ₹{spent - limit:,.2f}.")
            elif limit and spent >= limit * 0.8:
                messages.append(f"Careful: {budget['category']} spending has reached {spent / limit * 100:.0f}% of its budget.")

        if summary["expenses"] == 0:
            messages.append("No expenses have been recorded this month. Add them to get a more useful picture.")
        if not messages:
            messages.append("Keep recording transactions. Consistent data makes your monthly insights more useful.")
        return messages
