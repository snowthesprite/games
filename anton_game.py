from random import random

class ConnectFour:
  def __init__(self, players, log_name='logs.txt'):
    self.players = players
    self.logs = Logger('/home/runner/'+log_name)
    self.logs.clear_log()
    self.set_player_symbols()
    self.set_player_numbers()
    #self.determine_player_order()
    self.board = [[None for _ in range(6)] for _ in range(7)] #transpose; columns are lists
    self.round =  1
    self.winner = None
    self.log_board()
  
  def set_player_symbols(self): 
    self.players[0].set_player_symbol('1')
    self.players[1].set_player_symbol('2')

  def set_player_numbers(self): 
    self.players[0].set_player_number(1)
    self.players[1].set_player_number(2)
  
  # def determine_player_order(self):
  #   # rand = round(random())
  #   # if rand == 1:
  #   #   self.players = self.players[::-1]
  #   first_symbol = self.players[0].symbol
  #   self.players[0].set_first(first_symbol)
  #   self.players[1].set_first(first_symbol)

  def get_possible_moves(self):
    possible_moves = [i for i in range(7) if None in self.board[i]]
    return possible_moves

  def complete_round(self):
    for player in self.players:
      choices = self.get_possible_moves()
      if choices != [] and self.check_for_winner() == None:
        player_move = player.choose_move(self.board, choices)
        i = 0
        while i+1 < 6 and self.board[player_move][i+1]==None:
          i+=1
        self.board[player_move][i] = player.symbol
      self.log_board()
    self.round += 1

  def run_to_completion(self):
    while self.winner == None:
      self.complete_round()
      self.winner = self.check_for_winner()
    self.logs.write('PLAYER '+str(self.winner)+' HAS WON \n')

  def get_diagonals(self, row_index):
    forward_diag = []
    back_diag = []
    
    forward_coord = [row_index, 3]
    back_coord = [row_index, 3]
    while back_coord[0] >= 0 and back_coord[1] >= 0:
      forward_diag.append(self.board[forward_coord[1]][forward_coord[0]])
      back_diag.append(self.board[back_coord[1]][back_coord[0]])
      forward_coord[0]-=1
      back_coord[0]-=1
      forward_coord[1]+=1
      back_coord[1]-=1

    forward_coord = [row_index+1, 2]
    back_coord = [row_index+1, 4]
    while back_coord[0] <= 5 and back_coord[1] <= 6:
      forward_diag.insert(0,self.board[forward_coord[1]][forward_coord[0]])
      back_diag.insert(0,self.board[back_coord[1]][back_coord[0]])
      forward_coord[0]+=1
      back_coord[0]+=1
      forward_coord[1]-=1
      back_coord[1]+=1
      
    return [forward_diag, back_diag]

  def get_all_diagonals(self):
    all_diags = []
    for i in range(6):
      all_diags += self.get_diagonals(i)
    return all_diags

  def four_in_a_row(self, player, line):
    four_str = ''.join([player.symbol for _ in range(4)])
    line_str = ''.join([val if val != None else '0' for val in line])

    return four_str in line_str
  
  def check_for_winner(self):
    cols = self.board.copy()
    rows = self.transpose_board()
    diags = self.get_all_diagonals()

    board_full = True
    for line in (rows + cols + diags):
      if None in line:
        board_full = False

      for player in self.players:
        if self.four_in_a_row(player, line):
          return player.number
    
    if board_full:
      return 'Tie'
    return None
  
  def transpose_board(self):
    return [[self.board[i][j] for i in range(7)] for j in range(6)] 
  
  def log_board(self):
    transpose_board = self.transpose_board()
    for i in range(len(transpose_board)):
      row = transpose_board[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      self.logs.write(row_string[:-1]+'\n')
    self.logs.write('\n')
  
  def print_board(self):
    transpose_board = self.transpose_board()
    for i in range(len(transpose_board)):
      row = transpose_board[i]
      row_string = ''
      for space in row:
        if space == None:
          row_string += '_|'
        else:
          row_string += space + '|'
      print(row_string[:-1])
    print('\n')

class Logger:
  def __init__(self, filename = 'log.txt'):
    self.filename = filename

  def clear_log(self):
    with open(self.filename, 'w') as file:
      file.writelines([''])

  def write(self, string = None):
    with open(self.filename, 'a') as file:
      file.writelines([string])