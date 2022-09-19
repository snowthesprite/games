## Heuristic Tree
## You have to tell the tree to assign values
## make better prune tree later

class Node :
    def __init__(self, parent, player, game_state) :
        self.children = []
        self.player = player
        self.parent = [parent]
        self.score = None
        self.winner = self.check_for_winner(game_state)
    
    def check_for_winner(self, board) :
        rows = [board[row] for row in range(6)] #row
        cols = [''.join([board[row][col] for row in range(6)]) for col in range(7)]
        l_dias = []
        r_dias = []
        diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
        for (row, col) in diagonals :
            i=0
            l_dia = []
            r_dia = []
            while row-i >=0 and col+i <= 6 :
                ##l_dias.append(''.join([board[row-i][col+i] for i in range(row-col+1)]))
                ##r_dias.append(''.join([board[row-i][6-col-i] for i in range(row-col+1)]))
                l_dia.append(board[row-i][col+i])
                r_dia.append(board[row-i][6-col-i])
                i+= 1
            l_dias.append(l_dia)
            r_dias.append(r_dia)
        
        thing = rows + cols + l_dias + r_dias

        tie = []

        for stuff in thing :
            if stuff.count('0') > len(stuff) - 4 :
                continue
            if '1111' in stuff :
                return 1
            elif '2222' in stuff :
                return 2
            tie.append('0' in stuff)

        if True not in tie:
            return 'Tie'

class Con4Tree :
    start = ['0000000' for _ in range(6)]
    #7 col, 6 rows
    #'0000000'
    #'0000000'
    #'0000000'
    #'0000000'
    #'0000000'
    #'0000000'
    #ways to connect 4
    #Check each row/column for 4+ players 
    #make diagonals by going till hit 0 or 6

    def __init__(self, max_plr, num_layers, heuristic_funct) :
        self.root = None#start_board
        self.layer_num = num_layers
        self.heuristic = heuristic_funct
        #print(self.root)
        self.max_plr = max_plr
        self.leaf_nodes = [] 
        self.nodes = None#{self.root: Node(None, self.find_turn(start_board), self.root)}
        #self.nodes[self.root].score = 'root'
        #self.create_nodes(start_board)
    
    def find_turn(self, board) : 
        if board.count('1') == board.count('2') :
            return 1
        else :
            return 2

    def get_possible_moves(self, game_state) :
        if self.nodes[game_state].winner != None :
            return [[]]
        
        possible_moves = []
        
        cols = [[(row,col) for row in range(5,-1,-1)] for col in range(7)]
        for col in cols :
            for (row, col) in col :
                if board[row][col] == '0' :
                    possible_moves.append((row,col))
                    break
        return possible_moves     
    
    def create_nodes(self, start_board) :
        prev_choices = [start_board]
        curr_plr = self.find_turn(start_board)
        layer = 0
        while layer < self.layer_num and prev_choices != [] :
            choice = prev_choices[0]
            if self.find_turn(choice) != curr_plr :
                layer += 1
                curr_plr = self.find_turn(choice)
            if layer == self.layer_num :
                break
            prev_choices.remove(choice)
            possible_choices = self.get_possible_moves(choice)
            if [] in possible_choices :
                self.leaf_nodes.append(choice)
                continue

            update = [choice[:value] + str(curr_plr) + choice[value+1:] for value in possible_choices]
            self.nodes[choice].children = update
            for move in update :
                if move in self.nodes.keys() :
                    self.nodes[move].parent.append(choice)
                else :
                    prev_choices.append(move)
                    self.nodes[move] = Node(choice, (curr_plr%2) +1, move)
            
        self.leaf_nodes.extend(prev_choices)
        if len(set(self.leaf_nodes)) != len(self.leaf_nodes) :
            print("ERROR")
            #prev_choices.extend([move for move in update if move not in prev_choices])
        #return nodes

    def assign_values(self) :
        unassigned = self.leaf_nodes.copy()
        index = 0

        while len(unassigned) >= 1  :
            if index == len(unassigned) and unassigned != [] :
                index = 0

            node = self.nodes[unassigned[index]]
            unassigned.extend([parent for parent in node.parent if self.nodes[parent].score != 'root' and parent not in unassigned])

            child_scores = [self.nodes[child].score for child in node.children]
            if None in child_scores :
                index += 1
                continue
            
            if child_scores == [] :
                self.find_score(unassigned[index], node)
            elif node.player == self.max_plr :
                node.score = max(child_scores)
            else :
                node.score = min(child_scores)
            unassigned.pop(index)
    
    def find_score(self, board, node) :
        if node.winner != None :
            if node.winner == 'Tie' :
                node.score = 0
            elif node.winner == self.max_plr :
                node.score = 1
            else :
                node.score = -1
            return
        
        node.score = self.heuristic(board)

    def check_scores(self) :
        queue = [self.root]
        while queue != [] :
            node = self.nodes[queue[0]]
            if node.score == None :
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

    def prune_tree(self, new_board) :
        self.leaf_nodes = [] 
        self.root = new_board
        self.nodes = {self.root: Node(None, self.find_turn(new_board), self.root)}
        self.nodes[self.root].score = 'root'
        self.create_nodes(new_board)
        self.assign_values()