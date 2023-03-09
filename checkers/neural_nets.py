##For specifically Checkers

from random import choice
from numpy.random import normal, uniform, randint
import math

import matplotlib.pyplot as plt
plt.style.use('bmh')

#'''
## Takes approximently 0.006 sec for generation
class NetNode (): 
    def __init__(self, id, act_funct) :
        #xs is the input, or in this case, the board
        self.spec = None
        self.id = id
        self.parents = []
        self.act_funct = act_funct
        self.value = lambda weights, xs : sum([weights[(parent.id, self.id)] * parent.output(weights,xs) for parent in self.parents])
    
    def output(self, weights, input) :
        return self.act_funct(self.value(weights, input))
    
    def input(self) :
        self.value = lambda weights, xs : xs[self.id-1]

    def piece_value(self) :
        self.value = lambda weights, xs : sum([parent.value for parent in self.parents])

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
        #Makes piece Difference
        new_node = NetNode(id+1, act_funct)
        new_node.parents = self.make_node_specifics(1)
        new_node.piece_value()
        new_node.spec = 'piece'
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
        queue = self.nodes[len(self.nodes)-1]
        while queue != [] :
            node_to = queue[0]
            queue.pop(0)
            if node_to.spec == 'piece' :
                continue
            for node_from in node_to.parents :
                weights[(node_from.id, node_to.id)] = uniform(-0.2, 0.2)
            queue.extend([node for node in node_to.parents if node not in queue])
        return weights

class NeuralNetField (): 
    def __init__(self, layers, num_weights, act_funct) :
        #self.mut_rate = 0.05
        self.num_weights = num_weights
        self.net = NeuralNet(layers, act_funct)
        self.curr_gen = []
        self.p1 = Player(self.net.nodes)
        self.p2 = Player(self.net.nodes)

    def reproduce(self, parent, amount=1) :
        mutate = parent['mutate'] * math.exp(normal() / (2**(1/2) * self.num_weights ** (1/4)))
        k = parent['K'] * math.exp(normal() / (2**(1/2)))
        if k < 1 :
            k = 1
        elif k > 3 :
            k = 3

        child = {'weights': {}, 'mutate': mutate, 'K': k}
        for (connect, weight) in parent.weights.items() :
            child['weights'][connect] = weight + mutate * normal()
        return child

    def calc_score(self, plr) :
        score = 0
        p1.inst(plr)
        for _ in range(5) :
            p2.inst(choice(self.curr_gen))
            game = Checkers([p1, p2])
            game.run_game()
            if game.winner == 1 :
                score += 1
            if game.winner == 2 :
                score -= 2
        return score

    def evolve(self, gens, world) :
        generations = {}
        for gen in range(gens) :
            if gen % 50 == 0 :
                print('Gen', gen)
                self.in_prog_graph(generations, world)

            scores = [(id, self.calc_score(self.curr_gen[id])) for id in range(30)]
            scores.sort(reverse=True, key=(lambda scr : scr[1]))
            
            cont_pop = [self.curr_gen[net[0]] for net in scores[:15]]
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
        
'''
class TicTacToe:
    def __init__(self, nn, enemy):
        self.players = [nn, enemy]
    
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
'''

class Player (): 
    def __init__(self, nodes) :
        self.nodes = nodes
        self.weights = None
        self.k = None

    def inst(self, net_dict) :
        self.weights = net_dict['weights']
        self.k = net_dict['k']

    ## NEED TO CHANGE
    
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

    ## END NEED TO CHANGE
