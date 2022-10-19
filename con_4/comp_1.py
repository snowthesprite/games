import sys
sys.path.append('con_4/games')
from game_1 import Con4
from rand_plr import Row3
from anton_last import AntonLM
from cayden_last import CaydenLM
from charlie_last import CharlieLM
from justin_last import JustinLM
from adaptor import Adaptor

'''
results = {1: 0, 2: 0, 'Tie': 0}

players = [TreePlayerHeuristic(4), Row3()]
game = Con4(players)
game.run_to_completion()
results[game.winner]+= 1
print(results)


'''
others =  [('Cayden', CaydenLM()), ('Charlie', CharlieLM()), ('Justin', JustinLM()), ('Anton', AntonLM())]
tests = 10

for op in others :

    results = {1: 0, 2: 0, 'Tie': 0}
    #print('\n\n')
    for loop in range(tests) :
        #print(loop)
        players = [Row3(), Adaptor(op[1])]
        game = Con4(players)
        game.run_to_completion()
        results[game.winner]+= 1

    print(results)
    print('Percentage Won by Maia LM Plr:', results[1]/tests)
    print('Percentage Won by '+op[0]+' LM Plr:', results[2]/tests)
    print('Percentage of Cats Games:', results['Tie']/tests)