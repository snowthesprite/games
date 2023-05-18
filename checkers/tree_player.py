#import sys
#sys.path.append('tic_tac_toe/games')
from game_tree import *
import time as t

class TreePlayerNet :
    def __init__(self, heurist, num, tree, layers=2) :
        self.layers = layers
        self.heurist = heurist
        self.num = num #None
        self.tree = tree#CheckersTree(num, self.layers, self.heuristic)#None
        self.times = {'heuristic':[]}

    def heuristic(self, board) :
        t1 = t.time()
        h = self.heurist.find_value(board)
        t2 = t.time()
        self.times['heuristic'].append(t2-t1)
        return h#self.heurist.find_value(board)
  
    def set_player_info(self, n) :
        self.num = n
        self.tree = CheckersTree(n, self.layers, self.heuristic)

    def choose_move(self, board, choices) :
        self.tree.prune_tree(board, self.num)
        self.tree.assign_values(self.num, self.heuristic)

        #'''
        best = (None, -10)
        for choice in choices :
            update = self.tree.run_move(choice, board)
            update = self.tree.list_to_str(update, (self.num)%2+1)
            if self.tree.nodes[update].score >= best[1] :
                best = (choice, self.tree.nodes[update].score)
        return best[0]
        '''
        best = -10
        all_scores = []
        choicess = self.order_left(choices)
        for choice in choicess :
            update = self.tree.run_move(choice, board)
            update = self.tree.list_to_str(update, (self.num)%2+1)
            all_scores.append(self.tree.nodes[update].score)
            cur_node = self.tree.nodes[update]
            if cur_node.score > best :
                best_choices = [choice]
                best = cur_node.score
            elif cur_node.score == best :
                best_choices.append(choice)
        ordered_best = self.order_left(best_choices)
        return ordered_best[0]
        #'''

    def order_left(self, all_moves) :
        LeftMostPiece = all_moves.sort(key =lambda move : move[0][1])
        LeftMostMove = all_moves.sort(key =lambda move : move[1][1])
        TopMostPiece = all_moves.sort(key =lambda move : move[0][0])
        TopMostMove = all_moves.sort(key =lambda move : move[1][0])
        return all_moves

    def print_times(self) :
        for key in self.times :
            tt = self.times[key]
            print(key, sum(tt)/len(tt))
        
        for key in self.tree.times :
            tt = self.tree.times[key]
            print(key, sum(tt)/len(tt))