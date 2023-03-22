#work on making board dict (possibly)

from random import random

class Checkers :
    def __init__(self, players, loop=0):
        self.rand = loop#round(random())
        self.players = players
        self.board = [[(i+j)%2 * ((3 - (j<3)-2*(j>4))%3) for i in range(8)] for j in range(8)]
        '''
        self.board = [[0,0,0,0,0,0,0,0],
                      [0,0,2,0,2,0,2,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,2,0,2,0,0,0],
                      [0,0,0,1,0,0,0,0],
                      [0,0,2,0,2,0,2,0],
                      [0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],]
        #'''
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

    ## START FIND MOVES
    
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
        new_coord = [coord[0]+trans[0], coord[1]+trans[1]]
        if not self.out_of_bounds(new_coord) and self.board[new_coord[0]][new_coord[1]] == 0 :
            return True


    def get_possible_moves(self, coord) :
        translation = self.get_possible_trans(self.board[coord[0]][coord[1]])
        can_move = []
        for trans in translation :
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(new_coord, coord) :
                continue
            if self.foe_present(new_coord, coord) :
                if self.next_clear(new_coord, trans) :
                    can_move.append([(2*trans[0], 2*trans[1]), [new_coord]])
                    #print('ran')
            else :
                can_move.append([trans, []])
        return can_move


    def pos_combo(self, coord, piece) :
        #piece is actually the piece's coords
        translation = self.get_possible_trans(self.board[piece[0]][piece[1]])
        combat = []
        for trans in translation :
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(new_coord, piece) :
                continue
            if self.foe_present(new_coord, piece) :
                if self.next_clear(new_coord, trans) :
                    combat.append([(2*trans[0], 2*trans[1]), [new_coord]])
        return combat


    def get_pieces(self, plr_num) :
        pieces = []
        for row in range(8) :
            for col in range(8) :
                if abs(self.board[row][col]) == plr_num :
                    pieces.append((row, col))
        return pieces


    def get_all_moves(self, plr_num) :
        pieces = self.get_pieces(plr_num)
        can_move = []
        for coord in pieces :
            translations = self.get_possible_moves(coord)
            can_move.extend([[coord] + trans for trans in translations])
        id = 0
        while id < len(can_move) :
            move = can_move[id]
            if move[2] != [] :
                combo = self.pos_combo((move[0][0]+move[1][0], move[0][1]+move[1][1]), move[0])
                #adds all combo moves
                for comb in combo :
                    if not any(victim in move[2] for victim in comb[1]) :
                        can_move.append([move[0],(move[1][0]+comb[0][0], move[1][1]+comb[0][1]), move[2]+comb[1]])
            id += 1

        return can_move
    
    ## END FINDS MOVES
        

    def run_move(self, move, plr_num) :
        origin = move[0]
        trans = move[1]
        captures = move[2]
        self.update_board(origin, trans)
        for capt in captures :
            self.board[capt[0]][capt[1]] = 0
        
        end_coord = (origin[0]+trans[0], origin[1] + trans[1])
        self.crown(plr_num, end_coord)

    def run_game(self) :
        plr_num = 1
        turn = 0
        while self.winner == None :
            all_moves = self.get_all_moves(plr_num)
            if all_moves == [] :
                self.winner = (plr_num % 2) + 1
                print(turn)
                print(self.winner)
                self.print_board()
                break
            move = self.players[plr_num-1].choose_move(self.board, all_moves)
            self.run_move(move, plr_num)
            plr_num = (plr_num % 2) + 1
            turn += 1
            if turn > 100 :
                self.winner = 'Tie'

    def crown(self, plr_num, end_coord) :
        piece = self.board[end_coord[0]][end_coord[1]]
        if (end_coord[0] == 0 and piece == 1) or (end_coord[0] == 7 and piece == 2) :
            self.board[end_coord[0]][end_coord[1]] = -piece
            


    '''
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
        if self.rand == 1 and type(self.winner) == int:
            #print(type(self.winner))
            self.winner = (self.winner % 2) + 1
    #'''
    def print_board(self):
        print('   a b c d e f g h')
        print()
        id = 0
        for row in self.board:
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
            
        #print(row_string, '\n')
            
        #print('\n')
    
    def update_board(self, coord, trans) : 
        piece = self.board[coord[0]][coord[1]]
        new_coord = (coord[0] + trans[0], coord[1] + trans[1])
        self.board[coord[0]][coord[1]] = 0
        self.board[new_coord[0]][new_coord[1]] = piece