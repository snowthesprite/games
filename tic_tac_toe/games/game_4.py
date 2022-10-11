#min max player

from random import random

class TicTacToe:
    def __init__(self, players):
        self.rand = round(random())
        self.players = players
        self.board = '000000000'
        self.determine_player_order()
        self.set_player_numbers()
        self.round = 1
        self.winner = None

    def set_player_numbers(self): 
        self.players[0].set_player_info(1, self.board)
        self.players[1].set_player_info(2, self.board)
    
    def determine_player_order(self):
        if self.rand == 1:
            self.players = self.players[::-1]

    def get_possible_moves(self) :
        possible_moves = [index for index in range(len(self.board)) if self.board[index]=='0']
        if possible_moves == [] :
            possible_moves.append([])
        return possible_moves

    def complete_round(self):
        for player in self.players:
            choices = self.get_possible_moves()
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
        if self.rand == 1 and type(self.winner) == int:
            self.winner = (self.winner % 2) + 1

    def check_for_winner(self) :
        thing = [self.board[index: index+3] for index in range(0,9,3)] #row
        for index in range(3) :
            thing.append(self.board[index] + self.board[index+3] + self.board[index+6]) #column
        thing.extend([self.board[0] + self.board[4] + self.board[8], self.board[2] + self.board[4] + self.board[6]]) #diagonal
        for stuff in thing :
            if len(set(stuff)) == 1 and '0' not in set(stuff) :
                return int(stuff[0])
        if '0' not in self.board :
            return 'Tie'

    def print_board(self):
        row_string = ''
        for i in range(len(self.board)):
            if i % 3 == 0 :
                print(row_string[:-1])
            if space == 0:
                row_string += '_|'
            else:
                row_string += space + '|'
            
        print('\n')
    
    def update_board(self, player, choice) : 
        self.board = self.board[:choice] + str(player.num) + self.board[choice+1:]
