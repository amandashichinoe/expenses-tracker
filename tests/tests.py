import calendar
from datetime import datetime
import io
import os
import shutil
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from commands import add_expense, list_expenses, show_summary, delete_expense, read_expenses, get_total_expenses, write_expenses

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.expenses_file_path = os.path.join(self.test_dir, "test_expenses.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_expense(self):
        # Users can add an expense with a description and amount.
        add_expense("Test Lunch", 25.90, self.expenses_file_path)
        expenses = read_expenses(self.expenses_file_path)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["description"], "Test Lunch")
        self.assertEqual(expenses[0]["amount"], 25.90)

    @unittest.skip("Not implemented yet")
    def test_update_expense(self):
        # Users can update an expense.
        pass

    def test_delete_expense(self):
        # Users can delete an expense.
        add_expense("To be deleted", 1, self.expenses_file_path)
        expenses = read_expenses(self.expenses_file_path)
        expense_id = expenses[0]["id"]
        delete_expense(expense_id, self.expenses_file_path)
        expenses = read_expenses(self.expenses_file_path)
        self.assertEqual(len(expenses), 0)

    def test_get_total_expenses(self):
        # Users can view all expenses.
        add_expense("Food", 25.50, self.expenses_file_path)
        add_expense("Transport", 10.00, self.expenses_file_path)
        expenses = read_expenses(self.expenses_file_path)

        total = get_total_expenses(expenses)
        self.assertEqual(total, 35.50)

    def test_get_summary_all_expenses(self):
        # Users can view a summary of all expenses.
        add_expense("Groceries", 20, self.expenses_file_path)
        add_expense("Utilities", 30, self.expenses_file_path)
        output = io.StringIO()
        sys.stdout = output
        show_summary(expenses_file_path=self.expenses_file_path)

        sys.stdout = sys.__stdout__
        message_displayed = output.getvalue()
        self.assertIn("Total expenses: $50.00", message_displayed)

    def test_get_summary_by_month(self):
        # Users can view a summary of expenses for a specific month (of current year).
        now = datetime.now()
        expenses = [
            {
                "id": 1,
                "date": now.strftime("%d-%m-%Y"),
                "description": "Test",
                "amount": 100.00
            },
            {
                "id": 2,
                "date": now.replace(month=1).strftime("%d-%m-%Y"),
                "description": "January Expense",
                "amount": 50.00
            },
        ]
        write_expenses(expenses, self.expenses_file_path)

        captured_output = io.StringIO()
        sys.stdout = captured_output

        show_summary(month=now.month, expenses_file_path=self.expenses_file_path)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(f"Total expenses for {calendar.month_name[now.month]}: $100.00", output)


# Additional features:
# Add expense categories and allow users to filter expenses by category.
# Allow users to set a budget for each month and show a warning when the user exceeds the budget.
# Allow users to export expenses to a CSV file.