import argparse
import sys
from commands import add_expense, list_expenses, show_summary, update_expense, delete_expense

DEFAULT_EXPENSES_PATH = "data/expenses.json"

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
    parser_add.add_argument('--amount', required=True, type=str, help='Amount spent')

    parser_delete = subparsers.add_parser('delete', help='Delete an expense')
    parser_delete.add_argument('--id', required=True, type=int, help='ID of the expense to be deleted')

    parser_list = subparsers.add_parser('list', help='List all expenses')

    parser_summary = subparsers.add_parser('summary', help='Show summary of expenses')
    parser_summary.add_argument('--month', type=int, choices=range(1,13), help='Filter the expenses for a specific month (of current year)')

    parser_update = subparsers.add_parser('update', help='Update an existing expense')
    parser_update.add_argument('--expense_id', required=True, type=int, help='ID of the expense to be updated')
    parser_update.add_argument('--description', type=str, help='New description')
    parser_update.add_argument('--amount', type=str, help='New amount')

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
                result = add_expense(args.description, args.amount, DEFAULT_EXPENSES_PATH)
                print(result)
            case 'list':
                result = list_expenses(DEFAULT_EXPENSES_PATH)
                print(result)
            case 'summary':
                result = show_summary(DEFAULT_EXPENSES_PATH, args.month)
                print(result)
            case 'update':
                description = args.description if args.description else None
                amount = args.amount if args.amount else None
                result = update_expense(DEFAULT_EXPENSES_PATH, args.expense_id, description, amount)
            case 'delete':
                result = delete_expense(args.id, DEFAULT_EXPENSES_PATH)
                print(result)
            case _:
                parser.print_help()
                sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()