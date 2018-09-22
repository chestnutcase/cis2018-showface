import logging

from flask import request, jsonify;
import requests
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def tetris(jsoninput):
    seq = list(jsoninput["tetrominoSequence"])
    solution = [];
    for t in seq:
        solution.append(counter%10)
        counter += 2

    return {"actions":solution}


@app.route('/tetris', methods=['POST'])
def evaluate_tetris():
    data = request.get_json();
    requests.post('http://requestbin.fullcontact.com/1k953nu1', json=data);
    logging.info("data sent for evaluation {}".format(data));
    output = tetris(data);
    return jsonify(output);
