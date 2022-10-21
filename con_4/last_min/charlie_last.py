import copy, random
#from game_tree import *

class CharlieLM:
    
    def __init__(self, ply=None):
        self.number = None
  
    def set_player_number(self, n):
        self.number = n

    def choose_move(self, state, moves):
        
        for move in moves:

            capture_win_state = copy.deepcopy(state)
            block_loss_state = copy.deepcopy(state)

            for i in range(5, -1, -1):
                if state[i][move] == None:
                    capture_win_state[i][move] = self.number
                    block_loss_state[i][move] = 3 - self.number
                    break

            if check_for_winner(capture_win_state) or check_for_winner(block_loss_state):
                return move

        return random.choice(moves)

    def update_state(self, state):
        pass

def check_for_winner(state):

    board_full = True
    for row in get_combinations(state):
        
        if None in row:
            board_full = False

        if len(set(row)) == 1 and row[0] != None:
            return row[0]
    
    return 'tie' if board_full else None

def get_combinations(state):
    
    four_in_a_row = []

    for i in range(6):
        for j in range(4):
            row = [state[i][j + k] for k in range(4)]
            four_in_a_row.append(row)

    for i in range(3):
        for j in range(7):
            column = [state[i + k][j] for k in range(4)]
            four_in_a_row.append(column)
    
    for i in range(3):
        for j in range(4):
            forward_diag = [state[i + k][j + k] for k in range(4)]
            four_in_a_row.append(forward_diag)
    
    for i in range(3):
        for j in range(3, 7):
            backward_diag = [state[i + k][j - k] for k in range(4)]
            four_in_a_row.append(backward_diag)
    
    return four_in_a_row