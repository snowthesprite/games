from game_tree import *

tree = CheckersTree(1, 'num_layers', 'heuristic_funct')

tree.create_nodes('start_board', 1)

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