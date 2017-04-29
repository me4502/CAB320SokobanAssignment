"""
The partially defined functions and classes of this module
will be called by a marker script.

You should complete the functions and classes according to their specified
interfaces.
"""
import search
import sokoban
from search import astar_graph_search as astar_graph
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


def offset_to_direction(offset):
    if offset == (0, 1):
        return "Down"
    elif offset == (0, -1):
        return "Up"
    elif offset == (1, 0):
        return "Right"
    elif offset == (-1, 0):
        return "Left"
    else:
        raise ValueError("Unknown offset state")


def direction_to_offset(direction):
    if direction == "Down":
        return 0, 1
    elif direction == "Up":
        return 0, -1
    elif direction == "Right":
        return 1, 0
    elif direction == "Left":
        return -1, 0
    else:
        raise ValueError("Unknown direction")


def find_worker_goal(box, push_direction):
    """
    Find the goal coordinates for worker given a box and a push direction
    """
    offset = (0, 0)
    if push_direction == "Left":
        offset = (1, 0)
    elif push_direction == "Right":
        offset = (-1, 0)
    elif push_direction == "Up":
        offset = (0, 1)
    elif push_direction == "Down":
        offset = (0, -1)
    return add_tuples(box, offset)


def add_tuples(tuple1, tuple2):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[0] - b[0])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    """
    Identify the taboo cells of a warehouse. A cell is called taboo if whenever
    a box get pushed on such a cell then the puzzle becomes unsolvable.
    When determining the taboo cells, you must ignore all the existing boxes,
    simply consider the walls and the target cells.
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
    """

    # some constants
    squares_to_remove = ['$', '@']
    target_squares = ['.', '!', '*']
    wall_square = '#'
    taboo_square = 'X'

    def is_corner_cell(warehouse, x, y, wall=0):
        """
        cell is in a corner if there is at least 1 wall above/below
        and at least one wall left/right...
        """
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
            return (num_ud_walls >= 1) or (num_lr_walls >= 1)
        else:
            return (num_ud_walls >= 1) and (num_lr_walls >= 1)

    # get string representation
    warehouse_str = str(warehouse)

    # remove the things that aren't walls or targets
    for char in squares_to_remove:
        warehouse_str = warehouse_str.replace(char, ' ')

    # convert warehouse string into 2D array
    warehouse_2d = [list(line) for line in warehouse_str.split('\n')]

    # apply rule 1
    for y in range(len(warehouse_2d) - 1):
        inside = False
        for x in range(len(warehouse_2d[0]) - 1):
            # move through row in warehouse until we hit first wall
            # means we are now inside the warehouse
            if not inside:
                if warehouse_2d[y][x] == wall_square:
                    inside = True
            else:
                # check if all the cells to the right of current cell are empty
                # means we are now outside the warehouse
                if all([cell == ' ' for cell in warehouse_2d[y][x:]]):
                    break
                if warehouse_2d[y][x] not in target_squares:
                    if warehouse_2d[y][x] != wall_square:
                        if is_corner_cell(warehouse_2d, x, y):
                            warehouse_2d[y][x] = taboo_square

    # apply rule 2
    for y in range(1, len(warehouse_2d) - 1):
        for x in range(1, len(warehouse_2d[0]) - 1):
            if warehouse_2d[y][x] == taboo_square \
                    and is_corner_cell(warehouse_2d, x, y):
                row = warehouse_2d[y][x + 1:]
                col = [row[x] for row in warehouse_2d[y + 1:][:]]
                # fill in taboo_cells in row to the right of corner taboo cell
                for x2 in range(len(row)):
                    if row[x2] in target_squares or row[x2] == wall_square:
                        break
                    if row[x2] == taboo_square \
                            and is_corner_cell(warehouse_2d, x2 + x + 1, y):
                        if all([is_corner_cell(warehouse_2d, x3, y, 1)
                                for x3 in range(x + 1, x2 + x + 1)]):
                            for x4 in range(x + 1, x2 + x + 1):
                                warehouse_2d[y][x4] = 'X'
                # fill in taboo_cells in column moving down from corner taboo
                # cell
                for y2 in range(len(col)):
                    if col[y2] in target_squares or col[y2] == wall_square:
                        break
                    if col[y2] == taboo_square \
                            and is_corner_cell(warehouse_2d, x, y2 + y + 1):
                        if all([is_corner_cell(warehouse_2d, x, y3, 1)
                                for y3 in range(y + 1, y2 + y + 1)]):
                            for y4 in range(y + 1, y2 + y + 1):
                                warehouse_2d[y4][x] = 'X'

    # convert 2D array back into string
    warehouse_str = '\n'.join([''.join(line) for line in warehouse_2d])

    # remove the remaining target_squares
    for char in target_squares:
        warehouse_str = warehouse_str.replace(char, ' ')
    return warehouse_str

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def iterative_deepening_astar(problem, main_limit=100, h=None):
    h = search.memoize(h or problem.h)
    heuristic = lambda n: n.path_cost + h(n)

    initial = search.Node(problem.initial)
    bound = heuristic(initial)

    # Algorithm based off psuedocode from
    # https://en.wikipedia.org/wiki/Iterative_deepening_A*#Pseudocode
    def recursive_search(node, current_cost, limit):
        if current_cost + heuristic(node) > limit:
            return current_cost + heuristic(node)
        if problem.goal_test(node.state):
            return node
        value = main_limit  # Large value at the start.
        for child in node.expand(problem):
            result = recursive_search(child,
                                      current_cost + 1,
                                      limit)
            if type(result) is search.Node:
                return result
            elif type(result) is int and result < value:
                value = result
        return value

    while True:
        result = recursive_search(initial, 0, bound)
        if type(result) is search.Node:
            return result
        elif type(result) is int:
            if result == main_limit:
                return None
            bound = result


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
        global bad_cells
        if bad_cells is None:
            bad_cells = set(find_2D_iterator(taboo_cells(self.warehouse)
                                             .split("\n"), "X"))

        for offset in offset_states:
            new_state = add_tuples(state, offset)
            beyond_state = add_tuples(new_state, offset)
            if new_state not in self.warehouse.walls:
                if new_state in self.warehouse.boxes:
                    if beyond_state in bad_cells:
                        continue
                    yield offset_to_direction(offset)


