
# coding: utf-8


# In[1]:


cells = [
    # I
    [
        [(0,0), (0,1), (0,2), (0,3)],
        [(0,0), (1,0), (2,0), (3,0)],
        [(0,0), (0,1), (0,2), (0,3)],
        [(0,0), (1,0), (2,0), (3,0)]
    ],

    # j
    [
        [(0,0), (1,0), (1,1), (1,2)],
        [(0,0), (0,1), (1,0), (2,0)],
        [(0,0), (0,1), (0,2), (1,2)],
        [(0,1), (1,1), (2,1), (2,0)]
    ],

    # L
    [
        [(0,0), (1,0), (0,1), (0,2)],
        [(0,0), (0,1), (1,1), (2,1)],
        [(0,2), (1,2), (1,1), (1,0)],
        [(0,0), (1,0), (2,0), (2,1)]
    ],


    # O
    [
        [(0,0), (0,1), (1,0), (1,1)],
        [(0,0), (0,1), (1,0), (1,1)],
        [(0,0), (0,1), (1,0), (1,1)],
        [(0,0), (0,1), (1,0), (1,1)]
    ],

    # S
    [
        [(0,0), (1,0), (1,1), (2,1)],
        [(0,2), (0,1), (1,1), (1,0)],
        [(0,1), (1,1), (1,0), (2,0)],
        [(0,0), (0,1), (1,1), (1,2)]
    ],

    # T
    [
        [(0,1), (1,1), (1,0), (2,1)],
        [(0,1), (1,1), (1,0), (1,2)],
        [(0,0), (1,0), (2,0), (1,1)],
        [(0,0), (0,1), (0,2), (1,1)]
    ],

    # Z
    [
        [(0,1), (1,1), (1,0), (2,0)],
        [(0,0), (0,1), (1,1), (1,2)],
        [(0,0), (1,0), (1,1), (2,1)],
        [(0,2), (0,1), (1,1), (1,0)]
    ]
]


# In[2]:


bases = []
for cell in cells:
    cell_bases = []
    for orientation in cell:
        base_line = [4,4,4,4]
        for point in orientation:
            if point[1] < base_line[point[0]]:
                base_line[point[0]] = point[1]
        base_points = []
        for i,base in enumerate(base_line):
            if base != 4:
                base_points.append((i,base))
        cell_bases.append(base_points)
    bases.append(cell_bases)


# In[3]:


widths = []
for cell in cells:
    cell_widths = []
    for orientation in cell:
        width = 0
        for point in orientation:
            if point[0] > width:
                width = point[0]
        cell_widths.append(width)
    widths.append(cell_widths)


# In[ ]:


# from p#print import p#print as pp
from copy import deepcopy as d
# import matplotlib.pyplot as plt
"""
def ps(game_state): # plot state
    plt.figure(figsize=(2,4))
    plt.axis([-1, 10, -1, 21])
    for i, row in enumerate(game_state):
        for j, col in enumerate(row):
            if game_state[i][j] == 1:
                plt.scatter(j,i)
    plt.show()
"""

# In[ ]:


game_state = [[0] * 10 for _ in range(20)]
game_state_empty = d(game_state)

# game_state[0] = [1]*10
# game_state[1][1] = 1  # y then x
# game_state[1][2] = 1
# game_state[1][3] = 1
# game_state[2][2] = 1
# game_state[2][3] = 1
# # game_state[5][5] = 1

# # game_state[10] = [1]*10
# # game_state[11] = [1,0,1,0,1,0,1,0,1,0]

# game_state_x = d(game_state)


# In[ ]:


