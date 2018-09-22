import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

def is_prime(n):
    if n < 2:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    length = int(n**.5) + 1
    for i in range(3, length, 2):
        if n % i == 0:
            return False

    return True

def find_prime(lst, inp):
    num = inp
    if inp == 0:
        return lst
    while inp > 0:
        if is_prime(inp):
            if num - inp != 1:
                lst.append(inp)
                return find_prime(lst, num-inp)
        inp -= 1


@app.route('/prime-sum', methods=['POST'])
def evaluate_prime():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    inputValue = data.get("input");
    lst = []
    output = find_prime(lst, inputValue)
    return jsonify(output);
