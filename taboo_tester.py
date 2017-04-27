from __future__ import print_function
from __future__ import division


from sokoban import Warehouse, find_2D_iterator
from mySokobanSolver import taboo_cells

def test_taboo_cells(n):
    problem_file = "./warehouses/warehouse_%s.txt" % str(n)
    wh = Warehouse()
    wh.read_warehouse_file(problem_file)
    answer = taboo_cells(wh)
    print(set(find_2D_iterator(answer.split('\n'), "X")))
    print(answer)

if __name__ == "__main__":
    print("enter 'quit' to exit\n")
    c = input('Warehouse number: ')
    while c != 'quit':
        try:
            test_taboo_cells(c)
        except FileNotFoundError as e:
            print("Warehouse %s does not exist\n" % str(c))
        c = input('Warehouse number: ')
