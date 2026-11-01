from .storage import REPORTS_DIR


class ReportManager:
    def __init__(self, analytics):
        self.analytics = analytics

    def export_monthly(self, month=None):
        month = month or self.analytics.current_month()
        frame = self.analytics.month_data(month)
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        path = REPORTS_DIR / f"transactions_{month}.csv"
        if frame.empty:
            frame = self.analytics.dataframe().head(0)
        export_frame = frame.copy()
        if "date" in export_frame.columns:
            export_frame["date"] = export_frame["date"].dt.strftime("%Y-%m-%d")
        export_frame.to_csv(path, index=False)

        summary = self.analytics.summary(month)
        summary_path = REPORTS_DIR / f"summary_{month}.txt"
        with summary_path.open("w", encoding="utf-8") as file:
            file.write(f"PAISATRACK MONTHLY REPORT — {month}\n")
            file.write("=" * 42 + "\n")
            file.write(f"Income: ₹{summary['income']:,.2f}\n")
            file.write(f"Expenses: ₹{summary['expenses']:,.2f}\n")
            file.write(f"Net balance: ₹{summary['balance']:,.2f}\n")
            file.write(f"Savings rate: {summary['savings_rate']:.1f}%\n")
        return path
