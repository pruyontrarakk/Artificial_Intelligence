from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])


    def __lt__(self, other):
        return calculate_total_cost(self) <= calculate_total_cost(other)

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """

        if self.blank_index > 2:
            new_config = list(swap_position(self.config, self.blank_index, self.blank_index - 3))
            return PuzzleState(new_config, self.n, self, 'Up', self.cost + 1)

        return None

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """

        if self.blank_index < 6:
            new_config = list(swap_position(self.config, self.blank_index, self.blank_index + 3))
            return PuzzleState(new_config, self.n, self, 'Down', self.cost+1)

        return None

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """

        if self.blank_index % 3 != 0:
            new_config = list(swap_position(self.config, self.blank_index, self.blank_index - 1))
            return PuzzleState(new_config, self.n, self, 'Left', self.cost+1)

        return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """

        if self.blank_index % 3 != 2:
            new_config = list(swap_position(self.config, self.blank_index, self.blank_index + 1))
            return PuzzleState(new_config, self.n, self, "Right", self.cost+1)

        return None


    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path, cost, nodesExpanded, searchDepth, maxSearchDepth, totalTime, ramUsage):

    line = [
        "path_to_goal: {}".format(path),
        "cost_of_path: {}".format(cost),
        "nodes_expanded: {}".format(nodesExpanded),
        "search_depth: {}".format(searchDepth),
        "max_search_depth: {}".format(maxSearchDepth),
        "running_time: {}".format(round(totalTime, 8)),
        "running_time: {}".format(round(ramUsage, 8)),
    ]

    with open("output.txt", "w") as f:
        f.write("\n".join(line))
        f.close()

    print("path to goal", path)
    print("cost of path", cost)
    print("nodes expanded", nodesExpanded)
    print("search depth", searchDepth)
    print("max search depth", maxSearchDepth)
    print("running time", round(totalTime, 8))
    print("ram usage", round(ramUsage, 8))

    return


def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###

    start = time.time()
    startRam = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = [initial_state] #queue
    explored = set()
    nodesExpanded = 0
    depthCounter = 0
    path = []

    while frontier:
        state = frontier.pop(0)
        explored.add(tuple(state.config))

        if test_goal(state.config):
            cost = state.cost

            while state.action != "Initial":
                path.append(state.action)
                state = state.parent
            path.reverse()
            searchDepth = len(path)
            ramUsage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - startRam)/(2**20)
            writeOutput(path, cost, nodesExpanded, searchDepth, depthCounter, time.time() - start, ramUsage)
            return True

        nodesExpanded = nodesExpanded + 1

        for child in state.expand():
            child_config_tuple = tuple(child.config)
            if child_config_tuple not in explored:
                frontier.append(child)
                explored.add(child_config_tuple)
                depthCounter = max(depthCounter, child.cost)
    return False

def swap_position(list1, pos1, pos2):
    tempList = list1.copy()
    temp = tempList[pos2]
    tempList[pos2] = tempList[pos1]
    tempList[pos1] = temp
    return tempList

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###

    start = time.time()
    startRam = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = [initial_state]  # stack
    explored = set()
    nodesExpanded = 0
    depthCounter = 0
    path = []

    while frontier:
        state = frontier.pop()
        explored.add(tuple(state.config))

        if test_goal(state.config):
            cost = state.cost

            while state.action != "Initial":
                path.append(state.action)
                state = state.parent
            path.reverse()
            searchDepth = len(path)
            ramUsage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - startRam) / (2 ** 20)
            writeOutput(path, cost, nodesExpanded, searchDepth, depthCounter, time.time() - start, ramUsage)
            return True

        nodesExpanded = nodesExpanded + 1

        for child in state.expand()[::-1]:
            child_config_tuple = tuple(child.config)
            if child_config_tuple not in explored:
                frontier.append(child)
                explored.add(child_config_tuple)
                depthCounter = max(depthCounter, child.cost)

    return False


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###

    start = time.time()
    startRam = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    frontier = Q.PriorityQueue()
    frontier.put(initial_state)
    explored = set()
    nodesExpanded = 0
    depthCounter = 0
    path = []

    while not frontier.empty():
        state = frontier.get()
        explored.add(tuple(state.config))

        if test_goal(state.config):
            cost = state.cost

            while state.action != "Initial":
                path.append(state.action)
                state = state.parent
            path.reverse()
            searchDepth = len(path)
            ramUsage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - startRam) / (2 ** 20)
            writeOutput(path, cost, nodesExpanded, searchDepth, depthCounter, time.time() - start, ramUsage)
            return True

        nodesExpanded = nodesExpanded + 1

        for child in state.expand():
            child_config_tuple = tuple(child.config)
            if (child_config_tuple not in explored) and (not inFrontierQueue(frontier, child)):
                frontier.put(child)
                explored.add(child_config_tuple)
                depthCounter = max(depthCounter, child.cost)

    return False

def inFrontierQueue(frontier, child):
    for state in frontier.queue:
        if state.config == child.config:
            return True
    return False


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###

    totalCost = state.cost
    for i in range(9):
        totalCost = totalCost + calculate_manhattan_dist(i, state.config[i], state.n)
    return totalCost



def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###

    if (value == 0):
        return 0

    x = idx // n
    y = idx % n
    x_goal = value // n
    y_goal = value % n

    return abs(x - x_goal) + abs(y - y_goal)



def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    return (puzzle_state == goal)


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == '__main__':
    main()
