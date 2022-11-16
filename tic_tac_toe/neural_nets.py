##For specifically tic tac toe
##All hidden nodes are in range of 10 + self.hidden, starting at 11 (put range(11, 11+self.hidden))
from random import choice
from numpy.random import normal, uniform, randint
import math

#'''
class Node (): 
    def __init__(self, id, act_funct) :
        self.spec = None
        self.id = id
        self.parents = []
        self.act_funct = act_funct
        self.value = lambda weights, xs : sum([weights[(parent.id, self.id)] * parent.output(weights,xs) for parent in self.parents])
    
    def output(self, weights, input) :
        return self.act_funct(self.value(weights, input))
    
    def input(self) :
        self.value = lambda weights, xs : xs[self.id-1]

class NeuralNet (): 
    def __init__(self, nodes, weights, non_hidden = 1, premade = False) :
        self.nodes = nodes
        self.hidden = non_hidden
        
        if not premade :
            self.weights = self.make_weights()
        else :
            self.weights = weights
    
    def choose_move(self, board, possible_moves) :
        v_board = self.vector_board(board)
        layer = self.nodes[len(self.nodes)-1]
        move_val = [layer[space].output(self.weights, v_board) if space in possible_moves else -100 for space in range(9)]
        return move_val.index(max(move_val))

    def vector_board(self, board) :
        v_board = []
        for space in board :
            if space == '1' :
                v_board.append(1)
            elif space == '2' :
                v_board.append(-1)
            else :
                v_board.append(0)
        return v_board

    ## RSS is a thing that exists and is, in fact, what you are taking the derivative of. 
    ## Not... whatever you were thinking

    def calc_score(self) :
        score = 0
        for _ in range(32) :
            game = TicTacToe(self)
            game.run_to_completion()
            if game.winner == 1 :
                score += 1
            if game.winner == 2 :
                score -= 10
        return score


    def make_weights(self) :
        weights = {}
        overide = False
        hidden_range = list(range(20, 10+self.hidden, -1))
        for layer in range(len(self.nodes)-1) :
            for node_from in self.nodes[layer] :
                if node_from.id in hidden_range :
                    overide = True
                for node_to in self.nodes[layer+1] :
                    if node_to.spec == 'bias' :
                        continue
                    weights[(node_from.id, node_to.id)] = uniform(-0.5, 0.5)
                    if overide or node_to.id in hidden_range :
                        weights[(node_from.id, node_to.id)] = 0
                overide = False
        return weights

class NeuralNetField (): 
    def __init__(self, layers, act_funct) :
        self.nodes = {}
        #self.data = self.normalize_data(data)

        self.create_nodes(layers, act_funct)

        #self.num_weights = 111
        self.curr_gen = []

        #self.create_gen(amount)

    def create_nodes(self, node_layers, act_funct) :
        layers = self.create_layers(node_layers)
        id = 0
        for layer in range(len(layers)) :
            node_order = 0
            self.nodes[layer] = []
            for node in layers[layer] :
                id += 1
                new_node = Node(id, act_funct)
                if node == 'bias' : 
                    new_node.spec = 'bias'
                    new_node.value = lambda weights, *x : 1
                    self.nodes[layer].append(new_node)
                    continue
                if layer == 0 :
                    new_node.input()
                    self.nodes[layer].append(new_node)
                    continue

                new_node.parents = self.make_node_specifics(layer, node_order, id)
                self.nodes[layer].append(new_node)
                
    def make_node_specifics(self, layer, node_order, id) :
        from_node = []
        for prev_node_order in range(len(self.nodes[layer-1])) :
            prev_node = self.nodes[layer-1][prev_node_order]
            from_node.append(prev_node)
        return from_node
    
    def create_layers(self, node_layers) :
        net_set = []
        for layer_num in range(len(node_layers)) :
            if layer_num != 0 :
                net_set[layer_num - 1].append('bias')
            net_set.append([node for node in range(node_layers[layer_num])])
        return net_set

    def reproduce(self, parent, amount=1) :
        child = {'weights': {}, 'hidden': parent.hidden}

        pm = choice([0,1]) * choice([-1,1]) 
        if pm + parent.hidden <= 10 and pm + parent.hidden >= 1 :
            child['hidden'] += pm
            
        non_included = list(range(10+child['hidden'], 10, -1))
        for (connect, weight) in parent.weights.items() :
            if connect[0] in non_included or connect[1] in non_included :
                #print(connect)
                child['weights'][connect] = 0
            else :
                child['weights'][connect] = weight + normal(0,0.05)
                
        return child

    def evolve(self, gens) :
        generations = {}
        for gen in range(gens) :
            if gen % 1 == 0 :
                print(gen)
                #print(generations.items()[len(gen_avg)-100 : len(gen_avg)])
            gen_scores = [net.calc_score() for net in self.curr_gen]
            gen_max = max(gen_scores)
            #generations[gen] = {'avg' : sum(gen_scores) / len(gen_scores), 'max': gen_max}
            generations[gen] = sum(gen_scores)/len(gen_scores)

            cont_pop = [index for index in range(len(self.curr_gen)) if gen_scores[index] == gen_max]
            new_pop = []
            id = 0
            while len(new_pop + cont_pop) < len(self.curr_gen) :
                parent = self.curr_gen[(id + 1) % len(cont_pop)]
                new_pop.append(self.reproduce(parent))

            for idx in range(len(self.curr_gen)) :
                if idx in cont_pop :
                    continue
                child = new_pop[0]
                new_pop.pop(0)
                self.curr_gen[idx].weights = child['weights']
                self.curr_gen[idx].hidden = child['hidden']
        return generations
        
    def calc_ans(self, input) :
        return [net.calc_ans(input) for net in self.curr_gen]

    def create_gen(self, amount) :
        for _ in range(amount) :
            net = NeuralNet(self.nodes, None)
            self.curr_gen.append(net)
