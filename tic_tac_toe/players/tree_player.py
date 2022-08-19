import sys
sys.path.append('tic_tac_toe/games')
from game_tree_2 import TicTacToeTree

class TreePlayer :
    def __init__(self) :
        self.symbol = None
        self.number = None
        self.tree = None
        
  
    def set_player_symbol(self, n) :
        self.symbol = n
  
    def set_player_number(self, n) :
        self.number = n
        self.tree = TicTacToeTree(max_plr = n)

    def choose_move(self, choices) :
        pass
    