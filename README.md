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
| `add` | Add a new expense |
| `list` | List all expenses |
| `summary` | Show a summary of expenses |
| `summary --month <1-12>` | Show summary for a specific month |
| `delete --id <id>` | Delete an expense by ID |
| `update --expense_id <id> [--description <desc>] [--amount <amt>]` | Update an expense |

## Examples of usage

### Add a new expense

```
$ expense-tracker add --description "Lunch" --amount 20
# Expense added successfully (ID: 1)
```

### Delete an expense
```
$ expense-tracker delete --id 1
# Expense deleted successfully
```

### List all expenses
```
$ expense-tracker list
# ID  Date    Description Amount
# 1   2024-08-06  Lunch   $20
# 2   2024-08-06  Dinner  $10
```

### View summary
```
$ expense-tracker summary
# Total expenses: $30
```

### View summary by month

```
$ expense-tracker summary --month 8
# Total expenses for August: $20
```





