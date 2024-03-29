'''
COMP3702 - assignment one
Search algorithm for the game Sokoban
'''
import copy
import sys
import time
import numpy as np


class SokobanMap:
    """
   Creates an instance of the sokoban map
    """

    # input file symbols
    BOX_SYMBOL = 'B'
    TGT_SYMBOL = 'T'
    PLAYER_SYMBOL = 'P'
    OBSTACLE_SYMBOL = '#'
    FREE_SPACE_SYMBOL = ' '
    BOX_ON_TGT_SYMBOL = 'b'
    PLAYER_ON_TGT_SYMBOL = 'p'

    # move symbols (i.e. output file symbols)
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'

    # render characters
    FREE_GLYPH = '   '
    OBST_GLYPH = 'XXX'
    BOX_GLYPH = '[B]'
    TGT_GLYPH = '(T)'
    PLAYER_GLYPH = '<P>'

    def __init__(self, row_len=None, num_rows=None, box_positions=None, tgt_positions=None, player_position=None,
                 rows=None, depth=0, action=None, parent=None, heuristic=None):
        """
        Build a Sokoban map instance from the given file name
        :param state, row_len=None, num_rows=None, box_positions=None, tgt_positions=None, player_position=None,
                 rows=None, depth=0, action=None, parent=None:
        """

        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows
        self.state = (player_position, tuple(box_positions), tuple(tgt_positions))
        self.parent = parent  # parent node, a NODE! not just a matrix.
        self.action = action  # The one that led to this node (useful for retracing purpose)
        self.depth = depth
        self.heuristic = heuristic

    def manhattan_distance(self, state, depth):
        """

        :param depth:
        :param state: Takes in the state of the Sokoban map including box and target positions
        :return: Returns the heuristic h(n). It is an admissible heuristic
        """
        # i = 0
        j = 0
        k = 0

        box_positions = list(state[1])
        tgt_positions = list(state[2])
        player_positions = list(state[0])
        player_x = player_positions[1]
        player_y = player_positions[0]

        #  heuristic1 = 999
        h1 = 0
        h2 = 999
        for box in box_positions:
            goal2 = abs(player_x - box_positions[j][1]) + abs(player_y - box_positions[j][0])
            if h2 > goal2:
                h2 = goal2
            j += 1
        # Shortest distance between a box and target
        while box_positions:
            # iterate through all targets
            # print('tgts:', tgt_positions)
            # print('boxs', box_positions)
            k = 0
            heuristic1 = 999
            for box in box_positions:
                goal1 = abs(box_positions[k][1] - tgt_positions[0][1]) + abs(box_positions[k][0] - tgt_positions[0][0])
                if heuristic1 > goal1:
                    heuristic1 = goal1
                    del tgt_positions[0]
                    del box_positions[k]
                k += 1
            h1 += heuristic1
        # h = h/10
        # print('h', h)

        f = h1 + depth + h2 - 1
        # print('depth', depth)
        # print(f)
        return f

    def whos_next_astar(self, container):
        return np.argmin([anelement.heuristic for anelement in container])

    def render(self):
        """
        Render the map's current state to terminal
        """
        for r in range(self.y_size):
            line = ''
            for c in range(self.x_size):
                symbol = self.FREE_GLYPH
                if self.obstacle_map[r][c] == self.OBSTACLE_SYMBOL:
                    symbol = self.OBST_GLYPH
                if (r, c) in self.tgt_positions:
                    symbol = self.TGT_GLYPH
                # box or player overwrites tgt
                if (r, c) in self.box_positions:
                    symbol = self.BOX_GLYPH
                if self.player_x == c and self.player_y == r:
                    symbol = self.PLAYER_GLYPH
                line += symbol
            print(line)

        print('\n\n')

    def apply_move(self, move):
        """
        Apply a player move to the map.
        :param move: 'L', 'R', 'U' or 'D'
        :return: True if move was successful, false if move could not be completed
        """
        # basic obstacle check
        new_box_positions = copy.deepcopy(self.box_positions)
        if move == self.LEFT:
            if self.obstacle_map[self.player_y][self.player_x - 1] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x - 1
                new_y = self.player_y

        elif move == self.RIGHT:
            if self.obstacle_map[self.player_y][self.player_x + 1] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x + 1
                new_y = self.player_y

        elif move == self.UP:
            if self.obstacle_map[self.player_y - 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x
                new_y = self.player_y - 1

        else:
            if self.obstacle_map[self.player_y + 1][self.player_x] == self.OBSTACLE_SYMBOL:
                return False
            else:
                new_x = self.player_x
                new_y = self.player_y + 1

        # pushed box collision check
        if (new_y, new_x) in self.box_positions:
            if move == self.LEFT:
                if self.obstacle_map[new_y][new_x - 1] == self.OBSTACLE_SYMBOL or (
                        new_y, new_x - 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x - 1
                    new_box_y = new_y

            elif move == self.RIGHT:
                if self.obstacle_map[new_y][new_x + 1] == self.OBSTACLE_SYMBOL or (
                        new_y, new_x + 1) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x + 1
                    new_box_y = new_y

            elif move == self.UP:
                if self.obstacle_map[new_y - 1][new_x] == self.OBSTACLE_SYMBOL or (
                        new_y - 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y - 1

            else:
                if self.obstacle_map[new_y + 1][new_x] == self.OBSTACLE_SYMBOL or (
                        new_y + 1, new_x) in self.box_positions:
                    return False
                else:
                    new_box_x = new_x
                    new_box_y = new_y + 1

            new_box_positions.remove((new_y, new_x))
            new_box_positions.append((new_box_y, new_box_x))

        new_player_position = [new_y, new_x]
        return [new_player_position, new_box_positions]

    def is_finished(self):
        """
        Check if the goal state has been achieved
        :return: True if goal state reached, False otherwise
        """
        finished = True
        for i in self.box_positions:
            if i not in self.tgt_positions:
                finished = False
        return finished

    def done(self, current_node):
        """ The purpose of this function  is: Trace back this node to the founding granpa.
        Print out the states through out
        """
        founding_father = current_node
        states = []  # the retraced states will be stored here.
        counter = 0
        limit = 50  # if the trace is longer than 50, don't print anything, it will be a mess.
        while founding_father:
            states.append(founding_father.action)
            founding_father = founding_father.parent
            counter += 1
            # Keep doing this until you reach the founding father that has a parent None (see default of init method)
        print('Number of steps to the goal = ', counter - 1)
        return states

    def get_successors(self):
        """
        Find the possible legal moves for a given state
        :return: list type of possible legal moves
        """
        successors = []
        possibilities = ['D', 'L', 'U', 'R']
        # Iterate over all possibilities and append legal moves to the successors list
        for apossibility in possibilities:
            try:
                new_positions = self.apply_move(apossibility)
                # print('new state: ', apossibility, new_state)
                if new_positions:
                    successors.append(apossibility)  # if apply_move didn't return False
                    # print(apossibility, 'true', self.state)
                else:
                    raise Exception
            except:
                # print(apossibility, 'false', self.state)
                pass  # move on to the next possibility
        return successors

    def astar(self):
        """
        Find the optimal solution to the Sokoban game using a uniform cost search
        :return: Return None if failed to solve the game, otherwise return a list of optimal moves to reach goal state
        """
        start = time.time()  # Start the timer
        container = [self]  # Initialise container to current node
        # print('container', container)
        visited = set([])  # List of visited states

        i = 0
        while len(container) > 0:
            # print()
            # time.sleep(0)
            # expand node
            self.heuristic = self.manhattan_distance(self.state, self.depth)  # Make sure heuristic is defined
            index = self.whos_next_astar(container)
            node = container[index]
            del container[index]
            # node = container.pop(0)  # FIFO container - Get the last branch
            # node.render() #Render to terminal
            # print('the node that was popped', node.state)
            # node = container.pop(-1) #LIFO container (DFS); Equivalent to container.pop()

            if node.is_finished():
                print('Time required = ', -start + time.time())
                print('Explored states = ', len(visited))
                print('Container max size = ', len(container))
                moves = node.done(node)
                print('The value of i: ', i - 1)
                return moves

            # add successors

            suc = node.get_successors()
            # print(suc)
            for s in suc:

                new_positions = node.apply_move(s)
                new_state = (tuple(new_positions[0]), tuple(new_positions[1]), tuple(self.tgt_positions))
                ns_heuristic = self.manhattan_distance(new_state, node.depth)
                # print('the new state', new_state)
                if new_state not in visited:
                    new_node = SokobanMap(player_position=tuple(new_positions[0]), box_positions=new_positions[1],
                                          tgt_positions=self.tgt_positions, rows=self.obstacle_map, parent=node,
                                          action=s, depth=node.depth + 1, num_rows=self.y_size, row_len=self.x_size,
                                          heuristic=ns_heuristic)

                    container.append(new_node)
                    visited.add(node.state)
                    # print('visited states', visited)
            i += 1

        return None


def print_to_file(filename, moves):
    """
    Opens file and writes moves to it
    :param filename: Text file
    :param moves: Moves found by search algorithm
    :return: None
    """
    f = open(filename, "w+")

    moves = moves[:-1]
    moves.reverse()

    # print(moves)
    length = len(moves)
    ct = 0
    for item in moves:
        # print(item)
        if item is None:
            pass
        elif ct != length - 1:
            item = item.lower()
            f.write("%s," % item)
        else:
            item = item.lower()
            f.write("%s" % item)
        ct += 1
    f.close()


def main(arglist):
    """
    Run a playable game of Sokoban using the given filename as the map file.
    :param arglist: map file name
    """

    f = open(arglist[0], 'r')

    rows = []
    for line in f:
        if len(line.strip()) > 0:
            rows.append(list(line.strip()))

    f.close()

    row_len = len(rows[0])
    for row in rows:
        assert len(row) == row_len, "Mismatch in row length"

    num_rows = len(rows)

    box_positions = []
    tgt_positions = []
    player_position = None
    for i in range(num_rows):
        for j in range(row_len):
            if rows[i][j] == SokobanMap.BOX_SYMBOL:
                box_positions.append((i, j))
                rows[i][j] = SokobanMap.FREE_SPACE_SYMBOL
            elif rows[i][j] == SokobanMap.TGT_SYMBOL:
                tgt_positions.append((i, j))
                rows[i][j] = SokobanMap.FREE_SPACE_SYMBOL
            elif rows[i][j] == SokobanMap.PLAYER_SYMBOL:
                player_position = (i, j)
                rows[i][j] = SokobanMap.FREE_SPACE_SYMBOL
            elif rows[i][j] == SokobanMap.BOX_ON_TGT_SYMBOL:
                box_positions.append((i, j))
                tgt_positions.append((i, j))
                rows[i][j] = SokobanMap.FREE_SPACE_SYMBOL
            elif rows[i][j] == SokobanMap.PLAYER_ON_TGT_SYMBOL:
                player_position = (i, j)
                tgt_positions.append((i, j))
                rows[i][j] = SokobanMap.FREE_SPACE_SYMBOL

    assert len(box_positions) == len(tgt_positions), "Number of boxes does not match number of targets"
    # Set our initial state
    initial_state = (player_position, tuple(box_positions), tuple(tgt_positions))
    # Set our initial map
    initial_map = SokobanMap(row_len, num_rows, box_positions, tgt_positions, player_position, rows,
                             depth=0, action=None, parent=None)

    try:
        import msvcrt
        getchar = msvcrt.getch
    except ImportError:
        getchar = sys.stdin.read(1)

    if len(arglist) != 2:
        print("Running this file directly launches a solution search for the input map, and outputs the solution to "
              "the output file if found")
        print("Usage: filename.py [map_file_name] [output_file]")
        return
    # Start the search here
    moves = initial_map.astar()
    print(moves)
    # Open output file and write list of moves to file
    print_to_file(arglist[1], moves)
    # initial_map.manhattan_distance()
    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
