class Board:
    width = 8
    height = 8
    knight_coordinate = None
    goal_coordinate = None
    obstacle_coordinates = None

    def __init__(self, knight_coordinate, goal_coordinate, obstacle_coordinates):
        self.knight_coordinate = State(self, knight_coordinate)
        self.goal_coordinate = goal_coordinate
        self.obstacle_coordinates = obstacle_coordinates
        self.path = []

        self.board = [['-' for _ in range(self.width)] for _ in range(self.height)]

        # knight position
        knight_x, knight_y = self.knight_coordinate.state_coordinate
        self.board[knight_x][knight_y] = 'K'

        # goal position
        goal_x, goal_y = self.goal_coordinate
        self.board[goal_x][goal_y] = 'G'

        # obstacles' positions
        for obstacle_coordinate in obstacle_coordinates:
            x, y = obstacle_coordinate
            self.board[x][y] = 'X'

    # Prints the board before doing any moves
    def print_board(self):
        print('    ', end='')
        [print(i, end='\t') for i in range(8)]
        print("\n")

        x = 0

        for row in self.board:
            print(x, end='\t')
            x += 1
            # unpack and print row values, separated with tabs '\t'
            print(*row, sep='\t')

        print("\n")

    # Checks if the coordinate is in bounds with the board
    @staticmethod
    def in_bounds(coordinate):
        x, y = coordinate
        return 0 <= x < Board.width and 0 <= y < Board.height

    # Prints the shortest path from the start to the goal
    def print_path(self):
        if len(self.path) == 1:
            print("No solution")
            return

        print("Game: \n")
        self.print_board()

        print("Steps & Final: \n")
        x, y = self.path[0]
        self.board[x][y] = '-'
        for p in self.path[1:]:
            (x, y) = p
            self.board[x][y] = 'K'
            self.print_board()
            self.board[x][y] = '-'


class State:
    board = None

    def __init__(self, given_board, state_coordinate):
        self.state_coordinate = state_coordinate
        self.children = []
        self.closed = []

        State.board = given_board

    # Finds the valid children of the current state
    def find_children(self):
        moves = [(1, 2), (2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1), (-2, 1), (-1, 2)]

        for move in moves:
            final_move = tuple(map(lambda x, y: x + y, self.state_coordinate, move))
            if Board.in_bounds(final_move):
                if State.is_valid(self, move):
                    current_state = State(State.board, final_move)
                    current_state.set_closed(self.closed[:], self.state_coordinate)
                    self.children.append(current_state)

        return self.children[:]

    # Returns closed list
    def get_closed(self):
        return self.closed[:]

    # Updates the closed list of each state
    def set_closed(self, closed, parent):
        self.closed = closed[:]
        self.closed.append(parent)

    # Checks if the possible move contains an obstacle or not

    def is_valid(self, possible_move):
        paths = [self.moveOnAxis(possible_move, self.state_coordinate, 'X'),
                 self.moveOnAxis(possible_move, self.state_coordinate, 'Y')]

        # at least one path is valid
        return sum(1 for _ in filter(lambda path: 'X' not in path, paths)) >= 1

    # Checks if the current coordinate is the goal coordinate
    def is_goal(self):
        return self.state_coordinate == State.board.goal_coordinate

    def moveOnAxis(self, axis, knight, start='X'):
        path = []
        x, y = axis

        currentX, currentY = knight

        if start == 'X':
            for i in range(abs(x)):
                currentX = (-i + knight[0] + -1) if x < 0 else (i + knight[0] + 1)
                path.append(State.board.board[currentX][currentY])

            for i in range(abs(y)):
                currentY = (-i + knight[1] + -1) if y < 0 else (i + knight[1] + 1)
                path.append(State.board.board[currentX][currentY])

        else:
            for i in range(abs(y)):
                currentY = (-i + knight[1] + -1) if y < 0 else (i + knight[1] + 1)
                path.append(State.board.board[currentX][currentY])

            for i in range(abs(x)):
                currentX = (-i + knight[0] + -1) if x < 0 else (i + knight[0] + 1)
                path.append(State.board.board[currentX][currentY])

        return path
    # Gets the children of each current state until it reaches the goal

    @staticmethod
    def bfs(Open):
        while len(Open) != 0:
            states_to_visit = []

            for state in Open:
                if state.is_goal():
                    visited = state.get_closed()
                    return visited

                states_to_visit.extend(state.find_children())

            Open = states_to_visit[:]
        return []
