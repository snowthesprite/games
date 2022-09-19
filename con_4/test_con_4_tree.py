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
l_dias = []
r_dias = []
for dia in diagonals :
    l_dias.append([board[index] for index in range(dia[0],dia[1]-1,-6 )])
    r_dias.append([board[index] for index in range(dia[0] + 6,dia[1]-1,-8 )])
print(l_dias)
print()
print(r_dias)
'''
diagonals = [(3,0),(4,0),(5,0),(5,1),(5,2),(5,3)]
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
    

#print(l_dias)
#print()
#print(r_dias)
s = '01110001'
l = ['11111','234321','3201']
print('1111' in s)
print('0' in l[2])

for row in range(5,-1,-1) : 
    print(row)
#'''