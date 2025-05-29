import argparse
from commands import add_expense, list_expenses, show_summary, delete_expense


parser = argparse.ArgumentParser(
    prog="expense-tracker",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""\
        --------------------------------
                Expense Tracker
        --------------------------------
    A simple expense tracker to manage your finances
    """
)
# expense-tracker add --description "Lunch" --amount 20
subparsers = parser.add_subparsers(dest='command', help='Options for the command')

parser_add = subparsers.add_parser('add', help='Add a new expense')
parser_add.add_argument('--description', required=True, type=str, help='Description for the expense')
parser_add.add_argument('--amount', required=True, type=str, help='Amount expent')

# expense-tracker delete --id 2
parser_delete = subparsers.add_parser('delete', help='Delete an expense')
parser_delete.add_argument('--id', required=True, type=int, help='ID of the expense to be deleted')

# expense-tracker list
parser_list = subparsers.add_parser('list', help='List all expenses')

# expense-tracker summary
# expense-tracker summary --month 8
parser_summary = subparsers.add_parser('summary', help='Show summary of expenses')
parser_summary.add_argument('--month', type=int, choices=range(1,13), help='Filter the expenses for a specific month (of current year)')

args = parser.parse_args()
match args.command:
    case 'add':
        add_expense(args.description, args.amount)
    case 'list':
        list_expenses()
    case 'summary':
        show_summary(args.month)
    case 'delete':
        delete_expense(args.id)
    case _:
        parser.print_help()