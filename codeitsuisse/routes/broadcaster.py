import logging

from flask import request, jsonify;
import requests;
from codeitsuisse import app;

@app.route('/broadcaster/message-broadcast', methods=['POST'])
def evaluate_broadcast_1():
    data = request.get_json();
    requests.post('http://requestbin.fullcontact.com/1o9okt61',json=data);
    inputArray = data.get("data");
    nodeNames = [];
    linkedNodes = [];
    for connection in inputArray:
        fields = connection.split("->");
        nodeA = fields[0];
        nodeB = fields[1];
        nodeAExists = False;
        nodeBExists = False;
        for existingNode in nodeNames:
            if nodeAExists and nodeBExists:
                break
            if existingNode == nodeA:
                nodeAExists = True
            if existingNode == nodeB:
                nodeBExists = True
        if not nodeAExists:
            nodeNames.append(nodeA);
        if not nodeBExists:
            nodeNames.append(nodeB);
        nodeBLinked = False;
        for existingLinkedNode in linkedNodes:
            if existingLinkedNode == nodeB:
                nodeBLinked = True;
                break;
        if(not nodeBLinked):
            linkedNodes.append(nodeB);
    rootNodes = [];
    for node in nodeNames:
        linkExists = False;
        for link in linkedNodes:
            if node == link:
                linkExists = True;
                break;
        if not linkExists:
            rootNodes.append(node);
    return jsonify({"result":rootNodes});


def most_connected(connected_input):
    datas = connected_input["data"]
    dic = {}

    for data in datas:
        sender, recevier = data.split("->")
        if sender in dic:
            dic[sender].append(recevier)
        else:
            dic[sender] = [recevier]

        if recevier in dic:
            dic[recevier].append(sender)
        else:
            dic[recevier] = [sender]

    diclist = [x for x in list(dic.items())]
    lengths = [len(x[1]) for x in diclist]
    result = diclist[lengths.index(max(lengths))][0]
    return {"result":result}


@app.route('/broadcaster/most-connected-node', methods=['POST'])
def evaluate_broadcast_2():
    data = request.get_json();
    output = most_connected(data);
    return jsonify(output);
