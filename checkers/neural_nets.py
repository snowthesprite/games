##For specifically Checkers
## python checkers/test_nets.py -> output.txt

from random import choice
from numpy.random import normal, uniform
import math

#from tree_player import *
from left_tree_plr import *
from semi_int_plr import *
from game_2 import *

import matplotlib.pyplot as plt
plt.style.use('bmh')
import time as t
#'''
## Takes approximently 0.006 sec for generation
class NetNode (): 
    def __init__(self, id, act_funct) :
        #xs is the input, or in this case, the board
        self.spec = None
        self.id = id
        self.parents = []
        self.saved = None
        self.act_funct = act_funct
        self.value = lambda weights, xs : sum([weights[(parent.id, self.id)] * parent.output(weights,xs) for parent in self.parents])
    
    def output(self, weights, input) :
        if self.saved == None :
            self.saved = self.act_funct(self.value(weights, input))
        return self.saved
    
    def input(self) :
        self.act_funct = lambda x : x
        self.value = lambda weights, xs : xs[self.id-1]

    def piece_value(self) :
        self.spec = 'piece'
        self.act_funct = lambda x : x
        self.value = lambda weights, xs : sum([parent.output(weights, xs) for parent in self.parents])

    def bias(self) :
        self.spec = 'bias'
        self.value = lambda weights, xs : 1
        self.act_funct = lambda x : x

class NeuralNet (): 
    def __init__(self, node_layers, act_funct) :
        self.nodes = {}
        self.create_nodes(node_layers, act_funct)

    #NetNode/Weight Generation

    def create_nodes(self, node_layers, act_funct) :
        layers = self.create_layers(node_layers)
        id = 0
        for layer in range(len(layers)) :
            self.nodes[layer] = []
            for node in layers[layer] :
                id += 1
                new_node = NetNode(id, act_funct)
                if node == 'bias' : 
                    new_node.bias()
                    self.nodes[layer].append(new_node)
                    continue
                elif layer == 0 :
                    new_node.input()
                    self.nodes[layer].append(new_node)
                    continue

                new_node.parents = self.make_node_specifics(layer)
                self.nodes[layer].append(new_node)

        #Makes piece Difference
        new_node = NetNode(id+1, act_funct)
        new_node.parents = self.make_node_specifics(1)
        new_node.piece_value()
        self.nodes[len(layers)-1][0].parents.append(new_node)
        self.nodes[len(layers)-2].append(new_node)

                
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

    def make_weights(self) :
        weights = {}
        queue = [self.nodes[len(self.nodes)-1][0]]
        while queue != [] :
            node_to = queue[0]
            queue.pop(0)
            if node_to.spec == 'piece' :
                continue
            for node_from in node_to.parents :
                weights[(node_from.id, node_to.id)] = 0.1#uniform(-0.2, 0.2)
            queue.extend([node for node in node_to.parents if node not in queue])
        return weights

