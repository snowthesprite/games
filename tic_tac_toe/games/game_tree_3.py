#reduced
class Node :
    def __init__(self, parent, player, game_state) :
        self.children = []
        self.player = player
        self.parent = [parent]
        self.score = None
        self.winner = self.check_for_winner(game_state)
    
    def check_for_winner(self, game_state) :
        board = game_state
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
    start = [[None for _ in range(3)] for __ in range(3)]

    def __init__(self, starting_player=0, starting_state=start) :
        self.root = Node(None, starting_player, starting_state)
        self.max_plr = 1
        self.plr_marks = ['X', 'O']
        #self.total_nodes = 1
        self.leaf_nodes = [] 
        self.nodes = {starting_state: self.root}
        self.create_nodes(starting_state)
        #self.build_game_tree() 
        #self.check_scores()

    def create_children(self, parent) :
        if parent.winner != None :
            self.leaf_nodes += 1
            return
        next_plr = (parent.player + 1) % 2
        for (row_id, col_id) in self.get_possible_moves(parent.state) :
            game_state = [row.copy() for row in parent.state]
            game_state[row_id][col_id] = self.plr_marks[parent.player]
            child = Node(parent, next_plr, game_state)
            parent.children.append(child)
            self.total_nodes += 1

    def build_game_tree(self) :
        leaf_nodes = []
        queue = [self.root]
        while queue != [] :
            self.create_children(queue[0])
            queue.extend(queue[0].children)
            if queue[0].children == [] :
                leaf_nodes.append(queue[0])
            queue.pop(0)
        #self.assign_values(leaf_nodes)

    def get_possible_moves(self, game_state) :
        possible_moves = []
        #thing = self.check_for_winner(game_state)
        if self.nodes[game_state].winner != None :
            return [[]]
        for index in range(len(game_state)) :
            if game_state[index] == '0':
                possible_moves.append(index)
        if possible_moves == [] :
            possible_moves.append([])
        return possible_moves
    
    def create_nodes(self, starting_state) :
        prev_choices = [starting_state]
        #leaf_nodes = []
        while prev_choices != [] :
            choice = prev_choices[0]
            prev_choices.remove(choice)
            possible_choices = self.get_possible_moves(choice)
            if [] in possible_choices :
                self.leaf_nodes.append(choice)
                continue
            if choice.count('1') == choice.count('2') :
                sym = 1
            else :
                sym = 2

            update = [choice[:value] + str(sym) + choice[value+1:] for value in possible_choices]
            self.nodes[choice].children = update
            for move in update :
                if move in self.nodes.keys() :
                    self.nodes[move].parent.append(choice)
                else :
                    prev_choices.append(move)
                    self.nodes[move] = Node(choice, (sym+1)%2, move)
            #prev_choices.extend([move for move in update if move not in prev_choices])
        #return nodes

    def assign_values(self) :
        unassigned = self.leaf_nodes
        print(len(unassigned))
        index = 0
        total_removed = 0
        removed = 0
        i =0
        while index <= len(unassigned) :
            node = self.nodes[unassigned[index]]
            if i % 10000 == 0 :
                print('iteration:',i, 'index',index)
                print('actually removed:',removed)
                print('removed:',total_removed)
                print(len(unassigned))
                print()
            index+=1
            i+=1
            child_scores = [self.nodes[child].score for child in node.children]
            #if None in child_scores :
            #    continue
            if child_scores == [] :
                if node.winner == 'Tie' :
                    node.score = 0
                elif node.winner == self.max_plr :
                    node.score = 1
                else :
                    node.score = -1
            elif node.player == self.max_plr :
                node.score = max(child_scores)
            else :
                node.score = min(child_scores)

            unassigned.remove(unassigned[index])
            index -= 1
            removed+=1
            total_removed +=1 
            if node.parent not in unassigned :
                #unassigned.append(node.parent)
                removed-= 1
            unassigned.extend([parent for parent in node.parent if parent not in unassigned])
            if index == len(unassigned) and len(unassigned) > 1 :
                index = 0

    def check_scores(self) :
        self.root.score == 'root'
        queue = [self.root]
        while queue != [] :
            if queue[0].score == None :
                print('This node has no score')
                print(queue[0].state)
                print('This nodes children are')
                for node in queue[0].children :
                    print(node.state)
                    print(node.score)
                    print()
                print('this nodes parent is')
                print(queue[0].parent.state)
                print(queue[0].parent.score)
                print('\n\n\n')
            queue.extend(queue[0].children)
            queue.pop(0)
   
    ## yeah I lifted these from the shared game file what of it 

    def get_possible_moves_1(self, board) :
        possible_moves = [(i,j) for i in range(3) for j in range(3) if board[i][j] == None]
        return possible_moves
        