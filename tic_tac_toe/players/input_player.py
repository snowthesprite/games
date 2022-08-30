class InputPlayer:
    def __init__(self):
        self.num = None
  
    def set_player_info(self, n, board):
        self.num = n
  
    def choose_move(self, board, choices):
        move = self.get_input(choices)

        return choices[choices.index(move)]
    
    def print_board(self, board):
        row_string = ''
        for i in range(len(board)):
            if i % 3 == 0 :
                print(row_string[:-1])
            if space == 0:
                row_string += '_|'
            else:
                row_string += space + '|'
            
        print('\n')

    def get_input(self, choices) :
        self.print_board(board)
        choice = input("Pick a spot")
        print()
        while choice not in choices :
            choice = input("Not valid, pick a different spot")
        update = self.board[:choice] + str(player.num) + self.board[choice+1:]
        print('\n\n')
        self.print_board(update)
        tf = input("Is this the move you want? (T/F)")
        if tf :
            return point
        else :
            print('\n\n')
            return self.get_input(choices)

