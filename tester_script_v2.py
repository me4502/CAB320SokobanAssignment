
'''

New version of the tester script.

Main change is a more tolerant checking function for the 'taboo_cells' function.
Look at the 'same_multi_line_strings' function to see how multi-line strings will be compared.

added functions 
  same_multi_line_strings(s1,s2)
  test_check_macro_action_seq


A  similar script (with different inputs) will be used for marking your code.

Make sure that your code runs without errors with this script.


'''


from __future__ import print_function
from __future__ import division


from sokoban import Warehouse

from mySokobanSolver import my_team, taboo_cells, SokobanPuzzle, check_action_seq
from mySokobanSolver import solve_sokoban_elem, can_go_there, solve_sokoban_macro 




puzzle_t1 ='''
#######
#@ $. #
#######'''

puzzle_t2 ='''
  #######
  #     #
  # .$. #
 ## $@$ #
 #  .$. #
 #      #
 ########
'''

puzzle_t3 ='''
#######
#@ $ .#
#. $  #
#######'''

expected_answer_3 ='''
#######
#X    #
#    X#
#######'''


expected_answer_1 =''' 
 ####
 # .#
 #  ###
 #*   #
 #  $@#
 #  ###
 ####
'''

def same_multi_line_strings(s1,s2):
    '''
    Auxiliary function to test two multi line string representing warehouses
    '''
    L1 = [s.rstrip() for s in s1.strip().split('\n')]
    L2 = [s.rstrip() for s in s2.strip().split('\n')]
    S1 = '\n'.join(L1)
    S2 = '\n'.join(L2)
    return S1==S2
    


def test_warehouse_1():
    wh = Warehouse()
    # read the puzzle from the multiline string 
    wh.extract_locations(puzzle_t2.split(sep='\n'))
    print("\nPuzzle from multiline string")
    print(wh)

def test_warehouse_2():
    problem_file = "./warehouses/warehouse_01.txt"
    wh = Warehouse()
    wh.read_warehouse_file(problem_file)
    print("\nPuzzle from file")
    print(wh)
    print(wh.worker) # x,y  coords !!
    print(wh.walls)  # x,y  coords !!
    
def test_taboo_cells():
    wh = Warehouse()
    wh.extract_locations(puzzle_t3.split(sep='\n'))
    answer = taboo_cells(wh)
    # begin debug
    print(answer)
    print(len(answer))
    print(expected_answer_3)
    print(len(expected_answer_3))
    # end debug
    if same_multi_line_strings(answer,expected_answer_3):
        print('Test taboo_cells passed\n')
    else:
        print('** Test taboo_cells failed\n')
        
#    assert( answer.strip() == expected_answer_3.strip() )


def test_check_elem_action_seq():
    problem_file = "./warehouses/warehouse_01.txt"
    wh = Warehouse()
    wh.read_warehouse_file(problem_file)
    print('Initial state \n', wh ,'\n')
    answer = check_action_seq(wh, ['Right', 'Right','Down'])
    
    if same_multi_line_strings(answer,expected_answer_1):
        print('Test check_elem_action_seq passed\n')
    else:
        print('** Test check_elem_action_seq failed\n')
        

def test_solve_sokoban_elem():
#    problem_file = "./warehouses/warehouse_01.txt"
    wh = Warehouse()
#    wh.read_warehouse_file(problem_file)
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    print(wh)
    print('\nElementary solution')
    answer = solve_sokoban_elem(wh)
    print(answer)
    if  answer ==  ['Right', 'Right']:
        print('Test solve_sokoban_elem passed\n')
    else:
        print('** Test solve_sokoban_elem failed\n')
        

def test_can_go_there():
    problem_file = "./warehouses/warehouse_01.txt"
    wh = Warehouse()
    wh.read_warehouse_file(problem_file)
    print(wh)
    answer = can_go_there(wh,(30,2))
    assert( answer ==  False)
    answer = can_go_there(wh,(6,2))
    assert( answer ==  True)
    
  
def test_solve_sokoban_macro():
    wh = Warehouse()
    wh.extract_locations(puzzle_t3.split(sep='\n'))
    print(wh)
    answer = solve_sokoban_macro(wh)
    print(answer)
#    assert( answer ==  [ ((2,3),'Right'), ((2,4),'Right'), ((3,3),'Left') , ((3,2),'Left') ] )
#    print(wh.worker) # x,y  coords !!
#    print(wh.boxes)  # x,y  coords !!

def test_check_macro_action_seq():
    wh = Warehouse()
    wh.extract_locations(puzzle_t1.split(sep='\n'))
    print(wh)
    answer = solve_sokoban_macro(wh.copy())
    print(answer)

    print("\ntesting [((2, 3), 'Right')]")
    print( check_macro_action_seq(wh.copy(),[((2, 3), 'Right')]) )
    print("\ntesting [((2, 3), 'Left')]")
    print( check_macro_action_seq(wh.copy(), [((2, 3), 'Left')]) )
    

if __name__ == "__main__":
    pass    
#    test_warehouse_1() # test Warehouse
#    test_warehouse_2() # test Warehouse
    
#    print(my_team())  # should print your team

    test_taboo_cells() 
#    test_check_elem_action_seq()
#    test_solve_sokoban_elem()
#    test_can_go_there()
#    test_solve_sokoban_macro()   
#    test_check_macro_action_seq()