class MacroSokobanPuzzle(search.Problem):
    """
    Class to represent a Sokoban puzzle.
    This solves at a larger scale, by finding a list of macro moves.
    """

    def __init__(self, initial, goal):
        self.initial = (((-1, -1), "None"), initial)
        self.goal = goal.replace("@", " ")

    def actions(self, state):
        current_warehouse = sokoban.Warehouse()
        current_warehouse.extract_locations(state[1].split(sep="\n"))
        global bad_cells

        if bad_cells is None:
            bad_cells = set(find_2D_iterator(taboo_cells(current_warehouse)
                                             .split("\n"), "X"))

        for box in current_warehouse.boxes:
            for offset in offset_states:
                player_position = (box[0] + (offset[0] * -1),
                                   box[1] + (offset[1] * -1))
                new_box_position = add_tuples(box, offset)
                if can_go_there(current_warehouse, player_position) \
                        and new_box_position not in bad_cells \
                        and new_box_position not in current_warehouse.walls \
                        and new_box_position not in current_warehouse.boxes:
                    yield (box, offset_to_direction(offset))

    def result(self, state, action):
        current_warehouse = sokoban.Warehouse()
        current_warehouse.extract_locations(state[1].split(sep="\n"))
        box = action[0]
        if box in current_warehouse.boxes:
            offset = direction_to_offset(action[1])
            current_warehouse.worker = box
            current_warehouse.boxes.remove(box)
            current_warehouse.boxes.append(add_tuples(box, offset))
            return action, str(current_warehouse)
        else:
            print(str(current_warehouse))
            print(box)
            print(current_warehouse.boxes)
            raise ValueError("Box not in warehouse!")

    def goal_test(self, state):
        return state[1].replace("@", " ") == self.goal

    def value(self, state):
        return 1

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
    # call warehouse.worker and warehouse.boxes for locations
    x, y = warehouse.worker

    # failedSequence return string
    failed_sequence = 'Failure'

    # iterate through each move in the action_seq checking if valid
    for data in action_seq:
        if data == 'Left':
            print('left')
            # next location for left
            next_x = x - 1
            next_y = y
            # see if able to move the player in this direction
            if (next_x, next_y) in warehouse.walls:
                return failed_sequence  # impossible move, player was blocked
            elif (next_x, next_y) in warehouse.boxes:
                if (next_x - 1, next_y) not in warehouse.walls and (next_x, next_y) in warehouse.boxes:
                    # can move the box!
                    # move successful
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x - 1, next_y))
                    x = next_x
                else:
                    return failed_sequence  # box was blocked
            else:
                x = next_x
        elif data == 'Right':
            print('right')
            next_x = x + 1
            next_y = y
            if (next_x, next_y) in warehouse.walls:
                return failed_sequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                if (next_x + 1, next_y) not in warehouse.walls \
                        and (next_x, next_y) in warehouse.boxes:
                    # can move the box!
                    # move successful
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x + 1, next_y))
                    x = next_x
                else:
                    return failed_sequence  # box was blocked
            else:
                x = next_x
        elif data == 'Up':
            print('up')
            next_y = y - 1
            next_x = x
            if (next_x, next_y) in warehouse.walls:
                return failed_sequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                if (next_x, next_y - 1) not in warehouse.walls \
                        and (next_x, next_y) in warehouse.boxes:
                    # can move the box!
                    # move successful
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x, next_y - 1))
                    y = next_y
                else:
                    return failed_sequence  # box was blocked
            else:
                y = next_y
        elif data == 'Down':
            print('down')
            next_y = y + 1
            next_x = x
            if (next_x, next_y) in warehouse.walls:
                return failed_sequence  # impossible move
            elif (next_x, next_y) in warehouse.boxes:
                if (next_x, next_y + 1) not in warehouse.walls \
                        and (next_x, next_y) in warehouse.boxes:
                    # can move the box!
                    # move successful
                    warehouse.boxes.remove((next_x, next_y))
                    warehouse.boxes.append((next_x, next_y + 1))
                    y = next_y
                else:
                    return failed_sequence  # box was blocked
            else:
                y = next_y
        else:
            raise ValueError("No action sequence")

    # print statement just to check it got to the end and actions are valid
    applicable_sequence = 'Yes'
    print(applicable_sequence)

    # implement change character information for updating
    warehouse.worker = x, y
    '''
    The following code has been adapted from the provided
    Sokoban.py Warehouse.__str__ method
    '''
    X, Y = zip(*warehouse.walls)  # pythonic version of the above
    x_size, y_size = 1 + max(X), 1 + max(Y)

    vis = [[" "] * x_size for z in range(y_size)]
    for (x, y) in warehouse.walls:
        vis[y][x] = "#"
    for (x, y) in warehouse.targets:
        vis[y][x] = "."
    # Note y is worker[1], x is worker[0]
    if vis[warehouse.worker[1]][warehouse.worker[0]] == ".":
        vis[warehouse.worker[1]][warehouse.worker[0]] = "!"
    else:
        vis[warehouse.worker[1]][warehouse.worker[0]] = "@"
    # if a box is on a target display a "*"
    # exploit the fact that Targets has been already processed
    for (x, y) in warehouse.boxes:
        if vis[y][x] == ".":  # if on target
            vis[y][x] = "*"
        else:
            vis[y][x] = "$"
    warehouse = "\n".join(["".join(line) for line in vis])
    '''
    End adapted code from Sokoban.py Warehouse.__str__ method
    '''
    print(str(warehouse))
    return str(warehouse)


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

    macro_actions = solve_sokoban_macro(warehouse)

    # check if already solved
    if len(macro_actions) == 0:
        return macro_actions

    # check if impossible
    if macro_actions == ['Impossible']:
        return macro_actions

    worker_path = []

    for macro_action in macro_actions[1:]:
        target_box = macro_action[0]
        push_direction = macro_action[1]
        worker_goal = find_worker_goal(target_box, push_direction)

        def heuristic(n):
            state = n.state
            return ((state[1] - worker_goal[1]) ** 2) + ((state[0] - worker_goal[0]) ** 2)

        class FindPathProblem(search.Problem):

            def value(self, state):
                return heuristic(state)

            def result(self, state, action):
                new_state = add_tuples(state, action)
                return new_state

            def actions(self, state):
                for offset in offset_states:
                    new_state = add_tuples(state, offset)
                    if new_state not in warehouse.boxes and new_state not in warehouse.walls:
                        yield offset

        nodes = astar_graph(FindPathProblem(warehouse.worker, worker_goal), heuristic)

        if nodes is None:
            return ['Impossible']

        # build list of actions to get worker next to target box
        for node in nodes.path()[1:]:
            worker_path.append(offset_to_direction(node.action))

        # add the actual push action
        worker_path.append(push_direction)

        # move target box to new position
        warehouse.boxes.remove(target_box)
        warehouse.boxes.append(add_tuples(target_box, direction_to_offset(push_direction)))

        # move worker to new position
        warehouse.worker = target_box

    return worker_path


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


