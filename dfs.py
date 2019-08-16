import sys
import time


class SokobanMap:
    """
    Instance of a Sokoban game map. You may use this class and its functions
    directly or duplicate and modify it in your solution. You should avoid
    modifying this file directly.

    COMP3702 2019 Assignment 1 Support Code

    Last updated by njc 11/08/19
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

    def __init__(self, state, row_len=None, num_rows=None, box_positions=None, tgt_positions=None, player_position=None,
                 rows=None, depth=0, action=None, parent=None):
        """
        Build a Sokoban map instance from the given file name
        :param state, row_len=None, num_rows=None, box_positions=None, tgt_positions=None, player_position=None,
                 rows=None, depth=0, action=None, parent=None:
        """

        '''
        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows
        '''
        self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows
        self.state = tuple(state)
        self.parent = parent  # parent node, a NODE! not just a matrix.
        self.action = action  # The one that led to this node (useful for retracing purpose)
        self.depth = depth

    def apply_move(self, move):
        """
        Apply a player move to the map.
        :param move: 'L', 'R', 'U' or 'D'
        :return: True if move was successful, false if move could not be completed
        """
        # basic obstacle check
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

            # update box position
            self.box_positions.remove((new_y, new_x))
            self.box_positions.append((new_box_y, new_box_x))

        # update player position
        self.player_x = new_x
        self.player_y = new_y

        return True

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

    def is_finished(self):
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
            states.append(founding_father.state)
            founding_father = founding_father.parent
            counter += 1
            # Keep doing this until you reach the founding father that has a parent None (see default of init method)
        print('Number of steps to the goal = ', counter)
        if counter > limit:
            print('Too many steps to be printed')
        else:
            for i in reversed(states):  # Cause we want to print solution from initial to goal not the opposite.
                print(i, '\n')

    def explore_actions(self):
        possibilities = ['U', 'D', 'R', 'L']
        actions = []
        for apossibility in possibilities:
            try:
                self.apply_move(apossibility)
                actions.append(apossibility)  # if apply_move didn't return False
            except:
                pass  # move on to the next possibility
        return actions

    def dfs(self):  # This is actually a BFS
        start = time.time()

        frontier = [self]
        frontier_max_size = len(frontier)
        ft = set()
        ft.add(tuple(self.state))
        visited_nodes = set([])
        counter = 0
        print(frontier)
        while frontier:

            counter += 1
            print(counter, end='\r')

            if len(frontier) > frontier_max_size:
                frontier_max_size = len(frontier)
            current_node = frontier.pop(0)
            ft.remove(tuple(current_node.state))
            visited_nodes.add(tuple(current_node.state))

            if self.is_finished():
                print('Time required = ', -start + time.time())
                print('Explored states = ', len(visited_nodes))
                print('Frontier max size = ', frontier_max_size)
                current_node.done(current_node)

        actions = self.explore_actions()
        for anaction in actions:  # add exploration results to the frontier.
            self.apply_move(anaction)
            if tuple(self.state) not in visited_nodes:
                if tuple(self.state) not in ft:
                    new_state = (self.player_position, self.box_positions, self.tgt_positions)
                    new_node = SokobanMap(state=new_state, depth=current_node.depth + 1, parent=current_node,
                                          action=anaction)
                    frontier.append(new_node)
                    ft.add(tuple(new_state))

        print(self.state)
        print('Failed to reach the target goal! No. states explored: ', len(visited_nodes))
        return len(visited_nodes)


'''
                    new_node = Node(y_size=y, x_size=self.x_size, box_positions=self.box_positions, tgt_positions=None, player_position=None, obstacle_map=None, depth=None, action=None, parent=None):
                    frontier.append(new_node)
                    ft.add(player_position)
'''

'''
self.x_size = row_len
        self.y_size = num_rows
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = rows
'''

'''
class Node:
    def __init__(self, y_size=None, x_size=None, box_positions=None, tgt_positions=None, player_position=None, obstacle_map=None, depth=None, action=None, parent=None):
        self.y_size = y_size
        self.x_size = x_size
        self.action = action
        self.parent = parent
        self.depth = depth
        self.box_positions = box_positions
        self.tgt_positions = tgt_positions
        self.player_position = player_position
        self.player_x = player_position[1]
        self.player_y = player_position[0]
        self.obstacle_map = obstacle_map
'''


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
    initial_map = SokobanMap(initial_state, row_len, num_rows, box_positions, tgt_positions, player_position, rows,
                             depth=0, action=None, parent=None)

    try:
        import msvcrt
        getchar = msvcrt.getch
    except ImportError:
        getchar = sys.stdin.read(1)

    if len(arglist) != 1:
        print("Running this file directly launches a solution search for the input map, and outputs the solution to "
              "the output file if found")
        print("Usage: filename.py [map_file_name] [output_file]")
        return
    # Start the search here
    initial_map.dfs()
    return 0


'''
Not needed in this file (commented out)
    map_inst = SokobanMap(arglist[0])
    map_inst.render()

    steps = 0

    while True:
        char = getchar()

        if char == b'q':
            break

        if char == b'r':
            map_inst = SokobanMap(arglist[0])
            map_inst.render()

            steps = 0

        if char == b'\xe0':
            # got arrow - read direction
            dir = getchar()
            if dir == b'H':
                a = SokobanMap.UP
            elif dir == b'P':
                a = SokobanMap.DOWN
            elif dir == b'K':
                a = SokobanMap.LEFT
            elif dir == b'M':
                a = SokobanMap.RIGHT
            else:
                print("!!!error")
                a = SokobanMap.UP

            map_inst.apply_move(a)
            map_inst.render()

            steps += 1

            if map_inst.is_finished():
                print("Puzzle solved in " + str(steps) + " steps!")
                return
'''

if __name__ == '__main__':
    main(sys.argv[1:])
