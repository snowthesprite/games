import random as rand

class SemiIntPlr:
    def __init__(self, num) :
        self.num = num
  
    def set_player_number(self, n) :
        self.num = n
  
    def choose_move(self, board, choices) :
        captures = [choice for choice in choices if choice[2] != []]
        if captures != [] :
            captures.sort(reverse=True, key=(lambda move : len(move[2])))
            return captures[0]
        return rand.choice(choices)