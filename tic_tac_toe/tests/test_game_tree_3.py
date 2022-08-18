import sys
sys.path.append('tic_tac_toe/games')
from game_tree_3 import TicTacToeTree

board = '000000000'

tree = TicTacToeTree(0,board)

print('ran')

#print(len(tree.nodes))
#print(len(tree.leaf_nodes))

tree.assign_values()