import random as rand

class SemiIntPlr:
    def __init__(self) :
        self.num = None
  
    def set_player_number(self, n) :
        self.num = n
  
    def choose_move(self, board, choices) :
        captures = [choice for choice in choices if choice[2] != []]
        if captures != [] :
            return rand.choice(captures)
        return rand.choice(choices)