#'''

class TicTacToe:
    def __init__(self, nn):
        self.players = [nn, Enmy()]
        self.board = '000000000'
        self.round = 1
        self.winner = None
    
    def get_possible_moves(self) :
        possible_moves = [index for index in range(len(self.board)) if self.board[index]=='0']
        if possible_moves == [] :
            possible_moves.append([])
        return possible_moves

    def complete_round(self) :
        for plr_id in range(2) :
            plr = self.players[plr_id]
            choices = self.get_possible_moves()
            if choices != [] :
                player_move = plr.choose_move(self.board, choices)
                self.update_board(plr_id+1, player_move)
            if self.check_for_winner() != None:
                self.winner = self.check_for_winner()
                break
        self.round += 1

    def run_to_completion(self) :
        while self.winner == None :
            self.complete_round()

    def check_for_winner(self) :
        thing = [self.board[index: index+3] for index in range(0,9,3)] #row
        for index in range(3) :
            thing.append(self.board[index] + self.board[index+3] + self.board[index+6]) #column
        thing.extend([self.board[0] + self.board[4] + self.board[8], self.board[2] + self.board[4] + self.board[6]]) #diagonal
        for stuff in thing :
            if len(set(stuff)) == 1 and '0' not in set(stuff) :
                return int(stuff[0])
        if '0' not in self.board :
            return 'Tie'
    
    def update_board(self, plr_num, choice) : 
        #print(choice)
        self.board = self.board[:choice] + str(plr_num) + self.board[choice+1:]

class Enmy :
    def __init__(self) :
        self.id = 2

    def choose_move(self, board, possible_moves) :
        if randint(0, 10) == 0 :
            return choice(possible_moves)

        thing_m = [list(range(index, index+3)) for index in range(0,9,3)]
        thing = [board[index: index+3] for index in range(0,9,3)] #row
        for index in range(3) :
            thing_m.append([index, index + 3, index + 6])
            thing.append(board[index] + board[index+3] + board[index+6]) #column
        thing_m.extend([[0,4,8], [2,4,6]])
        thing.extend([board[0] + board[4] + board[8], board[2] + board[4] + board[6]]) #diagonal
        
        negative = []
        neutral = []
        for id in range(len(thing)) :
            stuff = thing[id]
            if stuff.count('2') == 2 and stuff.count('0') == 1 :
                return thing_m[id][stuff.index('0')]
            if stuff.count('1') == 2 and stuff.count('0') == 1 :
                #print(stuff, stuff.index('0'))
                #print(thing_m[id])
                negative.append(thing_m[id][stuff.index('0')])
            elif stuff.count('1') == 1 and stuff.count('0') == 2 :
                neutral.extend([index for index in range(3) if stuff[index] == '0'])
        
        if negative != [] :
            return choice(negative)
        if neutral != [] :
            return choice(neutral)
        
        return choice(possible_moves)
        

            