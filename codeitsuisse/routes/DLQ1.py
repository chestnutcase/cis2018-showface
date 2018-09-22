import logging

from flask import request, jsonify;
import numpy as np
from numpy.linalg import inv
from codeitsuisse import app;

logger = logging.getLogger(__name__)

def main(inputs):
    inp = np.array(inputs["input"])
    out = np.array(inputs["output"]).reshape((len(inputs["output"]), 1))
    params = inv(np.matmul(inp.transpose(), inp))
    params = np.matmul(params, inp.transpose())
    params = np.matmul(params, out)
    q = np.array(inputs["question"]).reshape(len(inputs["question"]), 1)
    answer = np.matmul(params.transpose(), q)
    return answer[0][0]
	
@app.route('/machine-learning/question-1', methods=['POST'])
def evaluate():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    result = main(data)
    logging.info("My result :{}".format(result))
    return jsonify({"answer":result});
