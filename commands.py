import calendar
import json
import os
from datetime import datetime

EXPENSES_FILE_PATH = "data/expenses.json"
DATE_FORMAT = "%d-%m-%Y"

def add_expense(description, amount, expenses_file_path=EXPENSES_FILE_PATH):
    if not description.strip():
        raise ValueError("Description cannot be empty.")

    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
    except ValueError as e:
        raise ValueError(f"Invalid amount: {e}")
    
    expenses = read_expenses(expenses_file_path)
    ids = [exp.get("id", 0) for exp in expenses]
    expense_id = max(ids, default=0) + 1
    
    expenses.append({
        "id": expense_id,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "description": description,
        "amount": float(amount)
    })

    write_expenses(expenses, expenses_file_path)
    print(f"Expense added successfully (ID: {expense_id})")


def list_expenses(expenses_file_path=EXPENSES_FILE_PATH):
    expenses = read_expenses(expenses_file_path)
    if not expenses:
        print("No expenses found")
        return None
    
    # header
    print(f"{'ID':<4} {'Date':<12} {'Description':<15} {'Amount':<7}")
    # content
    for expense in expenses:
        print(f"{expense['id']:<4} {expense['date']:<12} {expense['description']:<15} ${expense['amount']:<7.2f}")


def get_total_expenses(expenses, month=None):
    total = 0
    for exp in expenses:
        try:
            expense_date = datetime.strptime(exp["date"], "%d-%m-%Y")
            if month and expense_date.month != month:
                continue
            total += float(exp["amount"])
        except (ValueError, KeyError) as e:
            print(f'Invalid data. Skipping expense {exp}. Error: {e}')
            continue
    return round(total, 2)


def show_summary(month=None, expenses_file_path=EXPENSES_FILE_PATH):
    if month is not None and (month < 1 or month > 12):
        print("Invalid month. Please provide a number between 1 and 12.")
        return None
    expenses = read_expenses(expenses_file_path)
    total_expenses = get_total_expenses(expenses, month)
    if month:
        print(f"Total expenses for {calendar.month_name[month]}: ${total_expenses:.2f}")
    else:
        print(f"Total expenses: ${total_expenses:.2f}")


def delete_expense(id, expenses_file_path=EXPENSES_FILE_PATH):
    expenses = read_expenses(expenses_file_path)
    for idx, exp in enumerate(expenses):
        if exp.get("id") == id:
            del expenses[idx]
            write_expenses(expenses, expenses_file_path)
            print("Expense deleted successfully")
            return None     
    print(f"Could not find an expense with id {id}")


def read_expenses(expenses_file_path=EXPENSES_FILE_PATH):
    if not os.path.exists(expenses_file_path):
        return []
    try:
        with open(expenses_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Failed to read the expenses because the file is corrupt.")
        choice = input("Do you want to delete the corrupt file and start a new one? (y/n)\n").strip().lower()
        if choice.startswith("y"):
            os.remove(expenses_file_path)
            print("The corrupted file was deleted successfully")
            return []
        else:
            raise RuntimeError("Operation cancelled. Please fix it manually to continue.")
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading file: {e}")

    

def write_expenses(expenses, expenses_file_path = EXPENSES_FILE_PATH):
    try:
        with open(expenses_file_path, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to write the expenses: {e}")

    