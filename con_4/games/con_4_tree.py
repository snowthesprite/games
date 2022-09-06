## Heuristic Tree
## You have to tell the tree to assign values
## make better prune tree later

class Node :
    def __init__(self, parent, player, game_state) :
        #print(game_state)
        #print(player)
        self.children = []
        self.player = player
        self.parent = [parent]
        self.score = None
        self.winner = self.check_for_winner(game_state)
    
    def check_for_winner(self, board) :
        thing = [board[index: index+3] for index in range(0,9,3)] #row
        for index in range(3) :
            thing.append(board[index] + board[index+3] + board[index+6]) #column
        thing.extend([board[0] + board[4] + board[8], board[2] + board[4] + board[6]]) #diagonal
        for stuff in thing :
            if len(set(stuff)) == 1 and '0' not in set(stuff) :
                return int(stuff[0])
        if '0' not in board :
            return 'Tie'

class TicTacToeTree :
    start = '000000000'

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
        possible_moves = [index for index in range(len(game_state)) if game_state[index]=='0']
        if possible_moves == [] :
            possible_moves.append([])
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