from collections import defaultdict

zero = lambda x: 0

def transaction_simplification(expenses):
    amount_to_pay = defaultdict(zero)
    for expense in expenses:
        amount_per_user = expense.amount/ len(expense.users_involved)
        amount_to_pay[expense.payer] = amount_to_pay[expense.payer] - expense.amount_per_user
        for user in expense.users_involved:
            amount_to_pay[user] = amount_to_pay[user] + amount_per_user
    givers = dict()
    recievers = dict()
    for user, pending_amount in amount_to_pay.items():
        if pending_amount < 0: recievers[user] = pending_amount
        else: givers[user] = pending_amount
    givers = sorted(givers.items())
    recievers = sorted(recievers.items())
    iter_reciever = iter(recievers)
    pending_transactions = []
    for giver in givers:
        if(givers[giver] < )
        