class NeuralNetField (): 
    def __init__(self, layers, num_weights, act_funct) :
        #self.mut_rate = 0.05
        self.num_weights = num_weights
        self.net = NeuralNet(layers, act_funct)
        self.curr_gen = []
        self.pop = 0
        self.times = {'games':[]}

        tree = CheckersTree(2)
        self.p1 = TreePlayerNet(Player(self.net.nodes),1, tree)
        self.p2 = TreePlayerNet(Player(self.net.nodes),2,tree)

    def reproduce(self, parent, amount=1) :
        mutate = parent['mutate'] * math.exp(normal() / (2**(1/2) * self.num_weights ** (1/4)))
        k = parent['K'] * math.exp(normal() / (2**(1/2)))
        if k < 1 :
            k = 1
        elif k > 3 :
            k = 3

        child = {'weights': {}, 'mutate': mutate, 'K': k}
        for (connect, weight) in parent['weights'].items() :
            child['weights'][connect] = weight + mutate * normal()
        return child

    def calc_score(self, plr,id) :
        #print('run')
        score = 0
        #gen_not = self.curr_gen[:id] + self.curr_gen[id:]
        self.p1.heurist.inst(plr)
        for _ in range(1) :
            t1 = t.time()
            self.p2.heurist.inst(choice(self.curr_gen))
            game = Checkers([self.p1, self.p2])
            game.run_game()
            if game.winner == 1 :
                score += 1
            elif game.winner == 2 :
                score -= 2
            t2 = t.time()
            self.times['games'].append(t2-t1)
            print('winner', game.winner)#'games', t2-t1)

        return score

    def calc_graph_score(self, plr) :
        score = 0
        self.p1.heurist.inst(plr)
        for _ in range(2) : 
            game = Checkers([self.p1, SemiIntPlr(2)])
            game.run_game()
            if game.winner == 1 :
                score += 1
            elif game.winner == 2 :
                score -= 2
        return score

    def evolve(self, gens, world) :
        generations = {}
        half = int(self.pop/2)
        for gen in range(gens) :
            scores = [(id, self.calc_score(self.curr_gen[id],id)) for id in range(self.pop)]
            scores.sort(reverse=True, key=(lambda scr : scr[1]))
            
            cont_pop = [self.curr_gen[net[0]] for net in scores[:half]]
            new_pop = []
            ##!?! Every generation run the semi intelegent player against the entire cont pop. Graph the average score.
            ##!?! THere are small changes, try making both players run on one tree.
            if gen % 1 == 0 :
                #print('Gen', gen)
                '''
                gen_scores = []
                for parents in cont_pop :
                    gen_scores = [self.calc_graph_scores]
                '''

                #self.in_prog_graph(generations, world)

            id = 0
            while len(new_pop + cont_pop) < self.pop :
                parent = cont_pop[id]
                new_pop.append(self.reproduce(parent))
                id = (id + 1) % len(cont_pop)
            self.curr_gen = cont_pop + new_pop
            #print()
            
        return generations

    def create_gen(self, amount) :
        self.curr_gen = []
        self.pop = amount
        for _ in range(amount) :
            net = {'weights': self.net.make_weights(), 'mutate': 0.05, 'K': 2}
            self.curr_gen.append(net)

    def in_prog_graph(self, gen_scores, world) :
        x_axis = []
        y_axis = []
        for (gen, avg) in gen_scores.items() :
            x_axis.append(gen)
            y_axis.append(avg)
        plt.plot(x_axis, y_axis) 
        plt.savefig('evolving_prog'+str(world+16)+'.png')
        plt.clf()
    

class Player (): 
    def __init__(self, nodes) :
        self.nodes = nodes
        self.weights = None
        self.k = None

    def inst(self, net_dict) :
        self.weights = net_dict['weights']
        self.k = net_dict['K']
    
    def find_value(self, board) :
        #'''
        v_board = self.vector_board(board)
        output_node = self.nodes[len(self.nodes)-1][0]
        #output_node = output_node[0]
        val = output_node.output(self.weights, v_board)
        self.reset_nodes()
        '''
        v_board = self.vector_board(board)
        for id in range(4) :
            for node in self.nodes[id] :
                node.output(self.weights, v_board)
        output_node = self.nodes[len(self.nodes)-1]
        output_node = output_node[0]
        val = output_node.output(self.weights, v_board)
        self.reset_nodes()
        #'''

        return val#uniform(1,-1)
    
    def reset_nodes(self) :
        for (id, layer) in self.nodes.items() :
            for node in layer :
                node.saved = None

    def vector_board(self, board) :
        v_board = []
        for row_id in range(len(board)) :
            row = board[row_id]
            for space_id in range((1+row_id)%2, len(row), 2) :
                space = row[space_id]
                if space == -1 :
                    v_board.append(self.k)
                elif space == -2 :
                    v_board.append(- self.k)
                elif space == 2 :
                    v_board.append(-1)
                else :
                    v_board.append(space)
        return v_board
