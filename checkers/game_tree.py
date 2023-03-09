# For Checkers
# You have to tell the tree to assign values
# make better prune tree later

class TreeNode:
    def __init__(self, parent, player, game_state):
        self.children = []
        self.player = player
        self.parent = [parent]
        self.score = None
        self.board = game_state
        #self.winner = self.check_for_winner(game_state)

    def check_for_winner(self, board):
        thing = [board[index: index+3] for index in range(0, 9, 3)]  # row
        for index in range(3):
            thing.append(board[index] + board[index+3] +
                         board[index+6])  # column
        thing.extend([board[0] + board[4] + board[8],
                     board[2] + board[4] + board[6]])  # diagonal
        for stuff in thing:
            if len(set(stuff)) == 1 and '0' not in set(stuff):
                return int(stuff[0])
        if '0' not in board:
            return 'Tie'


class CheckersTree:
    #start = ''.join([''.join([str((i+j) % 2 * ((3 - (j < 3)-2*(j > 4)) % 3)) for i in range(8)]) for j in range(8)])
    #start = [[(i+j)%2 * ((3 - (j<3)-2*(j>4))%3) for i in range(8)] for j in range(8)]

    def __init__(self, max_plr, num_layers, heuristic_funct):
        start = [[(i+j)%2 * ((3 - (j<3)-2*(j>4))%3) for i in range(8)] for j in range(8)]
        self.root = self.list_to_str(start)
        self.layer_num = num_layers
        self.heuristic = heuristic_funct
        self.max_plr = max_plr
        self.leaf_nodes = []
        self.nodes = {self.root: TreeNode(None, 1, start)}

    # START FIND MOVES

    def get_possible_trans(self, piece):
        if piece < 0:
            return [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece == 1:
            return [(-1, 1), (-1, -1)]
        elif piece == 2:
            return [(1, 1), (1, -1)]

    def out_of_bounds(self, coord):
        if coord[1] > 7 or coord[1] < 0 or coord[0] > 7 or coord[0] < 0:
            return True
        return False

    def foe_present(self, board, coord, old_coord):
        cur = board[old_coord[0]][old_coord[1]]
        unkn = board[coord[0]][coord[1]]
        if abs(cur) != abs(unkn) and unkn != 0:
            return True
        return False

    def friend_present(self, board, coord, old_coord):
        cur = board[old_coord[0]][old_coord[1]]
        unkn = board[coord[0]][coord[1]]
        if abs(cur) == abs(unkn) and unkn != 0:
            return True
        return False

    def next_clear(self, board, coord, trans):
        new_coord = [coord[0]+trans[0], coord[1]+trans[1]]
        if not self.out_of_bounds(new_coord) and board[new_coord[0]][new_coord[1]] == 0:
            return True

    def get_possible_moves(self, board, coord):
        translation = self.get_possible_trans(board[coord[0]][coord[1]])
        can_move = []
        for trans in translation:
            new_coord = [coord[0] + trans[0], coord[1] + trans[1]]
            if self.out_of_bounds(new_coord) or self.friend_present(board, new_coord, coord):
                continue
            if self.foe_present(board, new_coord, coord):
                if self.next_clear(board, new_coord, trans):
                    can_move.append([(2*trans[0], 2*trans[1]), [new_coord]])
                    # print('ran')
            else:
                can_move.append([trans, []])
        return can_move

    def pos_combo(self, board, coord, piece):
        # piece is actually the piece's coords
        translation = self.get_possible_trans(board[piece[0]][piece[1]])
        combat = []
        for trans in translation:
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
        pieces = self.get_pieces(board, plr_num)
        can_move = []
        for coord in pieces:
            translations = self.get_possible_moves(board, coord)
            can_move.extend([[coord] + trans for trans in translations])
        id = 0
        while id < len(can_move):
            move = can_move[id]
            if move[2] != []:
                combo = self.pos_combo(board, (move[0][0]+move[1][0], move[0][1]+move[1][1]), move[0])
                # adds all combo moves
                for comb in combo:
                    if not any(victim in move[2] for victim in comb[1]):
                        can_move.append([move[0], (move[1][0]+comb[0][0], move[1][1]+comb[0][1]), move[2]+comb[1]])
            id += 1

        return can_move

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

    def update_board(self, board, coord, trans):
        piece = board[coord[0]][coord[1]]
        new_coord = (coord[0] + trans[0], coord[1] + trans[1])
        board[coord[0]][coord[1]] = 0
        board[new_coord[0]][new_coord[1]] = piece
        if (new_coord[0] == 0 and piece == 1) or (new_coord[0] == 7 and piece == 2):
            board[new_coord[0]][new_coord[1]] = -piece
        return board

    # END BOARD MANIPULATION AND UPDATING

    def list_to_str(self, board):
        str_board = ''.join(
            [''.join([str(piece) for piece in row]) for row in board])
        return str_board

    def create_nodes(self, start_board, plr):
        cur_queue = [self.root] #[start_board]
        next_queue = [0]
        cur_plr = plr
        layer = 0
        #while layer < self.layer_num and next_queue != []:
        while next_queue != [] :
            next_queue = []

            while cur_queue != []:
                s_board = cur_queue.pop(0)
                l_board = self.nodes[s_board].board
                possible_choices = self.get_all_moves(l_board, cur_plr)
                if [] in possible_choices:
                    self.leaf_nodes.append(s_board)
                    continue

                update = [self.run_move(choice, l_board) for choice in possible_choices]

                for move in update:
                    s_move = self.list_to_str(move)
                    self.nodes[s_board].children.append(s_move)
                    if s_move in self.nodes.keys():
                        if self.nodes[s_move].player != (cur_plr % 2) + 1:
                            print('Theres an identical board with a diff player')
                            return
                        self.nodes[s_move].parent.append(s_board)
                    else:
                        next_queue.append(s_move)
                        self.nodes[s_move] = TreeNode(
                            s_board, (cur_plr % 2) + 1, move)
            
            cur_queue.extend(next_queue)
            layer += 1
            cur_plr = (cur_plr % 2) + 1

        #self.leaf_nodes.extend(cur_queue)
        if len(set(self.leaf_nodes)) != len(self.leaf_nodes):
            print("ERROR")

    def assign_values(self):
        unassigned = self.leaf_nodes.copy()
        index = 0

        while len(unassigned) >= 1:
            if index == len(unassigned) and unassigned != []:
                index = 0

            node = self.nodes[unassigned[index]]
            unassigned.extend(
                [parent for parent in node.parent if self.nodes[parent].score != 'root' and parent not in unassigned])

            child_scores = [self.nodes[child].score for child in node.children]
            if None in child_scores:
                index += 1
                continue

            if child_scores == []:
                self.find_score(unassigned[index], node)
            elif node.player == self.max_plr:
                node.score = max(child_scores)
            else:
                node.score = min(child_scores)
            unassigned.pop(index)

    def find_score(self, board, node):
        if node.winner != None:
            if node.winner == 'Tie':
                node.score = 0
            elif node.winner == self.max_plr:
                node.score = 1
            else:
                node.score = -1
            return

        node.score = self.heuristic(board)

    def check_scores(self):
        queue = [self.root]
        while queue != []:
            node = self.nodes[queue[0]]
            if node.score == None:
                print('This node has no score')
                print(queue[0])
                print('This nodes children are')
                print(node.children)
                print([self.nodes[child].score for child in node.children])
                print()
                print('this nodes parents are')
                print(node.parent)
                print([self.nodes[parent].score for parent in node.parent])
                print('\n\n\n')
            queue.extend(node.children)
            queue.pop(0)

    def prune_tree(self, new_board):
        self.leaf_nodes = []
        self.root = new_board
        self.nodes = {self.root: TreeNode(
            None, self.find_turn(new_board), self.root)}
        self.nodes[self.root].score = 'root'
        self.create_nodes(new_board)
        self.assign_values()
