import sys
sys.path.append('tic_tac_toe/players')
sys.path.append('tic_tac_toe/games')
from game_4 import TicTacToe
from random_player_3 import RandomPlayer
from tree_player_2 import TreePlayerHeuristic
from tree_player import TreePlayer
#from input_player import InputPlayer

results = {1: 0, 2: 0, 'Tie': 0}

tests = 10

#'''
for loop in range(tests) :
    #print(loop)
    players = [TreePlayer(), TreePlayerHeuristic(9)]
    #if loop % 2 == 1 :
    #    players = players[::-1]

    game = TicTacToe(players)
    game.run_to_completion()
    results[game.winner] += 1

print(results)
print('Percentage Won by Full Tree Plr:', results[1]/tests)
print('Percentage Won by Heuristic (9) Plr:', results[2]/tests)
print('Percentage of Cats Games:', results['Tie']/tests)
#'''

#'''
results = {1: 0, 2: 0, 'Tie': 0}
print('\n\n')
for loop in range(tests) :
    #print(loop)
    players = [TreePlayerHeuristic(5), TreePlayerHeuristic(9)]
    #if loop % 2 == 1 :
    #    players = players[::-1]

    game = TicTacToe(players)
    game.run_to_completion()
    results[game.winner] += 1

print(results)
print('Percentage Won by Heuristic (5) Plr:', results[1]/tests)
print('Percentage Won by Heuristic (9) Plr:', results[2]/tests)
print('Percentage of Cats Games:', results['Tie']/tests)
#'''

#'''
results = {1: 0, 2: 0, 'Tie': 0}
print('\n\n')
for loop in range(tests) :
    #print(loop)
    players = [TreePlayerHeuristic(5), RandomPlayer()]
    #if loop % 2 == 1 :
    #    players = players[::-1]

    game = TicTacToe(players)
    game.run_to_completion()
    results[game.winner] += 1

print(results)
print('Percentage Won by Heuristic (5) Plr:', results[1]/tests)
print('Percentage Won by Rand Plr:', results[2]/tests)
print('Percentage of Cats Games:', results['Tie']/tests)
#'''
