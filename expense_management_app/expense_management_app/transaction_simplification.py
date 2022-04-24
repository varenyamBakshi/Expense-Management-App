from collections import defaultdict

def zero():
    return 0

def transaction_simplification(expenses, user):
    output = {}
    for expense in expenses:
        if expense.settled_expense: continue
        expense_num_members = len(expense.users_involved.all())
        expense_amount_per_person = expense.amount / expense_num_members

        for user in expense.users_involved.all():
            if user == expense.payer:
                continue
            else:
                if expense.payer not in output:
                    output[expense.payer] = {}
                if user not in output:
                    output[user] = {}
                if user not in output[expense.payer]:
                    output[expense.payer][user] = 0
                if expense.payer not in output[user]:
                    output[user][expense.payer] = 0

                output[expense.payer][user] += expense_amount_per_person # payer gains the money
                output[user][expense.payer] -= expense_amount_per_person # user gives the payer

        print("Expense info for " + user)
        for member in output[user]:
            amount = output[user][member]
            if amount > 0:
                print("You should take from " + member + " this much amount = " + str(amount))
            elif amount < 0:
                print("You should give " + member + " this much amount = " + str(-amount))
            
        print()

        