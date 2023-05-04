# For Checkers
# You have to tell the tree to assign values
#THERE CAN BE IDENTICAL BOARDS WITH DIFFERENT PLAYERS
import time as t

class TreeNode:
    def __init__(self, parent, player, game_state):
        self.children = []
        self.plr = player
        self.parent = set([parent])
        self.score = 'unset'
        self.board = game_state
        self.winner = None

    def assign_winner(self):
        self.winner = self.plr
    
    def reset(self) :
        self.score = None
        self.parent = set([])


class CheckersTree:
    
    def __init__(self, num_layers):
        start = [[(i+j)%2 * ((3 - (j<3)-2*(j>4))%3) for i in range(8)] for j in range(8)]
        self.times = {'reset children':[], 'create kids':[], 'assign values':[]
                      ,'find moves': [], 'create nodes':[], 'num heurst Called':[]}

        self.max_lyr = num_layers

        self.leaf_nodes = []
        self.fake_leaf = []

        self.root = self.list_to_str(start, 1)
        self.nodes = {self.root: TreeNode(None, 1, start)}
        self.nodes[self.root].parent = set([])
        self.nodes[self.root].score = 'root'
        self.create_nodes(1, self.max_lyr-2)

# START FIND MOVES

    def get_possible_trans(self, board, coord) :
        piece = board[coord[0]][coord[1]]
        if piece < 0:
            return [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece == 1:
            return [(-1, 1), (-1, -1)]
        elif piece == 2:
            return [(1, 1), (1, -1)]

    def out_of_bounds(self, coord) :
        if coord[1] > 7 or coord[1] < 0 or coord[0] > 7 or coord[0] < 0:
            return True
        return False

    def foe_present(self, board, coord, old_coord) :
        cur = board[old_coord[0]][old_coord[1]]
        unkn = board[coord[0]][coord[1]]
        if unkn != 0 and abs(cur) != abs(unkn) :
            return True
        return False

    def friend_present(self, board, coord, old_coord) :
        cur = board[old_coord[0]][old_coord[1]]
        unkn = board[coord[0]][coord[1]]
        if unkn != 0 and abs(cur) == abs(unkn) :
            return True
        return False

    def next_clear(self, board, coord, trans) :
        new_coord = [coord[0]+trans[0], coord[1]+trans[1]]
        if not self.out_of_bounds(new_coord) and board[new_coord[0]][new_coord[1]] == 0 :
            return True

    def get_possible_moves(self, board, coord):
        translation = self.get_possible_trans(board, coord)
        can_move = []
        for trans in translation:
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(board, new_coord, coord):
                continue
            if self.foe_present(board, new_coord, coord):
                if self.next_clear(board, new_coord, trans):
                    can_move.append([(new_coord[0] + trans[0], new_coord[1] + trans[1]), [new_coord]])
                    # print('ran')
            else:
                can_move.append([new_coord, []])
        return can_move

    def pos_combo(self, board, coord, piece):
        # piece is actually the piece's coords
        translation = self.get_possible_trans(board, piece)
        combat = []
        for trans in translation :
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(board, new_coord, piece):
                continue
            if self.foe_present(board, new_coord, piece):
                if self.next_clear(board, new_coord, trans):
                    combat.append([(2*trans[0], 2*trans[1]), [new_coord]])
        return combat

    def get_pieces(self, board, plr_num):
        pieces = []
        for row in range(8):
            for col in range(8):
                if abs(board[row][col]) == plr_num:
                    pieces.append((row, col))
        return pieces

    def get_all_moves(self, board, plr_num):
        ##!!
        t1 = t.time()
        ##!!

        pieces = self.get_pieces(board, plr_num)
        can_move = []
        for coord in pieces:
            moves = self.get_possible_moves(board, coord)
            can_move.extend([[coord] + move for move in moves])
        id = 0
        while id < len(can_move):
            move = can_move[id]
            if move[2] != []:
                combo = self.pos_combo(board, move[1], move[0])
                # adds all combo moves
                for comb in combo:
                    if not any(victim in move[2] for victim in comb[1]):
                        can_move.append([move[0], (move[1][0]+comb[0][0], move[1][1]+comb[0][1]), move[2]+comb[1]])
            id += 1
        
        ##!!
        t2 = t.time()
        self.times['find moves'].append(t2-t1)
        ##!!
        can_move = self.order_left(can_move)

        return can_move

    def order_left(self, all_moves) :
        LeftMostPiece = all_moves.sort(key =lambda move : move[0][1])
        LeftMostMove = all_moves.sort(key =lambda move : move[1][1])
        TopMostPiece = all_moves.sort(key =lambda move : move[0][0])
        TopMostMove = all_moves.sort(key =lambda move : move[1][0])
        return all_moves

 # ENDS FIND MOVES

# START BOARD MANIPULATION AND UPDATING

    def run_move(self, move, board):
        board = [row.copy() for row in board]
        origin = move[0]
        trans = move[1]
        captures = move[2]
        board = self.update_board(board, origin, trans)
        for capt in captures:
            board[capt[0]][capt[1]] = 0
        return board

    def update_board(self, board, coord, new_coord):
        piece = board[coord[0]][coord[1]]
        board[coord[0]][coord[1]] = 0
        board[new_coord[0]][new_coord[1]] = piece
        if (new_coord[0] == 0 and piece == 1) or (new_coord[0] == 7 and piece == 2):
            board[new_coord[0]][new_coord[1]] = -piece
        return board

    def list_to_str(self, board, plr):
        str_board = ''.join(
            [''.join(map(str, row)) for row in board])
        return str_board + ' ' + str(plr)
 # END BOARD MANIPULATION AND UPDATING

# START EVERYTHING ELSE
    def create_nodes(self, plr, cur_lyr = 0) :
        ##!!
        t1 = t.time()
        ##!!
        cur_queue = [self.root]
        next_queue = [0]
        cur_plr = plr
        layer = cur_lyr
        while layer < self.max_lyr and next_queue != [] :
            next_queue = []
            while cur_queue != [] :
                s_board = cur_queue.pop(0)
                node = self.nodes[s_board]
                if node.children != [] :
                    next_queue.extend(self.reset_children(s_board, node))
                else : next_queue.extend(self.create_children(s_board, node, cur_plr))

            cur_queue = next_queue
            layer += 1
            cur_plr = (cur_plr % 2) + 1

            if layer == self.max_lyr :
                self.fake_leaf = next_queue

        ##!!
        t2 = t.time()
        self.times['create nodes'].append(t2-t1)
        ##!!
        

    def reset_children(self, s_board, node) :
        ##!!
        t1 = t.time()
        ##!!

        next_queue = []
        for kid in node.children :
            child = self.nodes[kid]
            if kid != self.root and child.score != None :
                child.reset()
                next_queue.append(kid)
            child.parent.add(s_board)
        
        ##!!
        t2 = t.time()
        self.times['reset children'].append(t2-t1)
        ##!!

        return next_queue

    def create_children(self, s_board, node, cur_plr) :
        ##!!
        t1 = t.time()
        ##!!
        next_queue = []
        l_board = node.board
        possible_choices = self.get_all_moves(l_board, cur_plr)
        if possible_choices == [] :
            self.leaf_nodes.append(s_board)
            node.assign_winner()

            ##!!
            t2 = t.time()
            self.times['create kids'].append(t2-t1)
            ##!!

            return next_queue

        update = [self.run_move(choice, l_board) for choice in possible_choices]
        need_reset = False

        for move in update :
            s_move = self.list_to_str(move, (cur_plr%2)+1)
            node.children.append(s_move)
            next_queue.append(s_move)

            if s_move in self.nodes :
                kid = self.nodes[s_move]
                if s_move!= self.root and kid.score != None :
                    kid.reset()
                kid.parent.add(s_board)
            else :
                self.nodes[s_move] = TreeNode(
                    s_board, (cur_plr % 2) + 1, move)

        ##!!
        t2 = t.time()
        self.times['create kids'].append(t2-t1)
        ##!!

        return next_queue

    def assign_values(self, max_plr, heuristic) :
        t1 = t.time()

        unassigned = self.leaf_nodes + self.fake_leaf
        index = 0
        assi = 0

        while len(unassigned) >= 1:
            if index >= len(unassigned) :
                index = 0

            node = self.nodes[unassigned[index]]
            unassigned.extend(
                [parent for parent in node.parent if self.nodes[parent].score != 'root' and parent not in unassigned])

            child_scores = [self.nodes[child].score for child in node.children if self.nodes[child].score != 'root']
            if None in child_scores or 'unset' in child_scores :
                print('happended')
                index += 1
                continue

            if child_scores == [] :
                assi += self.find_score(node, max_plr, heuristic)
            elif node.plr == max_plr:
                node.score = max(child_scores)
            else:
                node.score = min(child_scores)
            unassigned.pop(index)

        ##!!
        t2 = t.time()
        #print('av', t2-t1)
        self.times['assign values'].append(t2-t1)
        self.times['num heurst Called'].append(assi)
        ##!!

    def find_score(self, node, max_plr, heuristic) :
        if node.winner != None :
            if node.winner == 'Tie' :
                node.score = 0
            elif node.winner == max_plr :
                node.score = 1
            else:
                node.score = -1
            return 0

        node.score = heuristic(node.board)
        return 1

    def prune_tree(self, new_board, plr) :
        self.nodes[self.root].score = 0

        self.leaf_nodes = []
        self.root = self.list_to_str(new_board, plr)
        self.nodes[self.root].score = 'root'
        self.create_nodes(plr)
