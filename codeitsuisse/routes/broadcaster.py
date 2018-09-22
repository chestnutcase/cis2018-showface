import logging

from flask import request, jsonify;

from codeitsuisse import app;

@app.route('/broadcaster/message-broadcast', methods=['POST'])
def evaluate_broadcast_1():
    data = request.get_json();
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
            if nodeAExists && nodeBExists:
                break
            if existingNode == nodeA:
                nodeAExists = True
            if existingNode == nodeB:
                nodeBExists = True
        if !nodeAExists:
            nodeNames.append(nodeA);
        if !nodeBExists:
            nodeNames.append(nodeB);
        nodeBLinked = False;
        for existingLinkedNode in linkedNodes:
            if existingLinkedNode == nodeB:
                nodeBLinked = True;
                break;
        if(!nodeBLinked):
            linkedNodes.append(nodeB);
    rootNodes = [];
    for node in nodeNames:
        linkExists = False;
        for links in linkedNodes:
            if node == linkedNodes:
                linkExists = True;
                break;
        if linkExists:
            rootNodes.append(node);
    return jsonify({"result":rootNodes});
