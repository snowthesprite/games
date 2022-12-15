##For specifically tic tac toe
##All hidden nodes are in range of 10 + self.hidden, starting at 11 (put range(11, 11+self.hidden))
from random import choice
from numpy.random import normal, uniform, randint
import math

import matplotlib.pyplot as plt
plt.style.use('bmh')

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
    def __init__(self, node_layers, act_funct) :
        self.nodes = {}
        self.create_nodes(node_layers, act_funct)
        self.weights = None

    def calc_score(self, weights) :
        self.weights = weights
        game = TicTacToe(self)
        score = 0
        for _ in range(30) :
            game.run_game()
            
            if game.winner == 1 :
                score += 1
            if game.winner == 2 :
                score -= 10
        return score
    
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

    #Node/Weight Generation

    def create_nodes(self, node_layers, act_funct) :
        layers = self.create_layers(node_layers)
        id = 0
        for layer in range(len(layers)) :
            self.nodes[layer] = []
            for node in layers[layer] :
                id += 1
                new_node = Node(id, act_funct)
                if node == 'bias' : 
                    new_node.spec = 'bias'
                    new_node.value = lambda weights, xs : 1
                    self.nodes[layer].append(new_node)
                    continue
                if layer == 0 :
                    new_node.input()
                    self.nodes[layer].append(new_node)
                    continue

                new_node.parents = self.make_node_specifics(layer)
                self.nodes[layer].append(new_node)
                
    def make_node_specifics(self, layer) :
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

    def make_weights(self, hidden) :
        weights = {}
        hidden_range = list(range(20, 10+hidden, -1))
        for layer in range(len(self.nodes)-1) :
            for node_from in self.nodes[layer] :
                overide = False
                if node_from.id in hidden_range :
                    overide = True
                for node_to in self.nodes[layer+1] :
                    if node_to.spec == 'bias' :
                        continue
                    weights[(node_from.id, node_to.id)] = uniform(-0.5, 0.5)
                    if overide or node_to.id in hidden_range :
                        weights[(node_from.id, node_to.id)] = 0
        return weights

class NeuralNetField (): 
    def __init__(self, layers, act_funct) :
        self.net = NeuralNet(layers, act_funct)
        self.curr_gen = []

    def reproduce(self, parent, amount=1) :
        child = {'weights': {}, 'hidden': parent['hidden']}

        pm = choice([-1,0,1])
        if pm + child['hidden'] <= 10 and pm + child['hidden'] >= 1 :
            child['hidden'] += pm
            
        non_included = list(range(20, 10+child['hidden'], -1))
        for (connect, weight) in parent['weights'].items() :
            if connect[0] in non_included or connect[1] in non_included :
                child['weights'][connect] = 0
            else :
                child['weights'][connect] = weight + normal(0,0.05)
                
        return child

    def evolve(self, gens) :
        generations = {}
        for gen in range(gens) :
            if gen % 50 == 0 :
                print('Gen:', gen)
                #self.in_prog_graph(generations)
            gen_scores = [self.net.calc_score(inst['weights']) for inst in self.curr_gen]

            generations[gen] = max(gen_scores)

            comp_scores = []
            for id in range(50) :
                net_score = gen_scores[id]
                ## Possible spot for error: May check against self
                score = sum([net_score - choice(gen_scores) for _ in range(10)])
                comp_scores.append((id, score))
            
            comp_scores.sort(reverse=True, key=(lambda scr : scr[1]))
            #print(comp_scores[:25])
            
            cont_pop = [self.curr_gen[net[0]] for net in comp_scores[:25]]
            new_pop = []
            id = 0
            while len(new_pop + cont_pop) < len(self.curr_gen) :
                parent = cont_pop[id]
                new_pop.append(self.reproduce(parent))
                id = (id + 1) % len(cont_pop)
            self.curr_gen = cont_pop + new_pop
            
        return generations

    def create_gen(self, amount) :
        self.curr_gen = []
        for _ in range(amount) :
            hidden = randint(1, 11)
            net = {'weights': self.net.make_weights(hidden), 'hidden': hidden}
            self.curr_gen.append(net)

    def in_prog_graph(self, gen_scores) :
        x_axis = []
        y_axis = []
        for (gen, avg) in gen_scores.items() :
            x_axis.append(gen)
            y_axis.append(avg)
        plt.plot(x_axis, y_axis) 
        plt.savefig('evolving_prog.png')
        

class TicTacToe:
    def __init__(self, nn):
        self.players = [nn, Enmy()]
    
    def get_possible_moves(self) :
        possible_moves = [index for index in range(9) if self.board[index]=='0']
        return possible_moves

    def run_game(self) :
        self.board = '000000000'
        self.winner = None
        plr_id = 0
        while self.winner == None :
            plr = self.players[plr_id]
            choices = self.get_possible_moves()
            player_move = plr.choose_move(self.board, choices)
            self.update_board(plr_id+1, player_move)
            self.winner = self.check_for_winner()
            plr_id = (plr_id + 1) % 2

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
        self.board = self.board[:choice] + str(plr_num) + self.board[choice+1:]

class Enmy :
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
                negative.append(thing_m[id][stuff.index('0')])

            elif stuff.count('1') == 1 and stuff.count('0') == 2 :
                neutral.extend([index for index in range(3) if stuff[index] == '0'])
        
        if negative != [] :
            return choice(negative)
        if neutral != [] :
            return choice(neutral)
        
        return choice(possible_moves)
        

            