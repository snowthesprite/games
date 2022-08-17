import sys
sys.path.append('tic_tac_toe/games')
from game_tree_3 import TicTacToeTree

board = '000000000'

tree = TicTacToeTree(0,board)

print('ran')

print(tree.total_nodes)
print(tree.leaf_nodes)