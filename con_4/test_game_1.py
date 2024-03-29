import sys
sys.path.append('con_4/games')
from game_1 import Con4
from comp_plr import *
from rand_plr import Row3

'''
results = {1: 0, 2: 0, 'Tie': 0}

players = [TreePlayerHeuristic(4), Row3()]
game = Con4(players)
game.run_to_completion()
results[game.winner]+= 1
print(results)


'''
tests = 20
results = {1: 0, 2: 0, 'Tie': 0}
#print('\n\n')
for loop in range(tests) :
    print(loop)
    players = [HeuristicStrat(4), Row3()]
    game = Con4(players)
    game.run_to_completion()
    results[game.winner]+= 1

print(results)
print('Percentage Won by Heuristic (4) Plr:', results[1]/tests)
print('Percentage Won by Row3 Plr:', results[2]/tests)
print('Percentage of Cats Games:', results['Tie']/tests)
#'''

