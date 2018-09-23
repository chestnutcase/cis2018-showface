import numpy as np
import sys
import getopt
from board import *

class a_star_node():
    def __init__(self, state, h_val, path=None):
        self.state = state
        self.h_val = h_val
        if not path == None:
            self.path = path
        self.path = []

    def get_children(self, depth):
        """Return a collection of the child states available"""
        pass

    def get_state(self):
        """Return the current state"""
        return self.state

    def state_in_list(state, c_list):
        """Check if state is in a given list"""
        pass

    def show_state(self):
        """Show the state"""
        pass

    def equals(self, node):
        """Check if this state matches node's state"""
        pass


class tile_puzzle_a_star_node(a_star_node):
    def get_children(self, depth):
        m = self.state.get_legal_moves()
        c = []
        for l in m:
            c.append(tile_puzzle_a_star_node(l, depth))
        return c

    def show_state(self):
        self.state.show_board()

    def equals(self, node):
        if self.state.is_same_grid(node.state):
            return True
        else:
            return False


class a_star_solver():
    def state_in_list(self, state, c_list):
        for c in c_list:
            if c.equals(state):
                return c
        return None

    def remove_non_optimal(self, open_list, depth):
        # This always seems to remove too many nodes
        if len(open_list) == 0:
            return
        else:
            for x in open_list:
                if (x.h_val - depth) > (depth * 4):
                    open_list.remove(x)

    def sort_open(self, open_list):
        if len(open_list) == 0:
            return
        else:
            base = open_list[0].h_val
            # get lowest h_val
            for x in open_list:
                if base < x.h_val:
                    base = x.h_val
            for i in open_list:
                if i.h_val > base:
                    open_list.remove(i)
                    open_list.append(i)

    def evaluate(self, board, goal, depth):
        board.h_val = depth
        #board.h_val += board.get_state().tiles_out_of_place(
                #   goal.get_state())
        board.h_val += board.get_state().moves_to_state(
                goal.get_state())

    def a_star(self, start, goal):
        open_list = [start] # Set initial state of open
        out_of_place = start.get_state().tiles_out_of_place(
                goal.get_state())
        #print "Tiles out of place:", out_of_place
        #print "Isolated moves from goal state:", (
        start.get_state().moves_to_state(goal.get_state())
        closed_list = [] # Set initial state of closed
        depth = 0
        count = 0
        while len(open_list) > 0: # While the open list has elements
            x = open_list.pop(0) # Pop the first element (x) off it
            if len(x.path) > depth: # Keep an eye on the depth
                depth = len(x.path)
                #print("depth")
                #print depth # #print the depth to measure progress
            if x.equals(goal): # If we've reached the goal state
                # Return path from start to x
                #print "Found it after", depth, "moves"
                #print "Total children added to open list:", count
                #print ""
                return x.path + [x]
            else:
                # Get a list of x's children
                children = x.get_children(depth)
                for c in children:
                    # If c is already in one or other of the lists
                    child_open = self.state_in_list(c, open_list)
                    child_closed = self.state_in_list(c, closed_list)
                    # If c is already in open_list
                    if child_open is not None:
                        # If child's path length < c's path length
                        if len(child_open.path) < len(c.path):
                            # Give child c's path
                            child_open.path = c.path
                    # If child is already in closed_list
                    elif child_closed is not None:
                        # If child's path length < c's path length
                        if len(child_closed.path) < len(c.path):
                            # Take child off closed list
                            closed_list.remove(child_closed)
                            # Add child to open list
                            open_list.append(child_closed)
                    # If child isn't in either list
                    else:
                        self.evaluate(c, goal, depth) # Evaluate child
                        open_list.append(c) # Add it to the open list
                        count += 1
                        p = x.path[:] # Get x's path
                        p.extend(c.path[:]) # Add c's path to it
                        c.path = p # Set c's path to that
                        c.path.append(x) # Add x to the end of c's path
            closed_list.append(x) # Add x to the closed list
            self.sort_open(open_list) # Sort the open list

def solver_find_blank_pos(grid):
    for i in range(len(grid[0])):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                return (i, j)
            


def main_main(jsoninput):
    puzzle = jsoninput["puzzle"]
    
    b = board(len(puzzle))
    c = board(len(puzzle), puzzle)
#     c = board(b.size, b.copy_grid())
#     #print(c.show_board())
#     c.randomise(random_iter)
    b_node = tile_puzzle_a_star_node(b, 0)
    c_node = tile_puzzle_a_star_node(c, 0)
    ##print "start:", b_node
    ##print "goal:", c_node
    solver = a_star_solver()
    steps = solver.a_star(c_node, b_node)
    steps[0].show_state()

    solution_array = []
    steps_less_start = steps[1:] # Don't #print the start state
    last_step = puzzle
    for step in steps_less_start:
        moved_grid = solver_find_blank_pos(step.state.grid)
        moved_grid_number = 3*moved_grid[0]+moved_grid[1]
        grid = np.array(last_step).flatten()
        moves = grid[moved_grid_number]
        solution_array.append(moves) # because the top left grid is zero
        step.show_state()
        last_step = step.state.grid
    # steps includes the goal as well so -1 is the moves
    #print "Did it in", len(steps)-1, "moves."
    return {"result": solution_array}


@app.route('/sorting-game', methods=['POST'])
def evaluate_sorting():
    data = request.get_json()
    requests.post('http://requestbin.fullcontact.com/1k953nu1', json=data)
    logging.info("data sent for evaluation {}".format(data))
    output = main_main(data)
    return jsonify(output)

