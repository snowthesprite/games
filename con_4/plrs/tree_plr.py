import sys
sys.path.append('con_4/games')
from con_4_tree import Con4Tree

class TreePlayerHeuristic :
    def __init__(self, layers) :
        self.num = None
        self.tree = None
        self.layers = layers

    def heuristic(self, board) :
        rows = [board[row] for row in range(6)] #row
        cols = [''.join([board[row][col] for row in range(6)]) for col in range(7)]
        l_dias = []
        r_dias = []
        diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
        for (row, col) in diagonals :
            i=0
            l_dia = []
            r_dia = []
            while row-i >=0 and col+i <= 6 :
                l_dia.append(board[row-i][col+i])
                r_dia.append(board[row-i][6-col-i])
                i+= 1
            l_dias.append(l_dia)
            r_dias.append(r_dia)
        
        win_process = rows + cols + l_dias + r_dias

        good_set = 0
        bad_set = 0
        for thing in win_process :
            good_num = thing.count(str(1))
            bad_num = thing.count(str(2))
            empty = thing.count('0')
            if good_num >= 2 and empty >= 2 :
                good_set+= 1
            if bad_num >= 2 and empty >= 2 :
                bad_set+=1
        return (good_set-bad_set)/len(win_process)
  
    def set_player_info(self, n) :
        self.num = n
        self.tree = Con4Tree(n, self.layers, self.heuristic)

    def choose_move(self, board, choices) :
        self.tree.prune_tree(board)
        best = (None, -1)
        #print(self.tree.nodes.keys())

        for col in choices :
            update = board.copy()
            choice = self.find_row(board, col)
            update[choice[0]] = board[choice[0]][:choice[1]] + str(self.num) + board[choice[0]][choice[1]+1:]
            flatdate = self.tree.flaten_board(update)
            if self.tree.nodes[flatdate].score >= best[1] :
                best = (choice, self.tree.nodes[flatdate].score)
        return best[0]

    def find_row(self, board, col) :
        for row in range(5,-1,-1) :
            if board[row][col] == '0' :
                return (row, col)

