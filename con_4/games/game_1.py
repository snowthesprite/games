#min max player

from random import random

class Con4 :
    def __init__(self, players):
        self.rand = round(random())
        self.players = players
        self.board = [''.join(['0' for _ in range(7)]) for __ in range(6)]
        self.determine_player_order()
        self.set_player_numbers()
        self.round = 1
        self.winner = None

    def set_player_numbers(self): 
        self.players[0].set_player_number(1)
        self.players[1].set_player_number(2)
    
    def determine_player_order(self):
        if self.rand == 1:
            self.players = self.players[::-1]
    
    def get_possible_moves_col(self) :
        possible_moves = []
        
        cols = [[(row,col) for row in range(5,-1,-1)] for col in range(7)]
        for colm in cols :
            for (row, col) in colm :
                if self.board[row][col] == '0' :
                    possible_moves.append(col)
                    break
        return possible_moves

    def complete_round(self):
        for player in self.players:
            choices = self.get_possible_moves_col()
            if choices != []:
                player_move = player.choose_move(self.board, choices)
                self.update_board(player, player_move)
            if self.check_for_winner() != None:
                self.winner = self.check_for_winner()
                break
        self.round += 1

    def run_to_completion(self):
        while self.winner == None:
            self.complete_round()
        '''
        if self.rand == 1 and type(self.winner) == int:
            #print(type(self.winner))
            self.winner = (self.winner % 2) + 1
        #'''

    def check_for_winner(self) :
        rows = [self.board[row] for row in range(6)] #row
        cols = [''.join([self.board[row][col] for row in range(6)]) for col in range(7)]
        l_dias = []
        r_dias = []
        diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
        for (row, col) in diagonals :
            i=0
            l_dia = []
            r_dia = []
            while row-i >=0 and col+i <= 6 :
                l_dia.append(self.board[row-i][col+i])
                r_dia.append(self.board[row-i][6-col-i])
                i+= 1
            l_dias.append(''.join(l_dia))
            r_dias.append(''.join(r_dia))
        
        thing = rows + cols + l_dias + r_dias

        tie = []

        for stuff in thing :
            tie.append('0' in stuff)
            if stuff.count('0') > len(stuff) - 4 :
                continue
            if '1111' in stuff :
                return 1
            elif '2222' in stuff :
                return 2

        if True not in tie:
            return 'Tie'

    def print_board(self):
        for row in self.board:
            row_string = ''
            for col in row :
                if col == '0' :
                    row_string += ' |'
                else:
                    row_string += col + '|'
            print(row_string)
            print('---------------')
            
        #print(row_string, '\n')
            
        #print('\n')
    
    def update_board(self, player, choice) : 
        #print(choice)
        for row in range(5,-1,-1) :
            if self.board[row][choice] == '0' :
                choice = (row, choice)
                break
        self.board[choice[0]] = self.board[choice[0]][:choice[1]] + str(player.num) + self.board[choice[0]][choice[1]+1:]
