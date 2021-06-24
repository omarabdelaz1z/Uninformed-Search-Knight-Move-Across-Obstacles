import chess


def play(board: chess.Board):
    Open = board.knight_coordinate.find_children()

    if board.knight_coordinate.is_goal():
        board.path = board.knight_coordinate.get_closed()
    else:
        board.path = chess.State.bfs(Open[:])

    board.path.append(goal_coordinate)

    if len(board.path) == 1:
        board.print_path()
    else:
        print("Moves from start to goal: ")
        print(*board.path, sep=", ")
        board.print_path()


if __name__ == '__main__':
    knight_coordinate = (0, 0)
    goal_coordinate = (6, 6)
    obstacles_coordinates = [(1, 4), (2, 2), (6, 2), (4, 4), (1, 5), (3, 7)]

    board = chess.Board(knight_coordinate, goal_coordinate, obstacles_coordinates)
    play(board)
