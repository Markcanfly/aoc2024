import sys
from typing import Literal

class RanIntoWall(Exception):
    pass

def print_board(board: list[list[str]], robot: tuple[int, int]):
    for y in range(len(board)):
        for x in range(len(board[0])):
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


def tiles_to_move(pos: tuple[int, int], direction: Literal["<", ">", "^", "v"], mx: list[list[str]]) -> set[tuple[int,int]] | None:
    def tiles_to_move_or_raise(pos: tuple[int, int], direction: Literal["<", ">", "^", "v"], mx: list[list[str]]) -> list[tuple[int,int]]:
        next_pos = step_towards(pos, direction)
        next_item = mx[next_pos[1]][next_pos[0]]
        match next_item:
            case "[":
                if direction in ("^", "v"):
                    return [next_pos, (next_pos[0] + 1, next_pos[1])] + tiles_to_move_or_raise(next_pos, direction, mx) + tiles_to_move_or_raise((next_pos[0] + 1, next_pos[1]), direction, mx)
                else:
                    return [next_pos] + tiles_to_move_or_raise(next_pos, direction, mx)
            case "]":
                if direction in ("^", "v"):
                    return [next_pos, (next_pos[0] - 1, next_pos[1])] + tiles_to_move_or_raise(next_pos, direction, mx) + tiles_to_move_or_raise((next_pos[0] - 1, next_pos[1]), direction, mx)
                else:
                    return [next_pos] + tiles_to_move_or_raise(next_pos, direction, mx)
            case ".":
                return []
            case "#":
                raise RanIntoWall()
            case otherwise:
                raise ValueError(f"unexpected elem in field: {otherwise} at {next_pos}")

    try:
        return set(tiles_to_move_or_raise(pos, direction, mx))
    except RanIntoWall:
        return None

def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        raw_board, raw_moves = infile.read().split("\n\n")

    board = [list(b) for b in raw_board.split("\n")]
    moves: list[Literal["<", ">", "^", "v"]] = list("".join(raw_moves.split("\n")))  # pyright: ignore

    # supersize board
    def morph(char: str) -> str:
        match char:
            case "#":
                return "##"
            case "O":
                return "[]"
            case ".":
                return ".."
            case "@":
                return "@."
            case otherwise:
                raise ValueError(f"unexpected elem in field: {otherwise}")

    board = [list("".join(morph(b) for b in line)) for line in board]
    # extract robot
    robot = [
        (x, y)
        for x in range(len(board[0]))
        for y in range(len(board))
        if board[y][x] == "@"
    ][0]
    board[robot[1]][robot[0]] = "."
    
    print("Initial state:")
    print_board(board, robot)
    print()

    for move in moves:
        if (to_move := tiles_to_move(robot, move, board)) is not None:
            robot = step_towards(robot, move)
            # move tiles
            tiles: dict[tuple[int,int], str] = dict()
            for tile_pos in to_move:
                tiles[tile_pos] = board[tile_pos[1]][tile_pos[0]]
                board[tile_pos[1]][tile_pos[0]] = "."
            for tile_pos, tile in tiles.items():
                next_tile_pos = step_towards(tile_pos, move)
                board[next_tile_pos[1]][next_tile_pos[0]] = tile
 
    print("Final state:")
    print_board(board, robot)
    print()

    sum_coords = sum(
        [
            y * 100 + x
            for x in range(len(board[0]))
            for y in range(len(board))
            if board[y][x] == "["
        ]
    )
    print("Sum of box coordinates:", sum_coords)


if __name__ == "__main__":
    main()
