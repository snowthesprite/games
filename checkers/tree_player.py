#import sys
#sys.path.append('tic_tac_toe/games')
from game_tree import *

class TreePlayerNet :
    def __init__(self, heurist, layers=4) :
        self.num = None
        self.tree = None
        self.layers = layers
        self.heuristic = heurist

    #def heuristic(self, board) :
    #    return
  
    def set_player_info(self, n, board) :
        self.num = n
        self.tree = CheckersTree(n, self.layers, self.heuristic)
        #self.tree.assign_values()

    def choose_move(self, board, choices) :
        self.tree.prune_tree(board)
        #tree.assign_values()
        best = (None, -1)
        for choice in choices :
            update = board[:choice] + str(self.num) + board[choice+1:]
            if self.tree.nodes[update].score >= best[1] :
                best = (choice, self.tree.nodes[update].score)
        return best[0]