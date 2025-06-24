import argparse
import sys
from commands import add_expense, list_expenses, show_summary, update_expense, delete_expense, set_budget, export_expenses

DEFAULT_EXPENSES_PATH = "data/expenses.json"
DEFAULT_BUDGET_PATH = "data/budget.json"
DEFAULT_EXPORT_PATH = "data/expenses.csv"

def build_parser():

    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
            --------------------------------
                    Expense Tracker
            --------------------------------
        A simple expense tracker to manage your finances.

        Examples:
        expense-tracker add --description "Lunch" --amount 20
        expense-tracker delete --id 2
        expense-tracker list
        expense-tracker summary
        expense-tracker summary --month 8
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Options for the command')

    parser_add = subparsers.add_parser('add', help='Add a new expense')
    parser_add.add_argument('--description', required=True, type=str, help='Description for the expense')
    parser_add.add_argument('--amount', required=True, type=float, help='Amount spent')
    parser_add.add_argument('--category', type=str, help='Expense category', default=None)

    parser_delete = subparsers.add_parser('delete', help='Delete an expense')
    parser_delete.add_argument('--id', required=True, type=int, help='ID of the expense to be deleted')

    parser_list = subparsers.add_parser('list', help='List all expenses')
    parser_list.add_argument('--category', type=str, help='Filer the expenses for a specific category', default=None)

    parser_summary = subparsers.add_parser('summary', help='Show summary of expenses')
    parser_summary.add_argument('--month', type=int, choices=range(1,13), help='Filter the expenses for a specific month (of current year)')
    parser_summary.add_argument('--category', type=str, help='Filter the expenses for a specific category', default=None)

    parser_update = subparsers.add_parser('update', help='Update an existing expense')
    parser_update.add_argument('--expense_id', required=True, type=int, help='ID of the expense to be updated')
    parser_update.add_argument('--description', type=str, help='New description')
    parser_update.add_argument('--amount', type=float, help='New amount')
    parser_update.add_argument('--category', type=str, help='Expense category', default=None)

    parser_set_budget = subparsers.add_parser('set-budget', help='Set the budget for the desired month')
    parser_set_budget.add_argument('--month', required=True, type=int, help='The numeric value corresponding to the month you want to set the budget')
    parser_set_budget.add_argument('--value', required=True, type=float, help='The value for the budget')

    parser_export_expense = subparsers.add_parser('export', help='Export the expenses to a CSV file')
    parser_export_expense.add_argument('--file-path', type=str, default=DEFAULT_EXPORT_PATH, help='The path (including the file name) where you want to export the CSV file')

    for subparser in [parser_add, parser_delete, parser_list, parser_summary, parser_update, parser_set_budget, parser_export_expense]:
        subparser.add_argument('--expenses_path', type=str, default=DEFAULT_EXPENSES_PATH, help=argparse.SUPPRESS)
        subparser.add_argument('--budget_path', type=str, default=DEFAULT_BUDGET_PATH, help=argparse.SUPPRESS)

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        match args.command:
            case 'add':
                result = add_expense(args.expenses_path, args.budget_path, args.description, args.amount, args.category)
                print(result["message"])
                if result["warning"]:
                    print(result["warning"])
            case 'list':
                result = list_expenses(args.expenses_path, args.category)
                print(result)
            case 'summary':
                result = show_summary(args.expenses_path, args.month, args.category)
                print(result)
            case 'update':
                result = update_expense(args.expenses_path, args.budget_path, args.expense_id, args.description, args.amount, args.category)
                print(result["message"])
                if result["warning"]:
                    print(result["warning"])
            case 'delete':
                result = delete_expense(args.expenses_path, args.id)
                print(result)
            case 'set-budget':
                result = set_budget(args.budget_path, args.month, args.value)
                print(result)
            case 'export':
                result = export_expenses(args.expenses_path, args.file_path)
                print(result)
            case _:
                parser.print_help()
                sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()