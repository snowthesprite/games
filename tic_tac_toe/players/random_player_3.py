## Shared Implimentation
from random import random
from random import seed
import math
seed(1)

class RandomPlayer:
  def __init__(self):
    self.num = None
  
  def set_player_info(self, n, board):
    self.num = n
  
  def choose_move(self, board, choices):
    random_idx = math.floor(len(choices) * random())
    return choices[random_idx]