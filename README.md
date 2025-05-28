# Expense Tracker

A simple expense tracker to manage your finances.

This project was implemented based on the Expense Tracker project idea from [roadmap.sh](https://roadmap.sh/projects/expense-tracker), which proposes building a command-line application to manage personal finances.

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





