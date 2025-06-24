# Expense Tracker

A simple command-line tool to help you manage your personal finances.  
You can add, list, update, delete expenses, and view summaries by month.

This project was implemented based on the Expense Tracker project idea from [roadmap.sh](https://roadmap.sh/projects/expense-tracker), which proposes building a command-line application to manage personal finances.

## Instalation
1. Clone the repository
```
git clone
cd expense-tracker
```

2. (Optional) Cate a virtual environment
```
python -m venv .venv

# For Windows
venv\Scripts\activate

# For Linux/MacOS
source venv/bin/activate

```

3. Run the CLI
```
python expense-tracker.py <command>
```

### Available Commands

| Command | Description |
|--------|-------------|
| `add --description <desc> --amount <amt> [--category <cat>]` | Add a new expense |
| `list` | List all expenses |
| `summary` | Show a summary of expenses |
| `summary [--month <1-12>] [--category <cat>]` | Show summary for a specific month and/or category |
| `delete --id <id>` | Delete an expense by ID |
| `update --expense_id <id> [--description <desc>] [--amount <amt>] [--category <cat>]` | Update an expense |
|`set-budget --month <1-12> --value <value>` | Set a budget to receive a warning when you exceed the budget for that month |
| `export [--file-path <file-path>]` | Export the expenses to a CSV file |

## Examples of usage

### Add a new expense

```
$ python expense-tracker.py add --description "Lunch" --amount 20
# Expense added successfully (ID: 1)
```

### Delete an expense
```
$ python expense-tracker.py delete --id 1
# Expense deleted successfully
```

### List all expenses
```
$ python expense-tracker.py list
# ID  Date    Description Amount
# 1   2024-08-06  Lunch   $20
# 2   2024-08-06  Dinner  $10
```

### View summary
```
$ python expense-tracker.py summary
# Total expenses: $30
```

### View summary by month

```
$ python expense-tracker.py summary --month 8
# Total expenses for August: $20
```

## Additional features:
### Add expense categories and filter expenses by category
```
$ python expense-tracker.py add --description "Pizza" --amount 50 --category "Delivery"                                                                                                          
# Expense added successfully (ID: 1)

$ python expense-tracker.py summary --category "Delivery"
Total expenses with Delivery: $50.00
```

### Set a budget for each month and a warning is shown the budget is exceeded
```
python expense-tracker.py set-budget --month 6 --value 100
Successfully configured the budget for month 6 (value: 100.0)

python expense-tracker.py add --description "Fancy Dinner" --amount 200
Expense added successfully (ID: 4)
[WARN] You exceeded the budget for June
```

### Export the expenses to a CSV file
```
$ python expense-tracker.py export --file-path "expenses.csv"
# The expenses were exported successfully. Path: expenses.csv
```




