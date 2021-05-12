class Game :
    def __init__(self, players, player_1) : 
        self.players = players
        self.plr_1 = player_1
        self.give_plr_num()
        self.game_board = [[None for _ in range(3)] for __ in range(3)]
        self.winner = None

    def give_plr_num(self):
        for i, player in enumerate(self.players):
            player.set_plr_num(i)

    def make_move (self, player) :
        chosen_spot = player.choose_point(self.game_board)
        self.game_board[chosen_spot[0]][chosen_spot[1]] = player.plr_num

    def run_to_completion(self) :
        id = self.plr_1
        while self.winner == None :
            plr = self.players[id]
            id = (id + 1) % 2
            self.make_move(plr)
            self.check_winner()
    
    def check_winner(self) :
        row_win = self.check_row()
        col_win = self.check_col()
        diag_win = self.check_diag()
        cats_game = self.check_cats_game()
        if row_win != None :
            self.winner = row_win
        elif col_win != None :
            self.winner = col_win
        elif diag_win != None :
            self.winner = diag_win
        elif cats_game :
            self.winner = 'Cats Game'

    def check_diag(self) :
        board = self.game_board
        if board[0][0] == board[1][1] and board[1][1] == board[2][2] :
            return board[0][0]
        elif board[0][2] == board[1][1] and board[1][1] == board[2][0] :
            return board[1][1]
        return None

    def check_col(self) :
        board = self.game_board
        for col_id in range(3) :
            if board[0][col_id] == board[1][col_id] and board[1][col_id] == board[2][col_id] :
                return board[0][col_id]
        return None

    def check_row(self) :
        for row in self.game_board :
            if row[0] == row[1] and row[1] == row[2] :
                return row[0]
        return None

    def check_cats_game(self) :
        for row in self.game_board :
            if None in row :
                no_none = False
                break
            else :
                no_none = True
        return no_none