game_state_p = [
     [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
     [1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# In[ ]:


# pp(game_state_p)


# In[ ]:


# ps(game_state_x)


# In[ ]:


def resolve_rows(game_state):
    game_state = d(game_state)
    rows_to_remove = []
    for i,row in enumerate(game_state):
        if row == [1]*10:
            rows_to_remove.append(i)

    for row_num in rows_to_remove[::-1]:
        del game_state[row_num]

    for _ in range(len(rows_to_remove)):
        game_state.append([0]*10)

    return game_state


# In[ ]:


# ps(resolve_rows(d(game_state)))


# In[ ]:


def calcuate_roof(game_state):
    game_state = d(game_state)
    columns = list(zip(*game_state))
#     #print(columns)
    return [-column[::-1].index(max(column)) % 20 for column in columns]


# In[ ]:


# calcuate_roof(game_state)


# In[ ]:


def calculate_holes(game_state):
    game_state = d(game_state)

#     #print("calculate_holes")
#     pp(game_state)

    difference_state = []
    for row_num in range(len(game_state)-1):
        row_difference = [x-y for x,y in zip(game_state[row_num], game_state[row_num+1])]
        difference_state.append(row_difference)

    number_of_holes = sum([i.count(-1) for i in difference_state])

#     pp(difference_state)
#     #print(number_of_holes)

    return number_of_holes


# In[ ]:


# #print(calculate_holes(game_state))


# In[ ]:


def calculate_borders(game_state):
#     ps(game_state)
    game_state = d(game_state)
    borders = 0

    for row in game_state:
        borders += 10*[y-x for x,y in zip(row[1:], row[:-1])].count(-1)
        borders += 10*[y-x for x,y in zip(row[:-1], row[1:])].count(-1)

    for i,row in enumerate(game_state[:-1]):
        borders += [x-y for x,y in zip(row[1:], game_state[i+1][:-1])].count(-1)
        borders += [x-y for x,y in zip(row[:-1], game_state[i+1][1:])].count(-1)

    for i,row in enumerate(game_state[:-2]):
        borders += [x-y for x,y in zip(row[1:], game_state[i+2][:-1])].count(-1)
        borders += [x-y for x,y in zip(row[:-1], game_state[i+2][1:])].count(-1)

    for i,row in enumerate(game_state[:-3]):
        borders += [x-y for x,y in zip(row[1:], game_state[i+3][:-1])].count(-1)
        borders += [x-y for x,y in zip(row[:-1], game_state[i+3][1:])].count(-1)

    for i,row in enumerate(game_state[:-4]):
        borders += 10*[x-y for x,y in zip(row[1:], game_state[i+4][:-1])].count(-1)
        borders += 10*[x-y for x,y in zip(row[:-1], game_state[i+4][1:])].count(-1)

    return borders


# In[ ]:


# pp(calculate_borders(game_state))


# In[ ]:


def add_element(game_state, block_char):
    game_state = d(game_state)
    # this is to try out all rotations (and then location)

    blocks = list("IJLOSTZ")
    block = blocks.index(block_char)

    scores = []
    moves = []

    for rotate in range(4):
        score, move = move_element(game_state, block, rotate)
        scores.append(score)
        moves.append(move)

    the_rotate = scores.index(min(scores))
    the_move = moves[the_rotate]

    game_state, score = drop_element(d(game_state), block, the_rotate, the_move, update=True)
    #print("hole_score: ", calculate_holes(game_state))

#     game_state = resolve_rows(d(game_state))
#     #print("add :", scores)

    return game_state, 10*the_rotate + the_move, score


# In[ ]:


def move_element(game_state, block, rotate):
    game_state = d(game_state)
    # this is to try out all location given block and rotation

    scores = []

#     ps(game_state)

    for move in range(10-widths[block][rotate]):
        scores.append(drop_element(game_state, block, rotate, move))

    move = scores.index(min(scores))
#     #print("move :", scores)

    return min(scores),move


# In[ ]:


def drop_element(game_state, block, rotate, move, update=False):
    game_state = d(game_state)
    # this is to calculate the dropdown and how good it is

    block_cells = cells[block][rotate]
    block_bases = bases[block][rotate]

#     #print(block_cells)
#     #print(block_bases)

    height = calculate_drop_height(game_state, block, rotate, move)

    for point in block_cells:
        if point[1]+height >= 19:
            #print("OVERFLOW")


        if game_state[point[1]+height][point[0]+move] != 0:  # row then column
            #print("ERROR")
            #print(point[1]+height, point[0]+move)
            #print(game_state[point[1]+height][point[0]+move])

#         #print(point[1]+height, point[0]+move)
#         #print(game_state[point[1]+height][point[0]+move])
        game_state[point[1]+height][point[0]+move] = 1

#         if update:
#             #print([point[1]+height],[point[0]+move])



    score = 100000*calculate_holes(game_state) + calculate_borders(game_state)
    # discourages (especially) overhang and borders

    if update:
        return game_state, score

    return score


# In[ ]:


def calculate_drop_height(game_state, block, rotate, move):
    game_state = d(game_state)
    block_bases = bases[block][rotate]
    block_base_line = [point[1] for point in block_bases]
#     #print(block_base_line)
    roof = calcuate_roof(game_state)

    relevant_roof = [roof[i+move] for i in range(len(block_base_line))]

#     #print(block_base_line)
#     #print(relevant_roof)

    difference = [(100*(x-y) - x) for x,y in zip(relevant_roof,block_base_line)]
    index = difference.index(max(difference))

    return relevant_roof[index]  # because do not add to existing space


# In[ ]:


# calculate_drop_height(d(game_state_p), 4, 3, 3)


# In[ ]:


# ps(game_state_p)
# game_state, score = drop_element(d(game_state_p), 5, 2, 5, update=True)
# # game_state = drop_element(game_state, 5, 3, 0, update=False)
# ps(game_state)
# #print(score)


# ### add element

# In[ ]:


# game_state, action, score = add_element(game_state_p, "T")
# ps(game_state)


# In[ ]:


# ps(game_state)
# game_state, action, score = add_element(game_state, "T")
# game_state = resolve_rows(game_state)
# #print("score :", score)
# ps(game_state)


# # The game

# In[ ]:


def the_function(jsoninput):
    blockchain = jsoninput["tetrominoSequence"]
    movechain = []
    game_state = d(game_state_empty)
    for block in list(blockchain):
        game_state, action, score = add_element(game_state, block)
        game_state = resolve_rows(game_state)
        movechain.append(action)
        #print("score:", score)
    #     pp(game_state)
    #    ps(game_state)
    return {"actions":movechain}


# In[ ]:


# json_input = {"tetrominoSequence": "IOJLLLTIOOTIOTZSTTTLLIJSZTIT"}
# #print(the_function(json_input))


# # Game declaration

# In[ ]:


import logging

from flask import request, jsonify
import requests
from codeitsuisse import app

logger = logging.getLogger(__name__)


def tetris(jsoninput):
    seq = list(jsoninput["tetrominoSequence"])
    solution = []
    counter = 0
    for t in seq:
        solution.append(counter % 10)
        counter += 2

    return {"actions": solution}


@app.route('/tetris', methods=['POST'])
def evaluate_tetris():
    data = request.get_json()
    requests.post('http://requestbin.fullcontact.com/1k953nu1', json=data)
    logging.info("data sent for evaluation {}".format(data))
    output = the_function(data)
    return jsonify(output)




# In[4]:


# from p#print import p#print as pp
# pp(bases)


# In[5]:


# import matplotlib.pyplot as plt

# for i,cell in enumerate(cells):
#     for j,orientation in enumerate(cell):
#         plt.figure(figsize=(1,1))
#         plt.axis([-1, 4, -1, 4])
#         for point in orientation:
# #             #print(point)
#             plt.scatter(point[0], point[1], marker="x")

#         for point in bases[i][j]:
# #             #print(point)
#             plt.scatter(point[0], point[1])

#         plt.axvline(x=widths[i][j])

#         plt.show()
#     #print("\n\n")


# In[ ]:


# get_ipython().system('jupyter nbconvert --to script tetris.ipynb')
