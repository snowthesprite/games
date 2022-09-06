import sys
sys.path.append('tic_tac_toe/games')
from game_tree_4 import TicTacToeTree

class TreePlayerHeuristic :
    def __init__(self, layers) :
        self.num = None
        self.tree = None
        self.layers = layers

    def heuristic(self, board) :
        win_process = [board[index: index+3] for index in range(0,9,3)] #row
        for index in range(3) :
            win_process.append(board[index] + board[index+3] + board[index+6]) #column
        win_process.extend([board[0] + board[4] + board[8], board[2] + board[4] + board[6]]) #diagonal

        good_set = 0
        bad_set = 0
        for thing in win_process :
            good_num = thing.count(str(self.num))
            bad_num = thing.count(str((self.num%2)+1))
            if good_num == 2 and bad_num == 0 :
                good_set+= 1
            if bad_num == 2 and good_num == 0 :
                bad_set+=1
        return (good_set-bad_set)/8
  
    def set_player_info(self, n, board) :
        self.num = n
        self.tree = TicTacToeTree(n, self.layers, self.heuristic)
        #self.tree.assign_values()

    def choose_move(self, board, choices) :
        self.tree.prune_tree(board)
        #tree.assign_values()
        best = (None, -1)
        for choice in choices :
            update = board[:choice] + str(self.num) + board[choice+1:]
            if self.tree.nodes[update].score >= best[1] :
                best = (choice, self.tree.nodes[update].score)
        return best[0]