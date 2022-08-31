class InputPlayer:
    def __init__(self):
        self.num = None
  
    def set_player_info(self, n, board):
        self.num = n
  
    def choose_move(self, board, choices):
        move = self.get_input(board, choices)

        return choices[choices.index(move)]
    
    def print_board(self, board):
        row_string = ''
        for i in range(len(board)):
            space = board[i]
            if i % 3 == 0 :
                print(row_string[:-1])
                row_string = ''
            if space == 0:
                row_string += '_|'
            else:
                row_string += space + '|'
            
        print(row_string, '\n')

    def get_input(self, board, choices) :
        self.print_board(board)
        print(choices)
        choice = int(input("Pick a spot: "))
        print()
        while choice not in choices :
            choice = int(input("Not valid, pick a different spot: 0"))
        update = board[:choice] + str(self.num) + board[choice+1:]
        print('\n\n')
        self.print_board(update)
        tf = input("Is this the move you want? (T/F): ")
        if tf == 'T' :
            tf = True
        else :
            tf = False
        if tf :
            return choice
        else :
            print('\n\n')
            return self.get_input(choices)

