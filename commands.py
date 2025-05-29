import calendar
import json
from datetime import datetime

EXPENSES_FILE_PATH = "data/expenses.json"
def add_expense(description, amount):
    expenses = read_expenses()
    if len(expenses) == 0:
        expense_id = 1
    else:
        expense_id = expenses[-1]["id"] + 1
    
    expenses.append({
        "id": expense_id,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "description": description,
        "amount": float(amount)
    })

    write_expenses(expenses)
    print(f"Expense added successfully (ID: {expense_id})")


def list_expenses():
    expenses = read_expenses()
    if not expenses:
        print("No expenses found")
        return None
    
    # header
    print(f"{'ID':<4} {'Date':<12} {'Description':<15} {'Amount':<7}")
    # content
    for expense in expenses:
        print(f"{expense['id']:<4} {expense['date']:<12} {expense['description']:<15} ${expense['amount']:<7.2f}")


def show_summary(month=None):
    expenses = read_expenses()
    total_expenses = 0
    if not expenses:
        print(f"Total expenses: ${total_expenses}")
        return None
    
    if month:
        for exp in expenses:
            if datetime.strptime(exp["date"], "%d-%m-%Y").month == month:
                total_expenses += exp["amount"]
            
        print(f"Total expenses for {calendar.month_name[month]}: ${total_expenses:.2f}")
    else:
        for exp in expenses:
            total_expenses += exp["amount"]
        print(f"Total expenses: ${total_expenses:.2f}")

def delete_expense(id):
    expenses = read_expenses()
    for idx in range(len(expenses)):
        expense_id = expenses[idx].get("id")
        if expense_id == id:
            del expenses[idx]
            write_expenses(expenses)
            return None     
    print(f"Could not find an expense with id {id}")


def read_expenses():
    with open(EXPENSES_FILE_PATH, "r") as file:
        return json.load(file)
    

def write_expenses(expenses):
    with open(EXPENSES_FILE_PATH, "w") as file:
        json.dump(expenses, file, indent=4)
    