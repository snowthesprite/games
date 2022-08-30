#reduced
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

    def __init__(self, max_plr, start_board=start) :
        if start_board.count('1') == start_board.count('2') :
            sym = 1
        else :
            sym = 2
        self.root = start_board
        #print(self.root)
        self.max_plr = max_plr
        self.leaf_nodes = [] 
        self.nodes = {self.root: Node(None, sym, self.root)}
        self.nodes[self.root].score = 'root'
        self.create_nodes(start_board)

    def get_possible_moves(self, game_state) :
        if self.nodes[game_state].winner != None :
            return [[]]
        possible_moves = [index for index in range(len(game_state)) if game_state[index]=='0']
        if possible_moves == [] :
            possible_moves.append([])
        return possible_moves
    
    def create_nodes(self, start_board) :
        prev_choices = [start_board]
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
                    self.nodes[move] = Node(choice, (sym%2) +1, move)
            #prev_choices.extend([move for move in update if move not in prev_choices])
        #return nodes

    def assign_values(self) :
        unassigned = self.leaf_nodes
        index = 0

        while len(unassigned) >= 1  :
            if index == len(unassigned) and unassigned != [] :
                index = 0

            node = self.nodes[unassigned[index]]
            unassigned.extend([parent for parent in node.parent if self.nodes[parent].score == None and parent not in unassigned])

            child_scores = [self.nodes[child].score for child in node.children]
            if None in child_scores :
                index += 1
                continue
            
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
            unassigned.pop(index)

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
   
    ## yeah I lifted these from the shared game file what of it 
        