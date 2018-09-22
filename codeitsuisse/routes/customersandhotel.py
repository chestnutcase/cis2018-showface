import logging

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


def minimum_distance(arr):
    arr = sorted(arr)
#     print(arr)
    diff = [arr[i] - arr[i+1] for i in range(len(arr)-1)]
    min_dist = [min(abs(x),abs(y)) for x,y in zip(diff[:1],diff[1:])]

    result = min(abs(diff[0]),abs(diff[-1]),min(min_dist))

#     print(result)
    return {"answer": result}

def minimum_camps(lst):
    lst = sorted(lst, key=lambda k: k['pos']) 
    
    pos_arr = [a["pos"] for a in lst]
    dis_arr = [a["distance"] for a in lst]
    cleared = [False] * len(lst)
    
    
    count = 1
    location = pos_arr[0] + dis_arr[0]
#     print(location)

    for i in range(len(lst)):
#         print("compare", pos_arr[i] - dis_arr[i], location)

        if pos_arr[i] - dis_arr[i] > location:
            count += 1
            location = pos_arr[i] + dis_arr[i]
#             print(location)

#     print(count)

    return {"answer": count}


@app.route('/customers-and-hotel/minimum-distance', methods=['POST'])
def evaluate_prime():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    lst = data.get("input");
    output = minimum_distance(lst)
    return jsonify(output);

@app.route('/customers-and-hotel/minimum-camps', methods=['POST'])
def evaluate_prime():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    lst = data.get("input");
    output = minimum_camps(lst)
    return jsonify(output);
