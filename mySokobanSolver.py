"""
The partially defined functions and classes of this module
will be called by a marker script.

You should complete the functions and classes according to their specified
interfaces.
"""
from math import sqrt

import search
from search import astar_graph_search as astar_graph

import sokoban
from sokoban import find_2D_iterator


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def my_team():
    """
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    """
    return [(8884731, 'Astrid', 'Jonelynas'),
            (8847436, 'Lindsay', 'Watt'),
            (9342401, 'Madeline', 'Miller')]


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def taboo_cells(warehouse):
    '''
    Identify the taboo cells of a warehouse. A cell is called taboo if whenever
    a box get pushed on such a cell then the puzzle becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target  cells.
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none
        of these cells is a target.

    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with
       an '#' and the taboo cells marked with an 'X'.
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.
    '''

    # some constants
    squares_to_remove = ['$', '@']
    target_squares = ['.', '!', '*']
    wall_square = '#'
    taboo_square = 'X'

    def is_corner_cell(warehouse, x, y, wall = 0):
        '''
        cell is in a corner if there is at least 1 wall above/below
        and at least one wall left/right...
        '''
        num_ud_walls = 0
        num_lr_walls = 0
        # check for walls above and below
        for (dx, dy) in [(0, 1), (0, -1)]:
            if warehouse[y + dy][x + dx] == wall_square:
                num_ud_walls += 1
        # check for walls left and right
        for (dx, dy) in [(1, 0), (-1, 0)]:
            if warehouse[y + dy][x + dx] == wall_square:
                num_lr_walls += 1
        if wall:
            return ((num_ud_walls >= 1) or (num_lr_walls >= 1))
        else:
            return ((num_ud_walls >= 1) and (num_lr_walls >= 1))

    # get string representation
    warehouse = str(warehouse)

    # remove the things that aren't walls or targets
    for char in squares_to_remove:
        warehouse = warehouse.replace(char, ' ')

    # convert warehouse string into 2D array
    warehouse = [list(line) for line in warehouse.split('\n')]

    # apply rule 1
    for y in range(1, len(warehouse)-1):
        inside = False
        for x in range(1, len(warehouse[0])-1):
            # move through row in warehouse until we hit first wall
            # means we are now inside the warehouse
            if not inside:
                if warehouse[y][x] == wall_square:
                    inside = True
            else:
                # check if all the cells to the right of current cell are empty
                # means we are now outside the warehouse
                if all([cell == ' ' for cell in warehouse[y][x:]]):
                    break
                if warehouse[y][x] not in target_squares:
                    if warehouse[y][x] != wall_square:
                        if is_corner_cell(warehouse, x, y):
                            warehouse[y][x] = taboo_square

    # apply rule 2
    for y in range(1, len(warehouse)-1):
        for x in range(1, len(warehouse[0])-1):
            if warehouse[y][x] == taboo_square and is_corner_cell(warehouse, x, y):
                row = warehouse[y][x+1:]
                col = [row[x] for row in warehouse[y+1:][:]]
                for x2 in range(len(row)):
                    if row[x2] in target_squares or row[x2] == wall_square:
                        break
                    if row[x2] == taboo_square and is_corner_cell(warehouse, x2+x+1, y):
                        if all([is_corner_cell(warehouse, x3, y, 1) for x3 in range(x+1, x2+x+1)]):
                            for x4 in range(x+1, x2+x+1):
                                warehouse[y][x4] = 'X'
                for y2 in range(len(col)):
                    if col[y2] in target_squares or col[y2] == wall_square:
                        break
                    if col[y2] == taboo_square and is_corner_cell(warehouse, x, y2+y+1):
                        if all([is_corner_cell(warehouse, x, y3, 1) for y3 in range(x+1, y2+y+1)]):
                            for y4 in range(y+1, y2+y+1):
                                warehouse[y4][x] = 'X'

    # convert 2D array back into string
    warehouse = '\n'.join([''.join(line) for line in warehouse])

    # remove the remaining target_squares
    for char in target_squares:
        warehouse = warehouse.replace(char, ' ')
    return str(warehouse)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    """
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.

    Use the sliding puzzle and the pancake puzzle for inspiration!
    """

    def __init__(self, warehouse, initial):
        self.initial = initial
        self.warehouse = warehouse
        # TODO Find goal.

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']
        """
        bad_cells = list(find_2D_iterator(taboo_cells(self.warehouse), "X"))
        for offset in offset_states:
            new_state = (state[0] + offset[0], state[1] + offset[1])
            beyond_state = (new_state[0] + offset[0], new_state[1] + offset[1])
            flipped_state = (new_state[1], new_state[0])
            flipped_beyond_state = (beyond_state[1], beyond_state[0])
            if flipped_state not in self.warehouse.walls:
                if flipped_state in self.warehouse.boxes:
                    if flipped_beyond_state in bad_cells:
                        continue
                if offset == (0, 1):
                    yield "Down"
                elif offset == (0, -1):
                    yield "Up"
                elif offset == (1, 0):
                    yield "Right"
                elif offset == (-1, 0):
                    yield "Left"
                else:
                    raise ValueError("Unknown offset state")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def check_action_seq(warehouse, action_seq):
    """

    Determine if the sequence of actions listed in 'action_seq' is legal or not

    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.

    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']

    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    """
    # call warehouse.worker for worker location
    x, y = warehouse.worker
    # failedSequence return string
    failedSequence = 'Failure'

    # iterate through each move in the action_seq checking if valid
    for data in action_seq:
        if data == 'Left':
            print('left')
            # next location for left
            next_x = x - 1
            next_y = y
            # see if able to move the player in this direction
            if (next_x, next_y) in warehouse.walls:
                return failedSequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                assert (x, y) in warehouse.boxes
                if (next_x, next_y) not in warehouse.walls and (next_x, next_y) not in warehouse.boxes:
                    # can move the box!
                    # move successful
                    print('can move the box')
                else:
                    return failedSequence  # box was blocked
            else:
                x = next_x
        elif data == 'Right':
            print('right')
            next_x = x + 1
            next_y = y
            if (next_x, next_y) in warehouse.walls:
                return failedSequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                assert (x, y) in warehouse.boxes
                if (next_x, next_y) not in warehouse.walls and (next_x, next_y) not in warehouse.boxes:
                    # can move the box!
                    # move successful
                    print('can move the box')
                else:
                    return failedSequence  # box was blocked
            else:
                x = next_x
        elif data == 'Up':
            print('up')
            next_y = y - 1
            next_x = x
            if (next_x, next_y) in warehouse.walls:
                return failedSequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                assert (x, y) in warehouse.boxes
                if (next_x, next_y) not in warehouse.walls and (next_x, next_y) not in warehouse.boxes:
                    # can move the box!
                    # move successful
                    print('can move the box')
                else:
                    return failedSequence  # box was blocked
            else:
                y = next_y
        elif data == 'Down':
            print('down')
            next_y = y + 1
            next_x = x
            if (next_x, next_y) in warehouse.walls:
                return failedSequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                assert (x, y) in warehouse.boxes
                if (next_x, next_y) not in warehouse.walls and (next_x, next_y) not in warehouse.boxes:
                    # can move the box!
                    # move successful
                    print('can move the box')
                else:
                    return failedSequence  # box was blocked
            else:
                y = next_y
        else:
            raise ValueError("No action sequence")
            return failedSequence

    applicableSequence = 'Yes'
    print (applicableSequence)
    return str(applicableSequence)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_sokoban_elem(warehouse):
    """
    This function should solve using elementary actions
    the puzzle defined in a file.

    @param warehouse: a valid Warehouse object

    @return
        A list of strings.
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that
        solves the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    """

    # "INSERT YOUR CODE HERE"

    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


offset_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def can_go_there(warehouse, dst):
    """
    Determine whether the worker can walk to the cell dst=(row,col)
    without pushing any box.

    @param warehouse: a valid Warehouse object
    @param dst: The destination tuple in (row,col)

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    """

    def heuristic(n):
        state = n.state
        # distance = sqrt(xdiff^2 + ydiff^2). sqrt not required as we only
        # care about order, and it's slow
        return ((state[1] - dst[1]) ** 2) + ((state[0] - dst[0]) ** 2)

    class FindPathProblem(search.Problem):

        def value(self, state):
            return heuristic(state)

        def result(self, state, action):
            new_state = (state[0] + action[0], state[1] + action[1])
            return new_state

        def actions(self, state):
            for offset in offset_states:
                new_state = (state[0] + offset[0], state[1] + offset[1])
                flipped_state = (new_state[1], new_state[0])
                if flipped_state not in warehouse.boxes \
                        and flipped_state not in warehouse.walls:
                    yield offset

    node = astar_graph(FindPathProblem(warehouse.worker, dst), heuristic)

    return node is not None


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def solve_sokoban_macro(warehouse):
    """
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ]
    means that the worker first goes the box at row 3 and column 4 and pushes
    it left, then goes the box at row 5 and column 2 and pushes it up, and
    finally goes the box at row 12 and column 4 and pushes it down.

    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return ['Impossible']
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    """

    # "INSERT YOUR CODE HERE"

    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
