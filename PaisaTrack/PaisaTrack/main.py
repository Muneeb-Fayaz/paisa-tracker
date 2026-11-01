from modules.transaction import TransactionManager
from modules.budget import BudgetManager
from modules.analytics import FinanceAnalytics
from modules.insights import InsightGenerator
from modules.visualization import ChartGenerator
from modules.reports import ReportManager


def show_menu():
    print("\n" + "=" * 52)
    print("                 PAISATRACK")
    print("          SMART PERSONAL FINANCE ANALYZER")
    print("=" * 52)
    options = [
        "Add income", "Add expense", "View transactions",
        "Update transaction", "Delete transaction",
        "Manage monthly budgets", "Financial summary",
        "Spending analytics", "Smart financial insights",
        "Generate charts", "Export monthly report", "Exit"
    ]
    for number, option in enumerate(options, start=1):
        print(f" {number:2}. {option}")
    print("=" * 52)


def read_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                print("Please enter an amount greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("That doesn't look like a valid number. Try again.")


def main():
    transactions = TransactionManager()
    budgets = BudgetManager()
    analytics = FinanceAnalytics(transactions)
    insights = InsightGenerator(analytics, budgets)
    charts = ChartGenerator(analytics)
    reports = ReportManager(analytics)

    while True:
        show_menu()
        choice = input("Choose an option (1-12): ").strip()

        if choice in ("1", "2"):
            kind = "income" if choice == "1" else "expense"
            title = input("Transaction title: ").strip()
            if not title:
                print("Title cannot be empty.")
                continue
            amount = read_amount("Amount (₹): ")
            category = input("Category (e.g. Salary, Food, Travel): ").strip().title()
            if not category:
                print("Category cannot be empty.")
                continue
            date = input("Date (YYYY-MM-DD, leave blank for today): ").strip() or None
            try:
                transaction_id = transactions.add_transaction(
                    kind, title, amount, category, date
                )
                print(f"\nSaved successfully. Transaction ID: {transaction_id}")
            except ValueError as error:
                print(f"Could not save transaction: {error}")

        elif choice == "3":
            records = transactions.get_all()
            if not records:
                print("\nNo transactions yet. Add income or an expense first.")
            else:
                print("\nID       DATE        TYPE      CATEGORY          AMOUNT       TITLE")
                print("-" * 76)
                for item in records:
                    print(f"{item['id']:<8} {item['date']:<11} {item['type']:<9} "
                          f"{item['category']:<17} ₹{float(item['amount']):>9.2f}  "
                          f"{item['title']}")
                print(f"\nTotal records: {len(records)}")

        elif choice == "4":
            transaction_id = input("Enter transaction ID to update: ").strip()
            current = transactions.get_by_id(transaction_id)
            if not current:
                print("No transaction found with that ID.")
                continue
            print("Leave a field blank to keep its current value.")
            title = input(f"Title [{current['title']}]: ").strip() or current["title"]
            category = input(f"Category [{current['category']}]: ").strip().title() or current["category"]
            amount_text = input(f"Amount [{current['amount']}]: ").strip()
            date = input(f"Date [{current['date']}]: ").strip() or current["date"]
            try:
                amount = float(amount_text) if amount_text else float(current["amount"])
                transactions.update_transaction(
                    transaction_id, title=title, category=category, amount=amount, date=date
                )
                print("Transaction updated.")
            except ValueError as error:
                print(f"Update failed: {error}")

        elif choice == "5":
            transaction_id = input("Enter transaction ID to delete: ").strip()
            confirm = input("Delete this transaction? (y/n): ").strip().lower()
            if confirm == "y":
                print("Transaction deleted." if transactions.delete_transaction(transaction_id)
                      else "No transaction found.")
            else:
                print("Deletion cancelled.")

        elif choice == "6":
            print("\n1. Set or update a monthly category budget")
            print("2. View current month's budgets")
            sub = input("Choose: ").strip()
            if sub == "1":
                category = input("Category: ").strip().title()
                if not category:
                    print("Category cannot be empty.")
                    continue
                amount = read_amount("Monthly budget (₹): ")
                month = input("Month (YYYY-MM, blank for current month): ").strip() or None
                try:
                    budgets.set_budget(category, amount, month)
                    print("Budget saved.")
                except ValueError as error:
                    print(error)
            elif sub == "2":
                month = input("Month (YYYY-MM, blank for current month): ").strip() or None
                rows = budgets.get_budgets(month)
                if not rows:
                    print("No budgets set for this month.")
                else:
                    spent = analytics.expenses_by_category(month)
                    print("\nCATEGORY          BUDGET       SPENT      REMAINING")
                    for row in rows:
                        used = spent.get(row["category"], 0.0)
                        remaining = float(row["amount"]) - used
                        print(f"{row['category']:<17} ₹{float(row['amount']):>8.2f}  "
                              f"₹{used:>8.2f}  ₹{remaining:>10.2f}")
            else:
                print("Please choose 1 or 2.")

        elif choice == "7":
            month = input("Month (YYYY-MM, blank for current month): ").strip() or None
            summary = analytics.summary(month)
            print(f"\nFINANCIAL SUMMARY — {summary['month']}")
            print("-" * 42)
            print(f"Total income       : ₹{summary['income']:,.2f}")
            print(f"Total expenses     : ₹{summary['expenses']:,.2f}")
            print(f"Net balance        : ₹{summary['balance']:,.2f}")
            print(f"Savings rate       : {summary['savings_rate']:.1f}%")
            print(f"Average daily spend: ₹{summary['average_daily_spend']:,.2f}")
            if summary["highest_expense"]:
                item = summary["highest_expense"]
                print(f"Highest expense    : ₹{float(item['amount']):,.2f} ({item['title']})")
            else:
                print("Highest expense    : No expenses recorded")

        elif choice == "8":
            month = input("Month (YYYY-MM, blank for current month): ").strip() or None
            categories = analytics.expenses_by_category(month)
            if not categories:
                print("No expense data available for this month.")
            else:
                print(f"\nSPENDING BY CATEGORY — {month or analytics.current_month()}")
                for category, amount in sorted(categories.items(), key=lambda pair: pair[1], reverse=True):
                    print(f"{category:<20} ₹{amount:,.2f}")
                print(f"\nAverage transaction: ₹{analytics.average_expense(month):,.2f}")

        elif choice == "9":
            month = input("Month (YYYY-MM, blank for current month): ").strip() or None
            messages = insights.generate(month)
            print("\nSMART FINANCIAL INSIGHTS")
            print("-" * 42)
            for message in messages:
                print(f"• {message}")

        elif choice == "10":
            month = input("Month (YYYY-MM, blank for current month): ").strip() or None
            try:
                paths = charts.generate_all(month)
                if paths:
                    print("\nCharts created:")
                    for path in paths:
                        print(f" - {path}")
                else:
                    print("There is not enough expense data to create charts yet.")
            except Exception as error:
                print(f"Chart generation failed: {error}")

        elif choice == "11":
            month = input("Month (YYYY-MM, blank for current month): ").strip() or None
            try:
                path = reports.export_monthly(month)
                print(f"Report exported to: {path}")
            except Exception as error:
                print(f"Report export failed: {error}")

        elif choice == "12":
            print("\nThanks for using PaisaTrack. Keep an eye on your money!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 12.")


if __name__ == "__main__":
    main()
