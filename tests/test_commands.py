import calendar
from datetime import datetime
import os
import shutil
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from commands import add_expense, list_expenses, show_summary, delete_expense, read_expenses, get_total_expenses, write_expenses, update_expense

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.expenses_path = os.path.join(self.test_dir, "test_expenses.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _create_expenses(self):
        now = datetime.now()
        expenses = {
            "1": {
                "date": now.strftime("%d-%m-%Y"),
                "description": "Groceries",
                "amount": 100.00,
                "category": "Food"
            },
            "2": {
                "date": now.replace(month=1).strftime("%d-%m-%Y"),
                "description": "Fruits",
                "amount": 50.00,
                "category": "Food"
            },
            "3": {
                "date": now.strftime("%d-%m-%Y"),
                "description": "Gas",
                "amount": 200,
                "category": "Transport"
            }
        }
        write_expenses(expenses, self.expenses_path)

    def test_add_expense(self):
        # Users can add an expense with a description and amount.
        add_expense(self.expenses_path, "Test Lunch", 25.90, "Food")
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(len(expenses), 1)
        my_expense = expenses["1"]
        self.assertEqual(my_expense["description"], "Test Lunch")
        self.assertEqual(my_expense["amount"], 25.90)
        self.assertEqual(my_expense["category"], "Food")

    def test_add_expense_with_empty_description(self):
        # Users cannot add an expense with empty description
        with self.assertRaises(ValueError) as cm:
            add_expense(self.expenses_path, "   ", 10, "Test")
        self.assertIn("Description cannot be empty", str(cm.exception))

    def test_add_expense_with_negative_amount(self):
        # Users cannot add an expense with negative amount
        with self.assertRaises(ValueError) as cm:
            add_expense(self.expenses_path, "Lunch", -5, "Test")
        self.assertIn("Amount cannot be negative", str(cm.exception))

    def test_add_expense_with_invalid_amount(self):
        # Users cannot add an expense with invalid amount
        with self.assertRaises(ValueError) as cm:
            add_expense(self.expenses_path, "Dinner", "invalid", "Test")
        self.assertIn("Invalid amount", str(cm.exception))

    def test_add_expense_without_category(self):
        # Users can add an expense without the category (the category will be "Uncategorized")
        add_expense(self.expenses_path, "Test Lunch", 25.90)
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(expenses["1"]["category"], "Uncategorized")

    def test_update_expense(self):
        # Users can update an expense.
        self._create_expenses()
        response = update_expense(self.expenses_path, "1", "Dinner", 42.90)
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(expenses["1"]["description"], "Dinner")
        self.assertEqual(expenses["1"]["amount"], 42.90)
        self.assertIn("Expense updated successfully", response)

    def test_update_description(self):
        # Users can update the description of an expense
        self._create_expenses()
        response = update_expense(self.expenses_path, "1", "Dinner")
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(expenses["1"]["description"], "Dinner")
        self.assertEqual(expenses["1"]["amount"], 100.00)
        self.assertEqual(expenses["1"]["category"], "Food")
        self.assertIn("Expense updated successfully", response)

    def test_update_amount(self):
        # Users can update the amount of an expense
        self._create_expenses()
        response = update_expense(self.expenses_path, 1, amount=42.90)
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(expenses["1"]["description"], "Groceries")
        self.assertEqual(expenses["1"]["amount"], 42.90)
        self.assertIn("Expense updated successfully", response)

    def test_update_category(self):
        # Users can update the category of an expense
        self._create_expenses()
        response = update_expense(self.expenses_path, 1, category="Delivery")
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(expenses["1"]["description"], "Groceries")
        self.assertEqual(expenses["1"]["category"], "Delivery")
        self.assertIn("Expense updated successfully", response)

    def test_update_invalid_description(self):
        # Users cannot update an expense with an invalid description
        self._create_expenses()
        with self.assertRaises(ValueError) as cm:
            update_expense(self.expenses_path, 1, "   ", 42.90)
        self.assertIn("Description cannot be empty", str(cm.exception))

    def test_update_invalid_amount(self):
        # Users cannot update an expense with an invalid amount
        self._create_expenses()
        with self.assertRaises(ValueError) as cm:
            update_expense(self.expenses_path, 1, "Dinner", "invalid")
        self.assertIn("Invalid amount", str(cm.exception))
    
    def test_update_negative_amount(self):
        # Users cannot update an expense with a negative amount
        self._create_expenses()
        with self.assertRaises(ValueError) as cm:
            update_expense(self.expenses_path, 1, "Dinner", -1)
        self.assertIn("Amount cannot be negative", str(cm.exception))
    
    def test_update_without_fields(self):
        # Users must provide at least one field to be updated
        self._create_expenses()
        with self.assertRaises(ValueError) as cm:
            update_expense(self.expenses_path, 1)
        self.assertIn("At least one field (description, amount, category) must be provided", str(cm.exception))

    def test_update_invalid_id(self):
        # Users cannot update an expense if the ID does not exist
        self._create_expenses()
        with self.assertRaises(ValueError) as cm:
            update_expense(self.expenses_path, 999, "Dinner", 42.90)
        self.assertIn("Expense with ID 999 not found", str(cm.exception))

    def test_delete_expense(self):
        # Users can delete an expense.
        self._create_expenses()
        expenses = read_expenses(self.expenses_path)
        response = delete_expense(self.expenses_path, 1)
        expenses = read_expenses(self.expenses_path)
        self.assertEqual(len(expenses), 2)
        self.assertIn(f"Expense deleted successfully (ID: 1)", response)


    def test_delete_expense_with_invalid_id(self):
        # Users cannot delete an expense with invalid id
        self._create_expenses()
        response = delete_expense(self.expenses_path, 9999)
        self.assertIn("Could not find an expense with id", response)

    def test_get_summary_all_expenses(self):
        # Users can view a summary of all expenses.
        self._create_expenses()
        response = show_summary(expenses_path=self.expenses_path)
        self.assertIn("Total expenses: $350.00", response)

    def test_get_summary_by_month(self):
        # Users can view a summary of expenses for a specific month (of current year).
        now = datetime.now()
        self._create_expenses()
        response = show_summary(month=now.month, expenses_path=self.expenses_path)
        self.assertIn(f"Total expenses for {calendar.month_name[now.month]}: $300.00", response)

    def test_summary_by_category(self):
        # Users can view a summary of expenses for a specific category
        self._create_expenses()
        response = show_summary(expenses_path=self.expenses_path, category="Food")
        self.assertIn(f"Total expenses with Food: $150.00", response)

    def test_summary_by_category_and_month(self):
        # Users can view a summary of expenses for a specific month and category
        now = datetime.now()
        self._create_expenses()
        response = show_summary(month=now.month, expenses_path=self.expenses_path, category="Food")
        self.assertIn(f"Total expenses with Food for {calendar.month_name[now.month]}: $100.00", response)

    def test_list_expenses(self):
        # Users can view all expenses
        self._create_expenses()
        response = list_expenses(self.expenses_path)
        self.assertIn("Gas", response)
        self.assertIn("Transport", response)
        self.assertIn("ID", response)
        self.assertIn("Date", response)
        self.assertIn("Description", response)
        self.assertIn("Amount", response)
        self.assertIn("Category", response)


    def test_list_expenses_by_category(self):
        # Users can filter expenses by category
        self._create_expenses()
        response = list_expenses(self.expenses_path, category="Food")
        self.assertIn("Category", response)
        self.assertIn("Food", response)
        self.assertNotIn("Transport", response)

    def test_list_without_expenses(self):
        response = response = list_expenses(self.expenses_path)
        self.assertIn("No expenses found", response)



        


# Additional features:
# Add expense categories and allow users to filter expenses by category.
# Allow users to set a budget for each month and show a warning when the user exceeds the budget.
# Allow users to export expenses to a CSV file.