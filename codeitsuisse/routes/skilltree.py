import logging

from flask import request, jsonify;
import copy
import numpy as np
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def check(trees, target):
    points_lst = []
    counts_lst = []
    for count, state in enumerate(trees):
        if state[1] >= target:
            points_lst.append(state[0])
            counts_lst.append(count)
    if points_lst == []:
        return None
    index = counts_lst[np.argmin(points_lst)]
    return trees[index][2]

def main(inputs):
    target = inputs["boss"]["offense"]
    trees = []
    for dit in inputs["skills"]:
        if type(dit["require"]) != str:
            state = [0, 0]
            state[0] += dit["points"]
            state[1] += dit["offense"]
            lst = [dit["name"]]
            state.append(lst)
            trees.append(state)
            
    checkpoint = check(trees, target)
    if checkpoint != None:
        return checkpoint
    
    while True:
        new_trees = []
        for dit in inputs["skills"]:
            for state in trees:
                if dit["require"] in state[2] and dit["name"] not in state[2]:
                    tree = copy.deepcopy(state)
                    tree[0] += dit["points"]
                    tree[1] += dit["offense"]
                    tree[2].append(dit["name"])
                    print(tree)
                    new_trees.append(tree)
        trees = copy.deepcopy(new_trees)
        checkpoint = check(new_trees, target)
        if checkpoint != None:
            return checkpoint

@app.route('/skill-tree', methods=['POST'])
def evaluate_skilltree():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = main(data)
    logging.info("My result :{}".format(result))
    return jsonify(result);
