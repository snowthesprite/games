board = [['00','01','02','03','04','05','06'],
         ['10','11','12','13','14','15','16'],
         ['20','21','22','23','24','25','26'],
         ['30','31','32','33','34','35','36'],
         ['40','41','42','43','44','45','46'],
         ['50','51','52','53','54','55','56']]

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