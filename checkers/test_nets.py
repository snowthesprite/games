from neural_nets import *
import math
import time
import matplotlib.pyplot as plt
import pickle
import random
import numpy.random

## At 2 Ply:
## Games: 224.23 sec
## Hurst: 0.06 sec
## Reset Kids: 2.37E^-5 sec
## Create kids: 0.0006 sec
## Prune Tree" 0.0038 sec
## Assign Values: 2.53 sec / With Shared Tree: 3.0 (Less amount run)
## Find moves: 0.0002 sec
## Create Nodes: 0.004 sec

#numpy.random.seed(10)
#random.seed(101)

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

nnf = NeuralNetField(node_layers, weights, lambda x: 1 / (1 + math.e ** (-x)))
nnf.create_gen(pop)
nnf.evolve(2,1)

b=nnf.times['games']
print('games', sum(b)/len(b))
print('\n\n') 
print('p1')
nnf.p1.print_times()
print('\n\n')
print('p2')
nnf.p2.print_times()
#'''