class Node :
    def __init__(self, parent, player, game_state) :
        self.state = game_state
        self.children = []
        self.player = player
        self.parent = parent
        self.winner = None

class TicTacToeTree :
    def __init__(self, starting_state, starting_player) :
        self.root = Node(None, starting_player, starting_state)
        self.plr_marks = ['X', 'O']
        self.total_nodes = 1
        self.leaf_nodes = 0 
        self.build_game_tree() 

    def create_children(self, parent) :
        if parent.winner != None :
            self.leaf_nodes += 1
            return
        next_plr = (parent.player + 1) % 2
        for (row_id, col_id) in self.get_possible_moves(parent.state) :
            game_state = [row.copy() for row in parent.state]
            game_state[row_id][col_id] = self.plr_marks[parent.player]
            child = Node(parent, next_plr, game_state)
            self.check_for_winner(child)
            parent.children.append(child)
            self.total_nodes += 1

    def build_game_tree(self) :
        queue = [self.root]
        while queue != [] :
            self.create_children(queue[0])
            children = queue[0].children
            for child in children :
                queue.append(child)
            queue.pop(0)

## yeah I lifted these from the shared game file what of it

    def get_possible_moves(self, board) :
        possible_moves = [(i,j) for i in range(3) for j in range(3) if board[i][j] == None]
        return possible_moves

    def check_for_winner(self, node) :
        board = node.state
        rows = board.copy()
        cols = [[board[i][j] for i in range(3)] for j in range(3)]
        diags = [[board[i][i] for i in range(3)],
                 [board[i][2-i] for i in range(3)]]
        
        prev_plr = (node.player + 1) % 2
        board_full = True
        for row in rows + cols + diags :
            if None in row:
                board_full = False

            if row == [self.plr_marks[prev_plr] for _ in range(3)] :
                node.winner = prev_plr
                return
    
        if board_full :
            node.winner = 'Tie'
        