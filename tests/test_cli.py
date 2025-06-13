import os
import sys
import shutil
import json
import tempfile
import subprocess
import unittest

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.script = os.path.abspath("expense-tracker.py")
        self.test_dir = tempfile.mkdtemp()
        self.expenses_path = os.path.join(self.test_dir, "expenses.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_cli(self, args):
        command = [sys.executable, self.script] + args + ["--expenses_path", self.expenses_path]
        result = subprocess.run(command, capture_output=True, text=True)
        return result

    def test_add_expense_cli(self):
        result = self.run_cli(["add", "--description", "Lunch", "--amount", "15.5", "--category", "Food"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Expense added successfully", result.stdout)

        with open(self.expenses_path) as f:
            expenses = json.load(f)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses["1"]["description"], "Lunch")

    def test_list_expenses_cli(self):
        self.run_cli(["add", "--description", "Coffee", "--amount", "5"])
        result = self.run_cli(["list"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Coffee", result.stdout)

    def test_summary_cli(self):
        self.run_cli(["add", "--description", "Food", "--amount", "25"])
        result = self.run_cli(["summary"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Total expenses", result.stdout)

    def test_delete_expense_cli(self):
        self.run_cli(["add", "--description", "ToDelete", "--amount", "1"])
        result = self.run_cli(["delete", "--id", "1"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Expense deleted successfully", result.stdout)

    def test_update_expense_cli(self):
        self.run_cli(["add", "--description", "Old", "--amount", "10"])
        result = self.run_cli(["update", "--expense_id", "1", "--description", "New", "--amount", "20"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("updated successfully", result.stdout)

        with open(self.expenses_path) as f:
            expenses = json.load(f)
        self.assertEqual(expenses["1"]["description"], "New")
        self.assertEqual(expenses["1"]["amount"], 20.0)
