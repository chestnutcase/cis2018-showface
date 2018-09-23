#start import
import random

"""
    tile_puzzle, an emulated sliding tile board and solver
    Copyright (C) 2012  James Heslin

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

class board():
    def __init__(self, size, grid=None):
        self.size = size
        if not grid == None:
            self.grid = grid
        else:
            self.grid = []
            numbers = []
            for element in range(1, (self.size**2)):
                numbers.append(element)
            numbers.append(0) # Drop it back in at the end
            ##print numbers
            for i in range(0, size):
                self.grid.append(numbers[size*i:size*i+size])
            ##print self.grid
            self.blank_pos = (size-1, size-1)
            ##print self.grid[self.blank_pos[0]][self.blank_pos[1]]

#         #print(self.grid)  # format is like [[5, 3, 2], [1, 6, 0], [4, 7, 8]]
        self.blank_pos = self.find_blank_pos(self.grid)
        ##print "Found blank_pos:", self.findblank_pos(self.grid)
        ##print "Actual blank_pos:", self.blank_pos

    def find_blank_pos(self, grid):
        for i in range(len(grid[0])):
            for j in range(len(grid)):
                if grid[i][j] == 0:
                    return (i, j)
        #print "Couldn't find the blank tile."
        return (0, 0)

    def copy_grid(self):
        l = []
        for i in list(self.grid):
            e = (list(i))
            l.append(e)
        ##print l
        return l

    def get_legal_moves(self):
        moves = []
        for i in range(0, 4):
            if self.is_valid_move(i):
                b = board(self.size, self.copy_grid())
                b.move_blank(i)
                moves.append(b)
        ##print moves
        return moves

    def is_same_grid(self, board):
        if not self.size == board.size:
            return False
        for i in range(0, self.size):
            for j in range(0, self.size):
                if not self.grid[i][j] == board.grid[i][j]:
                    return False
        return True

    def get_blank_pos(self):
        return self.blank_pos

    def show_board(self):
        for i in self.grid:
            line = "|"
            for j in i:
                if j < 10:
                    line += " "
                line += str(j)
                line += "|"
            #print line
        #print ""

    def is_valid_move(self, direction):
        if direction == 3: # up
            if self.blank_pos[0] < 1:
                return False
            else:
                ##print ("Can move up from", str(self.blank_pos[0]),
                    #str(self.blank_pos[1]))
                return True
        elif direction == 2: # right
            if self.blank_pos[1] > self.size-2:
                return False
            else:
                ##print ("Can move right from", str(self.blank_pos[0]),
                    #str(self.blank_pos[1]))
                return True
        elif direction == 1: # down
            if self.blank_pos[0] > self.size-2:
                return False
            else:
                ##print ("Can move down from", str(self.blank_pos[0]),
                    #str(self.blank_pos[1]))
                return True
        elif direction == 0: # left
            if self.blank_pos[1] < 1:
                return False
            else:
                ##print ("Can move left from", str(self.blank_pos[0]),
                    #str(self.blank_pos[1]))
                return True

    def tiles_out_of_place(self, goal):
        t = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] is not goal.grid[i][j]:
                    t += 1
        return t

    def set_grid(self, grid):
        self.grid = grid
        self.blank_pos = self.find_blank_pos(grid)

    def moves_to_state(self, goal):
        m = 0
        tiles = []
        # Check which tiles are out of place compared to the goal state
        for i in range(self.size):
            for j in range(self.size):
                if not self.grid[i][j] == goal.grid[i][j]:
                    tiles.append((i, j, goal.grid[i][j], 0))
        # Find the Manhattan distance between goal and actual position
        # of those tiles and add it to m
        i_diff = 0
        j_diff = 0
        for t in tiles:
            for i in range(self.size):
                for j in range(self.size):
                    if self.grid[i][j] == t[2]:
                        if i > t[0]:
                            i_diff = i - t[0]
                        else:
                            i_diff += t[0] - i
                        if j > t[1]:
                            j_diff += j - t[1]
                        else:
                            j_diff += t[1] - j
                        """# is this a corner tile?
                        if ((i == 0 and j == 0) or
                                (i == self.size and j == 0) or
                                (i == 0 and j == self.size) or
                                (i == self.size and j == self.size)):
                            m += 1"""
                        ##print i_diff, j_diff
                        m += i_diff
                        m += j_diff
                        ##print m
        return m


    def move_blank(self, direction): # 3: up 2: right 1: down 0: left
        #if self.is_valid_move(direction):
        bP = self.blank_pos
        ##print bP
        if direction == 0: # left
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]][bP[1]-1])
            self.grid[bP[0]][bP[1]-1] = 0
            self.blank_pos = (bP[0], bP[1]-1)

        elif direction == 1: # down
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]+1][bP[1]])
            self.grid[bP[0]+1][bP[1]] = 0
            self.blank_pos = (bP[0]+1, bP[1])

        elif direction == 2: # right
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]][bP[1]+1])
            self.grid[bP[0]][bP[1]+1] = 0
            self.blank_pos = (bP[0], bP[1]+1)

        elif direction == 3: # up
            self.grid[bP[0]][bP[1]] = (self.grid
                [bP[0]-1][bP[1]])
            self.grid[bP[0]-1][bP[1]] = 0
            self.blank_pos = (bP[0]-1, bP[1])
        #self.show_board()
        ##print bP, "->", self.blank_pos
        ##print

    def randomise(self, iterations):
        num = 0
        states = [] # Keep track of moves made
        state_done = False # Whether currently considered move has been made
        #print "Randomising:", iterations, "iterations"
        while num < iterations:
            state_done = False
            move = random.choice(self.get_legal_moves()) # Get random move
            if self.size > 2:
                for s in states: # Step through states
                    if move.is_same_grid(s): # Has this move been made?
                        num = states.index(s) + 2
                        # Can have made a max of two moves since then
                        state_done = True # Set flag

            # If this move hasn't been made
            if not state_done:
                states.append(move) # Add it to the list of moves made
                self.set_grid(move.grid) # Set current board state to that
                num += 1 # Increment number of moves made
            ##print num
        for s in states:
            s.show_board()

def main():
    # Test the board class
    b = board(3)
    b.show_board()
    b.randomise(50)
    c = board(b.size, b.copy_grid())
    c.show_board()
    #print c.is_same_grid(b)
    #print c.get_legal_moves()

if __name__ == "__main__":
    main()


#end import

from flask import request, jsonify
from codeitsuisse import app
import numpy as np
import sys
import getopt

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
        solution_array.append(int(str(moves))) # because the top left grid is zero
        step.show_state()
        last_step = step.state.grid
    # steps includes the goal as well so -1 is the moves
    #print "Did it in", len(steps)-1, "moves."
    return {"result": solution_array}


@app.route('/sorting-game', methods=['POST'])
def evaluate_sorting():
    data = request.get_json()
    output = main_main(data)
    return jsonify(output)
