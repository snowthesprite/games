import sys
sys.path.append('tic_tac_toe/games')
from game_tree_4 import TicTacToeTree

board = '000000000'

#'''
#tree = TicTacToeTree(0,board)
tree = TicTacToeTree(2, 5, board)

print('ran')

print(len(tree.nodes))
print(len(tree.leaf_nodes))
print(len(set(tree.leaf_nodes)))

tree.assign_values()
tree.check_scores()

val = 1244
print()

print(tree.leaf_nodes[val], tree.nodes[tree.leaf_nodes[val]].score)

tree.prune_tree(tree.leaf_nodes[val])

print('\n\n')

print(len(tree.nodes))
print(len(tree.leaf_nodes))
print(len(set(tree.leaf_nodes)))

tree.assign_values()
tree.check_scores()
#'''