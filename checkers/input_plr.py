class InputPlayer:
    def __init__(self):
        self.num = None
  
    def set_player_number(self, n):
        self.num = n
  
    def choose_move(self, board, choices):
        move = self.get_input(board, choices)

        return choices[choices.index(move)]
    
    def print_board(self, board):
        print('   a b c d e f g h')
        print()
        id = 0
        for row in board:
            row_string = chr(id+97) + ' |'
            for col in row :
                if col == 0 :
                    row_string += ' |'
                else :
                    row_string += str(col) + '|'
            print(row_string)
            print('   ---------------')
            id+=1
        print('\n\n')

    def get_input(self, board, choices) :
        self.print_board(board)
        dic_choice = self.translate_choices(choices)
        l = list(dic_choice.keys())
        print(l)
        choice = input('Pick a mvmt: ')
        print()
        while choice not in l :
            choice = int(input("Not valid, pick valid mvmt: "))
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
        return dic_choice[choice]

    def translate_choices(self, choices) :
        dic_choices = {}
        for (start, trans) in choices :
            end_row, end_col = start[0] + trans[0], start[1] + trans[1]
            key = chr(start[0] + 97) + chr(start[1]+97) + ' ' + chr(end_row + 97) + chr(end_col + 97)
            dic_choices[key] = (start, trans)
        return dic_choices

