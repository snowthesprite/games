import sys
sys.path.append('tic_tac_toe/players')
sys.path.append('tic_tac_toe/games')
from game_1 import Game
from random_player import RandomPlayer

results = {0: 0, 1: 0, 'Cats Game': 0}

tests = 1000

for loop in range(tests) :
    players = [RandomPlayer(), RandomPlayer()]

    game = Game(players, loop % 2)
    game.run_to_completion()
    results[game.winner] += 1

print(results)
print('Percentage Won by Plr 0:', results[0]/tests)
print('Percentage Won by Plr 1:', results[1]/tests)
print('Percentage of Cats Games:', results['Cats Game']/tests)
