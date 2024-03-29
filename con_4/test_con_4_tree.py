'''
board = ['00','01','02','03','04','05','06',
         '07','08','09','10','11','12','13',
         '14','15','16','17','18','19','20',
         '21','22','23','24','25','26','27',
         '28','29','30','31','32','33','34',
         '35','36','37','38','39','40','41']

rows = [board[index:index+7] for index in range(0,41,7)] #row
#print(rows)
cols = [[board[index + mult*7] for mult in range(6)] for index in range(7)]
#print(cols)
diagonals = [(21,3),(28,4),(35,5),(36,6),(37,13),(38,20)]
dia = diagonals[3]
print(dia)
print([board[index] for index in range(dia[0] + 6,dia[1]-6,-8 )])
'''
'''
l_dias = []
r_dias = []
for dia in diagonals :
    l_dias.append([board[index] for index in range(dia[0],dia[1]-1,-6 )])
    r_dias.append([board[index] for index in range(dia[0] + 6,dia[1]-1,-8 )])
print(l_dias)
print()
print(r_dias)
'''
'''
board = [['00','01','02','03','04','05','06'],
         ['10','11','12','13','14','15','16'],
         ['20','21','22','23','24','25','26'],
         ['30','31','32','33','34','35','36'],
         ['40','41','42','43','44','45','46'],
         ['50','51','52','53','54','55','56']]

diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]

l_dias = []
r_dias = []

for (row, col) in diagonals :
    i=0
    l_dia = []
    r_dia = []
    while row-i >=0 and col+i <= 6 :
        ##l_dias.append(''.join([board[row-i][col+i] for i in range(row-col+1)]))
        ##r_dias.append(''.join([board[row-i][6-col-i] for i in range(row-col+1)]))
        l_dia.append(board[row-i][col+i])
        r_dia.append(board[row-i][6-col-i])
        i+= 1
    l_dias.append(l_dia)
    r_dias.append(r_dia)
    

print(l_dias)
print()
print(r_dias)
s = '01110001'
l = ['11111','234321','3201']
print('1111' in s)
print('0' in l[2])
board = l.copy()
board[0] = board[0][:2] + 'y' + board[0][3:]
print(l)
print(board)
print(''.join(l))
#'''
'''
board = ['00','01','02','03','04','05','06',
         '07','08','09','10','11','12','13',
         '14','15','16','17','18','19','20',
         '21','22','23','24','25','26','27',
         '28','29','30','31','32','33','34',
         '35','36','37','38','39','40','41']

new = [board[index:index+7] for index in range(0,41,7)]
print(new)

#'''
#'''
import sys
sys.path.append('con_4/games')
from con_4_tree import Con4Tree
import time

def print_board(board):
    for row in board:
        row_string = '|'
        for col in row :
            if col == '0' :
                row_string += ' |'
            else:
                row_string += col + '|'
        print(row_string)
        print('---------------')

def heuristic(board) :
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

def get_possible_moves(board) :
        #print(game_state)
        possible_moves = []
        
        cols = [[(row,col) for row in range(5,-1,-1)] for col in range(7)]
        for col in cols :
            for (row, col) in col :
                if board[row][col] == '0' :
                    possible_moves.append((row,col))
                    break
        return possible_moves     

def size(board) :
        moves = self.get_possible_moves(board)
        rows = [board[row] for row in range(6)] #row
        rows_m = [[(row, col) for col in range (7)] for row in range(6)]
        cols = [''.join([board[row][col] for row in range(6)]) for col in range(7)]
        cols_m = [[(row,col) for row in range(6)] for col in range(7)]
        l_dias = []
        r_dias = []
        l_dias_m = []
        r_dias_m = []
        diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
        for (row, col) in diagonals :
            i=0
            l_dia = []
            r_dia = []
            l_dia_m = []
            r_dia_m = []
            while row-i >=0 and col+i <= 6 :
                l_dia.append(board[row-i][col+i])
                r_dia.append(board[row-i][6-col-i])
                l_dia_m.append((row-1,col+i))
                r_dia_m.append((row-i,6-col-i))
                i+= 1
            l_dias.append(''.join(l_dia))
            r_dias.append(''.join(r_dia))
            l_dias_m.append(l_dia_m)
            r_dias_m.append(r_dia_m)
        
        thing = rows + cols + l_dias + r_dias
        thing_m = rows_m + cols_m + l_dias_m + r_dias_m

        good = 0
        bad = 0
        nmy = (self.num % 2) + 1
        win = ''.join([str(self.num) for _ in range(3)])
        lose = ''.join([str(nmy) for _ in range(3)])
        lose_2 = f"{nmy}0{nmy}{nmy}"
        lose_3 = f"{nmy}{nmy}0{nmy}"
        for index in range(len(thing)) :
            if set(thing_m[index]).isdisjoint(set(moves)):
                continue
            if win in thing[index] :
                good += 1
            elif lose in thing[index] or lose_2 in thing[index] or lose_3 in thing[index]:
                bad += 1
        return (good-bad)

board = [''.join(['0' for _ in range(7)]) for __ in range(6)]
'''
t_1 = time.time()
heuristic(board)
t_2 = time.time()
print(t_2-t_1)

'''
tree = Con4Tree(1, 7, 'size')
t_1 = time.time()
tree.prune_tree(board)
t_2 = time.time()
print(t_2-t_1)

board[5] = '1200000'

t_1 = time.time()
tree.prune_tree(board)
t_2 = time.time()
print(t_2-t_1)

#'''
'''
for node in tree.nodes :
    thing = tree.inflate_board(node)
    print('\n\n')
    print_board(thing)
#'''