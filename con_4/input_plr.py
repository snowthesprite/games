class InputPlayer:
    def __init__(self):
        self.num = None
  
    def set_player_info(self, n, board):
        self.num = n
  
    def choose_move(self, board, choices):
        move = self.get_input(board, choices)

        return choices[choices.index(move)]
    
    def print_board(self, board):
        for row in board:
            row_string = '|'
            for col in row :
                if col == '0' :
                    row_string += ' |'
                else:
                    row_string += col + '|'
            print(row_string)
            print('---------------')
        print('\n\n')

    def get_input(self, board, choices) :
        self.print_board(board)
        print(choices)
        choice = input("Pick a spot: ")
        choice = choice.split(' ')
        #print(choice)
        choice = (int(choice[0]), int(choice[1]))
        print()
        while choice not in choices :
            choice = int(input("Not valid, pick a different spot: 0"))
        #update = board[:choice] + str(self.num) + board[choice+1:]
        #print('\n\n')
        #self.print_board(update)
        '''
        tf = input("Is this the move you want? (T/F): ")
        if tf == 'T' :
            tf = True
        else :
            tf = False
        if tf :
            return choice
        else :
            print('\n\n')
        '''
        #return self.get_input(choices)
        return choice

