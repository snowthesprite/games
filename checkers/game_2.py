## work on making board dict (possibly)

class Checkers :
    def __init__(self, players) :
        self.players = players
        self.board = [[(i+j) % 2 * ((3 - (j < 3)-2*(j > 4)) % 3)
                       for i in range(8)] for j in range(8)]
        self.round = 1
        self.winner = None

## START FIND MOVES
    
    def get_possible_trans(self, coord) :
        piece = self.board[coord[0]][coord[1]]
        if piece < 0 :
            return [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece == 1 :
            return [(-1, 1), (-1, -1)]
        elif piece == 2 :
            return [(1, 1), (1, -1)]

    def out_of_bounds(self, coord) :
        if coord[1] > 7 or coord[1] < 0 or coord[0] > 7 or coord[0] < 0 :
            return True
        return False

    def foe_present(self, coord, old_coord) :
        cur = self.board[old_coord[0]][old_coord[1]]
        unkn = self.board[coord[0]][coord[1]]
        if unkn != 0 and abs(cur) != abs(unkn) :
            return True
        return False

    def friend_present(self, coord, old_coord) :
        cur = self.board[old_coord[0]][old_coord[1]]
        unkn = self.board[coord[0]][coord[1]]
        if unkn != 0 and abs(cur) == abs(unkn) :
            return True
        return False

    def next_clear(self, coord, trans) :
        new_coord = [coord[0]+trans[0], coord[1]+trans[1]]
        if not self.out_of_bounds(new_coord) and self.board[new_coord[0]][new_coord[1]] == 0 :
            return True

    def get_possible_moves(self, coord) :
        translation = self.get_possible_trans(coord)
        can_move = []
        for trans in translation :
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(new_coord, coord) :
                continue
            if self.foe_present(new_coord, coord) :
                if self.next_clear(new_coord, trans) :
                    can_move.append([(new_coord[0] + trans[0], new_coord[1] + trans[1]), [new_coord]])
            else :
                can_move.append([new_coord, []])
        return can_move

    def pos_combo(self, coord, piece) :
        ## piece is actually the piece's coords
        translation = self.get_possible_trans(piece)
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
            moves = self.get_possible_moves(coord)
            can_move.extend([[coord] + move for move in moves])
        id = 0
        while id < len(can_move) :
            move = can_move[id]
            if move[2] != [] :
                combo = self.pos_combo(move[1], move[0])
                # adds all combo moves
                for comb in combo :
                    if not any(victim in move[2] for victim in comb[1]) :
                        can_move.append(
                            [move[0], (move[1][0]+comb[0][0], move[1][1]+comb[0][1]), move[2]+comb[1]])
            id += 1

        return can_move

    ## END FINDS MOVES

## START BOARD MANIPULATION
    def run_move(self, move, plr_num) :
        origin = move[0]
        trans = move[1]
        captures = move[2]
        self.update_board(origin, trans)
        for capt in captures :
            self.board[capt[0]][capt[1]] = 0

    def update_board(self, coord, new_coord) :
        piece = self.board[coord[0]][coord[1]]
        self.board[coord[0]][coord[1]] = 0
        self.board[new_coord[0]][new_coord[1]] = piece
        if (new_coord[0] == 0 and piece == 1) or (new_coord[0] == 7 and piece == 2) :
            self.board[new_coord[0]][new_coord[1]] = -piece

    def print_board(self) :
        print('    a  b  c  d  e  f  g  h')
        print()
        id = 0
        for row in self.board :
            row_string = chr(id+97) + '  |'
            for col in row :
                if col == 0 :
                    row_string += '  |'
                else :
                    if col < 0 :
                        row_string += 'K'
                    else :
                        row_string += 'P'
                    row_string += str(abs(col)) + '|'
            print(row_string)
            print('   -------------------------')
            id += 1
        print('\n\n')

 ## END BOARD MANIPULATION

## RUN GAME
    def run_game(self) :
        plr_num = 1
        while self.winner == None :
            #if self.round % 1 == 0 :
            #    print(self.round)
            all_moves = self.get_all_moves(plr_num)
            if all_moves == [] :
                self.winner = (plr_num % 2) + 1
                break

            move = self.players[plr_num-1].choose_move(self.board, all_moves)
            self.run_move(move, plr_num)
            plr_num = (plr_num % 2) + 1
            self.round += 1

            if self.round >= 200 :
                self.winner = 'Tie'
            #self.print_board()

        # print(row_string, '\n')
        print('moves:', self.round)
