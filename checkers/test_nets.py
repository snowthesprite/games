from neural_nets import *
import math
import time
import matplotlib.pyplot as plt
import pickle
import random
random.seed(10)

node_layers = [32,40,10, 1]

weights = 1742

worlds = 5
pop = 5
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
#'''