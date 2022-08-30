import sys
sys.path.append('tic_tac_toe/players')
sys.path.append('tic_tac_toe/games')
from game_4 import TicTacToe
from random_player_3 import RandomPlayer
from tree_player import TreePlayer

results = {1: 0, 2: 0, 'Tie': 0}

tests = 10

#'''
for loop in range(tests) :
    print(loop)
    players = [RandomPlayer(), TreePlayer()]
    #if loop % 2 == 1 :
        #players = players[::-1]

    game = TicTacToe(players)
    game.run_to_completion()
    results[game.winner] += 1

print(results)
print('Percentage Won by Plr 0:', results[1]/tests)
print('Percentage Won by Plr 1:', results[2]/tests)
print('Percentage of Cats Games:', results['Tie']/tests)
#'''
