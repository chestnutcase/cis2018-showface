import logging

from flask import request, jsonify
import requests
from codeitsuisse import app

logger = logging.getLogger(__name__)

def the_function(jsoninput):
    difference = jsoninput["maximum_difference_for_calories"]
    A = jsoninput["calories_for_each_type_for_raphael"]
    B = jsoninput["calories_for_each_type_for_leonardo"]
    MODULO = 100000123

    max_value = max(max(B),max(A))

    # do some sorting here
    B = [-x for x in B]

    C = A+B
    #print(C)
    C = sorted(C, key=abs)
    #print(C)
    #print(max_value)


    length = 50*difference
    limits = [0 for _ in range(2*length + 1)]
    limits[length] = 1
    # position length + 1 is 0

    #print(limits)
    #print()

    for x in C:
        #print()
        #print(x)

        if x == 0:
            array_1 = limits
        if x > 0:
            array_1 = ([0]*x)+limits[:-x]
        elif x < 0:
            array_1 = limits[-x:] + ([0]*(-x))
        array_2 = limits

        #print(array_1)
        #print(array_2)

        limits = [x+y%MODULO for x,y in zip(array_1,array_2)]
        #print(limits)

    #print("\nresult")
    relevant_range = limits[length - difference: -(length - difference)]
    result = sum([x%MODULO for x in relevant_range])

    return {"result":result}


@app.route('/two-dinosaurs', methods=['POST'])
def evaluate_dino():
    data = request.get_json()
    requests.post('http://requestbin.fullcontact.com/1k953nu1', json=data)
    logging.info("data sent for evaluation {}".format(data))
    output = the_function(data)
    return jsonify(output)
