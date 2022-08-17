import sys
sys.path.append('tic_tac_toe/games')
from game_tree_2 import TicTacToeTree

board = [[None for _ in range(3)] for __ in range(3)]

tree = TicTacToeTree(board, 0)

print('ran')

print(tree.total_nodes)
print(tree.leaf_nodes)

def print_board(board):
    for i in range(len(board)):
      row = board[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      print(row_string[:-1])
    print('\n')
''''
print_board(tree.root.state)
print_board(tree.root.children[2].state)
print_board(tree.root.children[1].children[1].state)
print_board(tree.root.children[1].children[1].children[2].state)
print_board(tree.root.children[1].children[1].children[2].children[1].state)
print_board(tree.root.children[1].children[1].children[2].children[1].children[3].state)
for child in tree.root.children[1].children[1].children[2].children[1].children[3].children :
    print_board(child.state)
'''