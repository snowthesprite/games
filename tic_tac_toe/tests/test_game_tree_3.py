import sys
sys.path.append('tic_tac_toe/games')
from game_tree_3 import TicTacToeTree

board = '000000000'

#tree = TicTacToeTree(0,board)
tree = TicTacToeTree(max_plr = 2, start_board=board)

print('ran')

#print(len(tree.nodes)) ##5478
#print(len(tree.leaf_nodes)) ##958

tree.assign_values()
print(tree.nodes['200000010'].score)
tree.check_scores()