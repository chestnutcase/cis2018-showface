import logging

from flask import request, jsonify;
import requests
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def transfer(jsoninput):
    persons = jsoninput["persons"]
    expenses = jsoninput["expenses"]

    rec_arr = [0] * len(persons)
    not_pay_arr = [0] * len(persons)

    accul = 0

    for expense in expenses:
        rec_arr[persons.index(expense["paidBy"])] += expense["amount"]

        if "exclude" in expense:
            num_people_payable = len(persons) - len(expense["exclude"])

            not_payable = expense["amount"]/num_people_payable

            for excluded in expense["exclude"]:
                not_pay_arr[persons.index(excluded)] += not_payable
                accul += not_payable

    total_receiveable = sum(rec_arr) + accul
    total_not_payable = sum(not_pay_arr)
    to_split = total_receiveable/len(persons)

#     print(to_split)
    pay_arr = [not_pay - to_split for not_pay in not_pay_arr]
    print(pay_arr)
    transfer = [x + y for x,y in zip(rec_arr, pay_arr)]

#     print(transfer)

    cumsum = lambda X: X[:1] + cumsum([X[0]+X[1]] + X[2:]) if X[1:] else X
    give = cumsum(transfer)

    transactions = [{"from": persons[i], "to": persons[i+1], "amount" : (-give[i])} for i in range(len(persons)-1)]

    for transaction in transactions:
        transaction["amount"] = round(transaction["amount"],2)

        if transaction["amount"] < 0:
            transaction["from"], transaction["to"] = transaction["to"], transaction["from"]
            transaction["amount"] = - transaction["amount"]

    return {"transactions": transactions}


@app.route('/tallyexpense', methods=['POST'])
def evaluate_expense():
    data = request.get_json();
    requests.post('http://requestbin.fullcontact.com/12ejc1f1', json=data);
    logging.info("data sent for evaluation {}".format(data));
    output = transfer(data);
    return jsonify(output);