offset_states = [(-1, 0), (1, 0), (0, -1), (0, 1)]
bad_cells = None


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
            new_state = add_tuples(state, action)
            return new_state

        def actions(self, state):
            for offset in offset_states:
                new_state = add_tuples(state, offset)
                if new_state not in warehouse.boxes \
                        and new_state not in warehouse.walls:
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

    # specify the goal
    goal = str(warehouse).replace("$", " ").replace(".", "*")

    # specify heuristic
    def h(n):
        state = n.state[1]
        wh = sokoban.Warehouse()
        wh.extract_locations(state.split('\n'))
        num_targets = len(wh.targets)
        heuristic = 0
        for box in wh.boxes:
            dist = 0
            for target in wh.targets:
                dist += manhattan_distance(box, target)
            heuristic += (dist / num_targets)
        print('h: ', heuristic)
        return heuristic

    # execute iterative_deepening_astar to solve the puzzle
    M = iterative_deepening_astar(MacroSokobanPuzzle(str(warehouse), goal), 35, h)
    # take the returned action and it's paths to get there
    macro_actions = M.path()
    # extract the action data from the node data
    macro_actions = [e.action for e in macro_actions]

    # extract the state data from the node data
    state_check = M.path()
    state_check = [b.state for b in state_check]
    # if no box is in the original state of the puzzle, it is in a goal state
    if '$' not in str(state_check[0]):
        # puzzle is in goal state, return []
        return []
    # when the puzzle cannot be solved MacroSokobanPuzzle.action returns 'None'
    elif M.action == 'None':
        # return ['Impossible']
        return ['Impossible']
    else:
        # return sequence of macro actions, M
        return macro_actions

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
