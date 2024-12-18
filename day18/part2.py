import sys
from typing import Generator


def print_mx(mx: list[list[str]]):
    for line in mx:
        print("".join(line))


def print_mx_nodes(mx: list[list[str]], nodes: set[tuple[int, int]]):
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            print("O" if (x, y) in nodes else mx[y][x], end="")
        print()


def in_mx(mx: list[list[str]], coordinates: tuple[int, int]) -> bool:
    return 0 <= coordinates[0] < len(mx[0]) and 0 <= coordinates[1] < len(mx)


def neighbours(
    mx: list[list[str]], curr: tuple[int, int]
) -> Generator[tuple[int, int], None, None]:
    # ←→↑↓
    for next in [
        (curr[0], curr[1] - 1),
        (curr[0], curr[1] + 1),
        (curr[0] - 1, curr[1]),
        (curr[0] + 1, curr[1]),
    ]:
        if in_mx(mx, next) and mx[next[1]][next[0]] != "#":
            yield next


def manhattan_distance(node1: tuple[int, int], node2: tuple[int, int]) -> int:
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])


def path_exists(
    mx: list[list[str]], source: tuple[int, int], dest: tuple[int, int]
) -> bool:
    # A-Star
    visited: set[tuple[int, int]] = set()
    queue = [(0, source)]
    g_score: dict[tuple[int, int], int] = {source: 0}

    while queue:
        curr = queue.pop(0)[1]
        if curr == dest:
            return True
        visited.add(curr)
        for neighbour in neighbours(mx, curr):
            tentative_g = g_score[curr] + 1

            if neighbour not in g_score or tentative_g < g_score[neighbour]:
                # estimate distance based on manhattan distance from goal
                f_score = tentative_g + manhattan_distance(curr, dest)
                g_score[neighbour] = tentative_g
                queue.append((f_score, neighbour))
                # keep queue sorted by distance estimate
                queue.sort()

    return False


def main():
    if len(sys.argv) != 3:
        raise ValueError("2 arguments expected: inputfile size")

    with open(sys.argv[1]) as infile:
        corruption = [tuple(map(int, line.strip().split(","))) for line in infile]

    size = int(sys.argv[2])

    for byte_index in range(len(corruption)):
        print(byte_index)
        mx = [
            [
                "#" if (x, y) in corruption[: byte_index + 1] else "."
                for x in range(size + 1)
            ]
            for y in range(size + 1)
        ]
        if not path_exists(mx, (0, 0), (size, size)):
            print("First byte preventing escape:", corruption[byte_index])
            break


if __name__ == "__main__":
    main()
