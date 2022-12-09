from neural_nets import *
import math
import time
'''
board = '000000000'

def vector_board(board) :
    v_board = []
    for space in board :
        if space == '1' :
            v_board.append(1)
        elif space == '2' :
            v_board.append(-1)
        else :
            v_board.append(0)
    return v_board
'''

node_layers = [9,10,9]

data = 0

weights = 9

nnf = NeuralNetField(node_layers, lambda x: 1 / (1 + math.e ** (-x)))
#'''
t_1 = time.time()
nnf.create_gen(50)
t_2 = time.time()
print('Creation:', t_2 - t_1)

#for (connection, weight) in nn.weights.items() :
#    print(connection, weight)
amt = 200
t_1 = time.time()
gen_scores = nnf.evolve(amt)
t_2 = time.time()
print('Evolution:', (t_2-t_1)/amt)

#'''
import matplotlib.pyplot as plt
plt.style.use('bmh')
x_axis = []
y_axis = []
for (gen, avg) in gen_scores.items() :
    x_axis.append(gen)
    y_axis.append(avg)
plt.plot(x_axis, y_axis) 
plt.savefig('evolving.png')
#'''

