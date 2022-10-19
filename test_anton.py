from game import *
from rand_plr import *
from anton_strat import *

results = {1: 0, 2: 0, 'Tie':0}

print('First 50')
for _ in range(50):
  print(_)
  players = [Adaptor(), Row3()]
  game = Con4(players)
  game.run_to_completion()
  results[game.winner]+= 1

print(num_wins)
'''
num_wins = {1: 0, 2: 0, 'Tie':0}

print('Next 50')
for _ in range(50):
  players = [RandomPlayer(), HeuristicPlayer()]
  game = ConnectFour(players)
  game.run_to_completion()
  winner = game.winner
  print(winner)
  num_wins[winner] += 1
  
print(num_wins)


players = [HeuristicPlayer(), RandomPlayer()]
game = ConnectFour(players)
game.run_to_completion()
winner = game.winner
'''