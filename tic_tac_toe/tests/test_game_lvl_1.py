#import sys
#sys.path.append('players')
#sys.path.append('games')
from game_1 import *
from random_player import RandomPlayer

results = {0: 0, 1: 0, 'Cats Game': 0}

tests = 1000

for loop in range(tests) :
    players = [RandomPlayer(), RandomPlayer()]

    game = Tic_Tac_Toe(players, loop % 2)
    game.run_to_completion()
    results[game.winner] += 1

print(results)
print('Percentage Won by Plr 0:', results[0]/tests)
print('Percentage Won by Plr 1:', results[1]/tests)
print('Percentage of Cats Games:', results['Cats Game']/tests)
