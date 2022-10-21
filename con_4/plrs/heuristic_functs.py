'''
Generation 1
initialization
#2ply : 0.00579380989074707
#3ply : 0.031876564025878906 
#4ply : 0.16466116905212402
#5ply : 1.1452903747558594
#6ply : 9.395210981369019


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
'''

##MUST GO INSIDE CON TREE
'''
Generation 2
Initialization, secondary
2ply: 0.008117, 0.007983
3ply: 0.047439, 5.675436 * 10**-5
4ply: 0.225950, 5.268050 * 10**-5
5ply: 1.319004, 9.608268 * 10**-5
6ply: 9.964441, 0.000177
7ply: 99

    def heuristic_funct(self, board) :
        moves = self.get_possible_moves(self.flaten_board(board))
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
        nmy = (self.max_plr % 2) + 1
        win = ''.join([str(self.max_plr) for _ in range(3)])
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

'''