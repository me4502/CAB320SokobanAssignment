from __future__ import print_function
from __future__ import division

import time
from sokoban import Warehouse
from mySokobanSolver import solve_sokoban_elem

START_WAREHOUSE = 21
END_WAREHOUSE = 50
TESTS_PER_WAREHOUSE = 5
DATA_FILENAME = "timing_data.csv"

def test_warehouse(warehouse_number):
    average_time = 0
    result = None
    for i in range(TESTS_PER_WAREHOUSE):
        problem_file = "./warehouses/warehouse_{:02d}.txt".format(warehouse_number)
        wh = Warehouse()
        wh.read_warehouse_file(problem_file)
        start_time = time.process_time()
        result = solve_sokoban_elem(wh)
        average_time += (time.process_time() - start_time) / TESTS_PER_WAREHOUSE
        print("{}%".format((i+1) * 100 / TESTS_PER_WAREHOUSE))

    with open(DATA_FILENAME, 'a') as file:
        file.write("{:02d},{},{}\n".format(warehouse_number, average_time, result))

if __name__ == "__main__":
    with open(DATA_FILENAME, 'w') as file:
        file.write("warehouse_number,elapsed_time,result\n")

    # test_warehouse(33)
    for n in range(START_WAREHOUSE, END_WAREHOUSE, 2):
        print("Testing warehouse {:02d}".format(n))
        test_warehouse(n)
