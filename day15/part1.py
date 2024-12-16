import sys
from typing import Generator, Literal


def print_board(board: list[list[str]], robot: tuple[int, int]):
    for y in range(len(board[0])):
        for x in range(len(board)):
            if robot == (x, y):
                print("@", end="")
            else:
                print(board[y][x], end="")
        print()


def step_towards(
    pos: tuple[int, int], direction: Literal["<", ">", "^", "v"]
) -> tuple[int, int]:
    match direction:
        case "<":
            vec = (-1, 0)
        case ">":
            vec = (1, 0)
        case "^":
            vec = (0, -1)
        case "v":
            vec = (0, 1)
    return (pos[0] + vec[0], pos[1] + vec[1])


def is_within(pos: tuple[int, int], mx: list[list[str]]) -> bool:
    return 0 <= pos[1] < len(mx) and 0 <= pos[0] < len(mx[0])


def items_in_direction(
    pos: tuple[int, int], direction: Literal["<", ">", "^", "v"], mx: list[list[str]]
) -> Generator[tuple[tuple[int, int], str], None, None]:
    while is_within((next_pos := step_towards(pos, direction)), mx):
        pos = next_pos
        yield next_pos, mx[next_pos[1]][next_pos[0]]


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        # with open("data/tiny_example_input") as infile:
        raw_board, raw_moves = infile.read().split("\n\n")

    board = [list(b) for b in raw_board.split("\n")]
    moves: list[Literal["<", ">", "^", "v"]] = list("".join(raw_moves.split("\n")))  # pyright: ignore

    # extract robot
    robot = [
        (x, y)
        for x in range(len(board[0]))
        for y in range(len(board))
        if board[y][x] == "@"
    ][0]
    board[robot[1]][robot[0]] = "."

    for move in moves:
        boxes: list[tuple[int, int]] = []
        # print(f"Move {move}:")
        for pos, val in items_in_direction(robot, move, board):
            match val:
                case ".":
                    robot = step_towards(robot, move)
                    for box in boxes:
                        board[box[1]][box[0]] = "."
                    for box in boxes:
                        next_box = step_towards(box, move)
                        board[next_box[1]][next_box[0]] = "O"
                    break
                case "O":
                    boxes.append(pos)
                case "#":
                    pass
                    break

    sum_coords = sum(
        [
            y * 100 + x
            for x in range(len(board[0]))
            for y in range(len(board))
            if board[y][x] == "O"
        ]
    )
    print("Sum of box coordinates", sum_coords)


if __name__ == "__main__":
    main()
