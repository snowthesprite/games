from neural_nets import *
import math
import time
import matplotlib.pyplot as plt
import pickle
import random
import numpy.random
## python checkers/test_nets.py -> output.txt

## Game runs much slower in debug mode

## At 2 Ply:
## Games: 4.4 sec
## Hurst: 0.001 sec
## Reset Kids: 1.11E^-5 sec
## Create kids: 0.0003 sec
## Prune Tree" 0.002 sec
## Assign Values: 0.043 sec
## Find moves: 6.11E^-5 sec
## Create Nodes: 0.002 sec

numpy.random.seed(10)
random.seed(10)

node_layers = [32,40,10, 1]

weights = 1742

worlds = 5
pop = 2
'''
t1 = time.time()
nn = NeuralNet(node_layers, lambda x: 2*x)
w = nn.make_weights()
print(len(w))
t2 = time.time()
print(t2-t1)
##nnf = NeuralNetField(node_layers, lambda x: 1 / (1 + math.e ** (-x)))
'''

nnf = NeuralNetField(node_layers, weights, lambda x: math.tanh(x))
nnf.create_gen(pop)
nnf.evolve(2,1)
#nnf.calc_score(nnf.curr_gen[0],0)z

b=nnf.times['games']
print('games', sum(b)/len(b))
#print('p1')
nnf.p1.print_times()
#print('\n\n')
#print('p2')
#nnf.p2.print_times()
#'''