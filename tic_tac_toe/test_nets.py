from neural_nets import *
import math
import time
import matplotlib.pyplot as plt
import pickle

plt.style.use('bmh')

def make_graph(gen) :
    x_axis = []
    y_axis = []
    for (gen, max) in gen_scores.items() :
        x_axis.append(gen)
        y_axis.append(max)
    plt.plot(x_axis, y_axis) 
    plt.savefig('evolving.png')
    plt.clf()
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

weights = 9

worlds = 5

nnf = NeuralNetField(node_layers, lambda x: 1 / (1 + math.e ** (-x)))
amt = 100
pop = 50
all_scores = []

#nnf.create_gen(50)
#t1=time.time()
#gen_scores = nnf.evolve(amt)
#t2=time.time()
#print('total',t2-t1)

#'''
t1=time.time()
for _ in range(worlds) :
    print(_)
    nnf.create_gen(pop)
    gen_scores = nnf.evolve(amt, _)
    
    
    all_scores.append(gen_scores)
    #make_graph(gen_scores, _)
    #print(gen_scores)
    with open('lastgens.pickle', 'ab') as handle:
        pickle.dump([nnf.curr_gen, gen_scores], handle, protocol=pickle.HIGHEST_PROTOCOL)

t2=time.time()
print('world:', (t2-t1)/(amt*worlds))

#with open('allscores.pickle', 'wb') as handle:
#    pickle.dump(all_scores, handle, protocol=pickle.HIGHEST_PROTOCOL)

#graph_all = {_: sum([world[_] for world in all_scores])/worlds for _ in range(amt)}

#make_graph(graph_all)

'''

def loadall(filename):
    objects = []
    with open(filename, "rb") as f:
        while True:
            try:
                #yield pickle.load(f)
                objects.append(pickle.load(f))
            except EOFError:
                break
    return objects

items = loadall('filename.pickle')
#print(items)

#gen_scores = [max([nnf.net.calc_score(inst['weights']) for inst in thing]) for thing in items]
gen_scores = [thing[1] for thing in items]
print(gen_scores)
#'''


'''
objects = []
with (open("filename.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
#'''