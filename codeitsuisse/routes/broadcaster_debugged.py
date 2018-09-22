import logging

from flask import request, jsonify
import requests
import numpy as np
from codeitsuisse import app


def main(inputs):
    connections = inputs["data"]
    a = []
    b = []
    for connection in connections:
        fields = connection.split("->")
        a.append(fields[0])
        b.append(fields[1])

    output = set(a) - set(b)

    return list(output)


@app.route('/broadcaster/message-broadcast', methods=['POST'])
def evaluate_broadcast_1():
    data = request.get_json()
    output = main(data)
    return jsonify({"result": output})


def recursion(nodes, leaves, key):
    num = 0
    if key in leaves:
        return 1
    else:
        num += 1

    children = nodes[key]
    for i in children:
        num += recursion(nodes, leaves, i)
    return num


def main_2(inputs):
    connections = inputs["data"]

    a = []
    b = []
    nodes = {}

    for connection in connections:
        fields = connection.split("->")
        _from = fields[0]
        _to = fields[1]
        a.append(_from)
        b.append(_to)

        if _from not in nodes:
            nodes[_from] = [_to]
        else:
            nodes[_from].append(_to)

    leaves = list(set(b) - set(a))
    roots = list(set(a) - set(b))

    roots.sort()
    lst = []
    for root in roots:
        num = recursion(nodes, leaves, root)
        lst.append(num)

    lst = np.array(lst)
    _max = np.argmax(lst)
    return roots[_max]


@app.route('/broadcaster/most-connected-node', methods=['POST'])
def evaluate_broadcast_2():
    data = request.get_json()
    output = main_2(data)
    return jsonify({"result": output})
