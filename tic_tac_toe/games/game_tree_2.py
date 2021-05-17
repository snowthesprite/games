class Node :
    def __init__(self, parent, player, game_state) :
        self.state = game_state
        self.children = []
        self.player = player
        self.parent = parent
        #self.score = None
        self.winner = self.check_for_winner()
    
    def check_for_winner(self) :
        board = self.state
        rows = board.copy()
        cols = [[board[i][j] for i in range(3)] for j in range(3)]
        diags = [[board[i][i] for i in range(3)],
                 [board[i][2-i] for i in range(3)]]

        full_board = True
        for row in rows + cols + diags :
            if None in row:
                full_board = False
                continue

            if row[0] == row[1] and row[1] == row[2] :
                return (self.player + 1) % 2

        if full_board :
            return 'Tie'

class TicTacToeTree :
    start = [[None for _ in range(3)] for __ in range(3)]

    def __init__(self, max_plr, starting_player=0, starting_state=start) :
        self.root = Node(None, starting_player, starting_state)
        self.max_plr = max_plr
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
        #parent_leaf_nodes = []
        queue = [self.root]
        while queue != [] :
            self.create_children(queue[0])
            queue.extend(queue[0].children)
            #if queue[0].children == [] :
                #parent_leaf_nodes.append(queue[0].parent)
            queue.pop(0)
        #self.assign_values(parent_leaf_nodes)

    def assign_values(self, parent_leaf_nodes) :
        unassigned = parent_leaf_nodes
        while unassigned != [] :
            print(unassigned[0].state)
            print(len(unassigned))
            i = 0
            total_removed = 0
            removed = 0
            for node in unassigned.copy() :
                if i % 10000 == 0 :
                    print('iteration:',i)
                    print('actually removed:',removed)
                    print('removed:',total_removed)
                    print()
                i+=1
                child_scores = [child.score for child in node.children]
                if None in child_scores :
                    continue
                if node.player == self.max_plr :
                    node.score = max(child_scores)
                else :
                    node.score = min(child_scores)
                unassigned.remove(node)
                removed+=1
                total_removed +=1 
                if node.parent not in unassigned :
                    unassigned.append(node.parent)
                    removed-= 1
            
## yeah I lifted these from the shared game file what of it

    def get_possible_moves(self, board) :
        possible_moves = [(i,j) for i in range(3) for j in range(3) if board[i][j] == None]
        return possible_moves
        