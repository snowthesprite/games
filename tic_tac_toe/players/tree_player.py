import sys
sys.path.append('tic_tac_toe/games')
from game_tree_3 import TicTacToeTree

class TreePlayer :
    def __init__(self) :
        self.num = None
        self.tree = None
  
    def set_player_info(self, n, board) :
        self.num = n
        self.tree = TicTacToeTree(max_plr = n, start_board = board)
        self.tree.assign_values()

    def choose_move(self, board, choices) :
        best = (None, -1)
        for choice in choices :
            update = board[:choice] + str(self.num) + board[choice+1:]
            if self.tree.nodes[update].score >= best[1] :
                best = (choice, self.tree.nodes[update].score)
        return best[0]
    