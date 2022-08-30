import sys
sys.path.append('tic_tac_toe/games')
from game_tree_3 import TicTacToeTree

board = '000000000'

#tree = TicTacToeTree(0,board)
tree = TicTacToeTree(max_plr = 2, start_board=board)

print('ran')

#print(len(tree.nodes))
#print(len(tree.leaf_nodes))

tree.assign_values()
print(tree.nodes['200000010'].score)
tree.check_scores()