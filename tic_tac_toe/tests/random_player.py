from random import randint

class RandomPlayer():
    def __init__(self):
        self.plr_num = None

    def set_plr_num(self, n):
        self.plr_num = n

    def choose_point(self, game_board):
        possible_rows = [id for id in range(3) if None in game_board[id]]
        possible_cols = {}
        for row in possible_rows :
            possible_cols[row] = []
            for col_id in range(3) :
                if game_board[row][col_id] == None :
                    possible_cols[row].append(col_id)
                    
        chosen_row = randint(0,len(possible_rows)-1)
        chosen_row = possible_rows[chosen_row]

        chosen_cols = randint(0, len(possible_cols[chosen_row])-1)
        chosen_cols = possible_cols[chosen_row][chosen_cols]

        return (chosen_row, chosen_cols)