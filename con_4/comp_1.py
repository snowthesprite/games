import sys
sys.path.append('con_4/games')
from game_1 import Con4
from comp_plr import Maia
from anton_comp import Anton
from cayden_comp import Cayden
from charlie_comp import Charlie
from justin_comp import Justin
from william_comp import William
from adaptor import Adaptor

'''
results = {1: 0, 2: 0, 'Tie': 0}

players = [TreePlayerHeuristic(4), Row3()]
game = Con4(players)
game.run_to_completion()
results[game.winner]+= 1
print(results)


'''
others =  [('Maia', Maia()), ('Cayden', Adaptor(Cayden())), ('Charlie', Adaptor(Charlie())), ('Justin', Adaptor(Justin())), ('Anton', Adaptor(Anton()))]
tests = 4
#'''
for id_1 in range(1,5) :
    plr_1 = others[id_1]
    for id_2 in range(3 + id_1, 5) :
        plr_2 = others[id_2]
        results = {1: 0, 2: 0, 'Tie': 0}
        #print(plr_1[0], plr_2[0], '\n\n')
        for loop in range(tests) :
            #print(loop)
            players = [plr_1[1], plr_2[1]]
            game = Con4(players, loop)
            game.run_to_completion()
            results[game.winner]+= 1

        print(results)
        print('Percentage Won by '+plr_1[0]+':', results[1]/tests)
        print('Percentage Won by '+plr_2[0]+':', results[2]/tests)
        print('Percentage of Ties:', results['Tie']/tests)
        print('\n\n')
#'''
'''
plrs = [others[0][1], others[1][1]]
game = Con4(plrs, 0)
game.run_to_completion()
#'''