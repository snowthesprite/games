from game_tree import *
import random as rand

#'''
allt = []
for _ in range(1) :
    tree = CheckersTree(1, 4, 'heuristic_funct')
    tree.leaf_nodes = []
    times = 0
    fake_leaf = [tree.root]
    while fake_leaf != [] :
        tree.root = rand.choice(fake_leaf)
        fake_leaf = tree.create_nodes('start_board', tree.nodes[tree.root].plr)
        times += 1
    allt.append(times)

print(sum(allt)/20)
#'''

'''
boa = [[0,0,0,0,0,0,0,0],
         [0,0,2,0,2,0,2,0],
         [0,0,0,0,0,0,0,0],
         [0,0,2,0,2,0,0,0],
         [0,0,0,1,0,0,0,0],
         [0,0,2,0,2,0,2,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],]

def list_to_str(board) :
    str_board = '|'.join([''.join([str(piece) for piece in row]) for row in board])
    return str_board

print(list_to_str(boa))
'''