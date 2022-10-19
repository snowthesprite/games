class Adaptor() :
    def __init__(self, strat) :
        self.strat = strat
        self.num = None
    
    def set_player_number(self, num):
        self.num = num
        self.strat.set_player_number(num)
    
    def row_list(self,board) :
        num_board = []
        for row in board :
            row_l = list(row)
            num_board.append([int(_) for _ in row_l])
        return num_board
    
    def choose_move(self, board, choices):
        board = self.row_list(board)
        return self.strat.choose_move(board, choices)
        