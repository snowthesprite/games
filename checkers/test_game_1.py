from game_2 import Checkers
from input_plr import *
from rand_plr import *
import time
'''
results = {1: 0, 2: 0, 'Tie': 0}

players = [TreePlayerHeuristic(4), Row3()]
game = Con4(players)
game.run_to_completion()
results[game.winner]+= 1
print(results)


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

#print(chr(0+97) + 'a')

#'''
#players = [InputPlayer(), RandPlr()]
t1 = time.time()
players = [RandPlr(), RandPlr()]
game = Checkers(players)
#print(game.board)
game.run_game()
t2 = time.time()

print(t2-t1)
'''
for _ in range(100) :
    players = [RandPlr(), RandPlr()]
    game = Checkers(players)
    game.run_game()
#'''
