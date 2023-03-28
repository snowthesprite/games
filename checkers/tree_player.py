#import sys
#sys.path.append('tic_tac_toe/games')
from game_tree import *

class TreePlayerNet :
    def __init__(self, heurist, layers=2) :
        self.num = None
        self.tree = None
        self.layers = layers
        self.heurist = heurist

    def heuristic(self, board) :
        return self.heurist.find_value(board)
  
    def set_player_info(self, n) :
        self.num = n
        self.tree = CheckersTree(n, self.layers, self.heuristic)
        #self.tree.assign_values()

    def choose_move(self, board, choices) :
        self.tree.prune_tree(board, self.num)
        self.tree.assign_values()
        best = (None, -1)
        for choice in choices :
            update = self.tree.run_move(choice, board)
            update = self.tree.list_to_str(update, (self.num)%2+1)
            if self.tree.nodes[update].score >= best[1] :
                best = (choice, self.tree.nodes[update].score)
        return best[0]