# 💸 PaisaTrack — Smart Personal Finance Analyzer

**PaisaTrack** is a terminal-based personal finance tracker built with Python. It helps you record income and expenses, set monthly budgets, understand spending habits and export simple financial reports.

This project is designed as a practical intermediate Python project. The code is split into small modules so it is easier to read, learn from and improve.

> PaisaTrack is an educational project. It does not connect to banks, provide financial advice or verify transactions.

## ✨ Features

- **Income and expense tracking** — add, view, edit and delete transactions.
- **CSV storage** — your records stay saved between sessions.
- **Monthly budgets** — set category-wise limits and check how much is left.
- **Financial summary** — view income, expenses, net balance, savings rate and average daily spending.
- **Spending analytics** — see how much you spend in each category.
- **Smart insights** — get simple rule-based messages based on your records and budgets.
- **Charts** — create category, income-vs-expense, monthly trend and budget comparison charts.
- **Monthly reports** — export transactions and a text summary.

## 🧰 Built With

| Tool | Why it is used |
|---|---|
| Python | Main application |
| Pandas | Working with transaction data |
| NumPy | Numerical calculations |
| Matplotlib | Charts and visual reports |
| CSV | Simple local data storage |
| Datetime | Date and month validation |

## 📁 Project Structure

```text
PaisaTrack/
│
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── transactions.csv
│   └── budgets.csv
│
├── modules/
│   ├── __init__.py
│   ├── storage.py
│   ├── transaction.py
│   ├── budget.py
│   ├── analytics.py
│   ├── insights.py
│   ├── visualization.py
│   └── reports.py
│
├── charts/       # Generated charts are saved here
└── reports/      # Exported reports are saved here
```

The `data` CSV files are created automatically the first time the app runs.

## 🚀 Getting Started

### 1. Install Python

Install Python 3.10 or newer. During installation on Windows, enable **Add Python to PATH**.

### 2. Download the project

Download this repository as a ZIP and extract it, or clone it:

```bash
git clone https://github.com/YOUR-USERNAME/PaisaTrack.git
cd PaisaTrack
```

### 3. Create a virtual environment (recommended)

**Windows CMD:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

If you use `uv`, you can install the dependencies with:

```bash
uv sync
```

For a fresh `uv` project, run `uv add pandas numpy matplotlib` first.

### 5. Run PaisaTrack

```bash
python main.py
```

Or, if you use `uv`:

```bash
uv run main.py
```

## 🖥️ Main Menu

```text
====================================================
                 PAISATRACK
          SMART PERSONAL FINANCE ANALYZER
====================================================
  1. Add income
  2. Add expense
  3. View transactions
  4. Update transaction
  5. Delete transaction
  6. Manage monthly budgets
  7. Financial summary
  8. Spending analytics
  9. Smart financial insights
 10. Generate charts
 11. Export monthly report
 12. Exit
====================================================
```

## 🧪 A Quick Test

Try entering these example records manually:

| Type | Title | Category | Amount |
|---|---|---|---:|
| Income | Monthly allowance | Income | ₹10,000 |
| Expense | Groceries | Food | ₹1,500 |
| Expense | Bus pass | Transport | ₹800 |
| Expense | Notebook | Education | ₹400 |

Then open **Financial summary** and **Spending analytics** from the menu.

These are example entries for testing only. The application does not preload made-up transactions.

## 📊 Where Files Are Saved

- Transactions: `data/transactions.csv`
- Budgets: `data/budgets.csv`
- Charts: `charts/`
- Monthly transaction exports and summaries: `reports/`

Keep a backup of the `data` folder if you want to preserve your records.

## 📝 Date Formats

- Transaction date: `YYYY-MM-DD` (example: `2026-11-01`)
- Budget/report month: `YYYY-MM` (example: `2026-11`)

If you leave a transaction date blank, today's date is used.

## 🔍 Notes and Current Limitations

- All amounts are entered in Indian rupees (₹).
- Data is stored locally in CSV files on your computer.
- This is a single-user terminal application; it does not have login accounts.
- Smart insights use simple rules, not machine learning or generative AI.
- Average daily spending is calculated across the days that contain expense records.
- Monthly charts use the transaction history available in your CSV file.

## 💡 Ideas to Improve It Later

- Add recurring transactions.
- Add a search screen with date ranges.
- Add a yearly financial summary.
- Add password-protected local profiles.
- Add unit tests with `unittest` or `pytest`.
- Add a simple desktop interface after the terminal version is stable.

## 👨‍💻 Learning Goals

Building this project gives practice with:

- Functions, classes and modules
- Reading and writing CSV files
- Input validation and exception handling
- Pandas filtering, grouping and aggregation
- NumPy calculations
- Matplotlib chart generation
- Organising a multi-file Python application

## 📄 License

This project is open for learning and personal use. Add a license file if you plan to publish it for wider reuse.

---

**Built with Python, curiosity and a little financial discipline.**
