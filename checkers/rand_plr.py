import random as rand

class RandPlr:
    def __init__(self):
        self.num = None
  
    def set_player_number(self, n):
        self.num = n
  
    def choose_move(self, board, choices):
        return rand.choice(choices)