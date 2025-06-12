import calendar
import json
import os
from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"

def add_expense(description, amount, expenses_path):
    if not description.strip():
        raise ValueError("Description cannot be empty.")

    amount = validate_amount(amount)
    
    expenses = read_expenses(expenses_path)
    ids = [int(key) for key in expenses.keys()]
    expense_id = max(ids, default=0) + 1
    
    expenses[str(expense_id)] = {
        "date": datetime.now().strftime(DATE_FORMAT),
        "description": description,
        "amount": float(amount)
    }

    write_expenses(expenses, expenses_path)
    message = f"Expense added successfully (ID: {expense_id})"
    return message

def update_expense(expenses_path, expense_id, description=None, amount=None):
    expenses = read_expenses(expenses_path)
    expense_id = str(expense_id)
    if expense_id not in expenses:
        raise ValueError(f"Expense with ID {expense_id} not found.")
    if description is not None:
        if not description.strip():
            raise ValueError("Description cannot be empty.")
        expenses[expense_id]["description"] = description
    if amount is not None:
        expenses[expense_id]["amount"] = validate_amount(amount)
    write_expenses(expenses, expenses_path)
    return f"Expense {expense_id} updated successfully"


def validate_amount(amount):
    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        return amount
    except ValueError as e:
        raise ValueError(f"Invalid amount: {e}")


def list_expenses(expenses_path):
    expenses = read_expenses(expenses_path)

    if not expenses:
        return "No expenses found"
    header = [f"{'ID':<4} {'Date':<12} {'Description':<15} {'Amount':<7}"]
    rows = [
        f"{expense_id:<4} {expense['date']:<12} {expense['description']:<15} ${expense['amount']:<7.2f}"
        for expense_id, expense in expenses.items()
    ]
    return "\n".join(header + rows)


def get_total_expenses(expenses, month=None):
    total = 0
    for exp in expenses.values():
        try:
            if ("date" not in exp) or ("amount" not in exp):
                continue
            expense_date = datetime.strptime(exp["date"], DATE_FORMAT)
            if (month is not None) and (expense_date.month != month):
                continue
            total += float(exp["amount"])
        except (ValueError, KeyError) as e:
            print(f'Invalid data. Skipping expense {exp}. Error: {e}')
            continue
    return round(total, 2)


def show_summary(expenses_path, month=None):
    if (month is not None) and (month < 1 or month > 12):
        return "Invalid month. Please provide a number between 1 and 12."
    expenses = read_expenses(expenses_path)
    total_expenses = get_total_expenses(expenses, month)
    if month:
        message = f"Total expenses for {calendar.month_name[month]}: ${total_expenses:.2f}"
    else:
        message = f"Total expenses: ${total_expenses:.2f}"
    return message


def delete_expense(expense_id, expenses_path):
    expenses = read_expenses(expenses_path)
    expense_id = str(expense_id)
    if expense_id in expenses:
        del expenses[expense_id]
        write_expenses(expenses, expenses_path)
        return "Expense deleted successfully"
    return f"Could not find an expense with id {expense_id}"


def read_expenses(expenses_path):
    if not os.path.exists(expenses_path):
        return {}
    try:
        with open(expenses_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise RuntimeError("Expenses file is corrupt. Please fix or delete it manually.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading file: {e}")

    
def write_expenses(expenses, expenses_path):
    try:
        with open(expenses_path, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to write the expenses: {e}")