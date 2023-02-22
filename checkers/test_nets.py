from neural_nets import *
import math
import time
import matplotlib.pyplot as plt
import pickle

node_layers = [32,40,10, 1]

weights = 9

worlds = 5

nn = NeuralNet(node_layers, lambda x: 2*x)
w = nn.make_weights()
print(len(w))
##nnf = NeuralNetField(node_layers, lambda x: 1 / (1 + math.e ** (-x)))