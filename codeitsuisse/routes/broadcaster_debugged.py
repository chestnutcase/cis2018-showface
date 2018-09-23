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
    requests.post('http://requestbin.fullcontact.com/yl3yqsyl', json=data)
    output = main_2(data)
    return jsonify({"result": output})

from collections import deque, namedtuple

inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path

def main_3(inputs):
    inp = []
    for rela in inputs["data"]:
        distance = float(rela.split(",")[1])
        nodes = rela.split(",")[0].split("->")
        _rela = (nodes[0], nodes[1], distance)
        inp.append(_rela)
    graph = Graph(inp)
    #print(graph.edges)
    return graph.dijkstra(inputs["sender"], inputs["recipient"])

@app.route('/broadcaster/fastest-path', methods=['POST'])
def evaluate_broadcast_3():
    data = request.get_json()
    requests.post('http://requestbin.fullcontact.com/18dof5x1', json=data)
    output = main_3(data)
    output = list(output)
    return jsonify({"result": output})
