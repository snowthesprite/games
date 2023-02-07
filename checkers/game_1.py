#work on making board dict (possibly)

from random import random

class Con4 :
    def __init__(self, players, loop):
        self.rand = loop#round(random())
        self.players = players
        self.board = [[(i+j)%2 * ((3 - (j<3)-(j<4))%3) for i in range(8)] for j in range(8)]
        #self.determine_player_order()
        self.set_player_numbers()
        self.round = 1
        self.winner = None


    def set_player_numbers(self): 
        self.players[0].set_player_number(1)
        self.players[1].set_player_number(2)

    
    def determine_player_order(self):
        if self.rand % 2 == 1:
            self.players = self.players[::-1]

    
    def get_possible_trans(self, piece) :
        if piece < 0 :
            return [(1,1), (1,-1), (-1,1), (-1,-1)]
        elif piece == 1 :
            return [(-1,1), (-1,-1)]
        elif piece == 2 :
            return [(1,1), (1,-1)]

    
    def out_of_bounds(self, coord) :
        if coord[1] > 7 or coord[1] < 0 or coord[0] > 7 or coord[0] < 0 :
            return True
        return False


    def foe_present(self, coord, old_coord) :
        cur = self.board[old_coord[0]][old_coord[1]]
        unkn = self.board[coord[0]][coord[1]]
        if abs(cur) != abs(unkn) and unkn != 0 :
            return True
        return False


    def friend_present(self, coord, old_coord) :
        cur = self.board[old_coord[0]][old_coord[1]]
        unkn = self.board[coord[0]][coord[1]]
        if abs(cur) == abs(unkn) and unkn != 0 :
            return True
        return False


    def next_clear(self, coord, trans) :
        new_coord = coord
        if self.board[new_coord[0]][new_coord[1]] == 0 and not self.out_of_bounds(new_coord) :
            return True


    def get_possible_moves(self, coord) :
        translation = self.get_possible_trans(self.board[coord[0]][coord[1]])
        can_move = []
        for trans in translation :
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(new_coord, coord) :
                continue
            if self.foe_present(new_coord, coord) and self.next_clear(new_coord, trans) :
                can_move.append((2*trans[0], 2*trans[1]))
            else :
                can_move.append(trans)
        return can_move


    def get_pos_moves_combo(self, coord) :
        translation = self.get_possible_trans(self.board[coord[0]][coord[1]])
        can_move = []
        for trans in translation :
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if this.out_of_bounds(new_coord) or this.board[coord[0]][coord[1]] != 0 :
                continue
            if this.foe_present(new_coord, coord) and this.next_clear(new_coord, trans) :
                can_move.append((2*trans[0], 2*trans[1]))
            else :
                can_move.append(trans)
        return can_move


    def get_pieces(self, plr_num) :
        pieces = []
        for row in range(8) :
            for col in range(8) :
                if abs(self.board[row][col]) == plr_num :
                    pieces.append((row, col))


    def get_all_moves(self, plr_num) :
        pieces = self.get_pieces(plr_num)
        can_move = []
        for coord in pieces :
            translations = self.get_possible_moves(coord)
            can_move.extend([(coord, trans) for trans in translations])
        return can_move


    def capture(self, move) :
        coord_2 = move[0]
        coord = (coord_2[0] + move[1][0], coord_2[1] + move[1][1])
        self.update_board(coord_2, coord)
        coord_2 = (coord[0] + move[1][0], coord[1] + move[1][1])
        self.update_board(coord, coord_2)


    def side_moves(self, move) :
        new_coord = (move[0][0] + move[1][0], move[0][1] + move[1][1])
        while 2 in move[1] or -2 in move[1] :
            self.capture(move)
            new_coord = (new_coord[0] + move[1][0], new_coord[1] + move[1][1])
            pos_moves = self.get_pos_moves_combo(new_coord)
            if pos_moves[1] :
                move = self.player[plr_num-1].choose_move([(new_coord, trans) for trans in pos_moves[0]])
            else :
                break


    def complete_round(self) :
        plr_num = 1
        while self.winner == None :
            move = self.players[plr_num-1].choose_move(self.get_all_moves(plr_num))
            self.side_moves(move)




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
        pass

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
    
    def update_board(self, old_coord, new_coord) : 
        piece = self.board[old_coord[0]][old_coord[1]]
        self.board[old_coord[0]][old_coord[1]] = 0
        self.board[new_coord[0]][new_coord[1]] = piece