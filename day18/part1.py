import sys
from typing import Generator


def print_mx(mx: list[list[str]]):
    for line in mx:
        print("".join(line))


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


def main():
    if len(sys.argv) != 4:
        raise ValueError("3 arguments expected: inputfile size first")

    with open(sys.argv[1]) as infile:
        corruption = [tuple(map(int, line.strip().split(","))) for line in infile]

    size = int(sys.argv[2])
    first = int(sys.argv[3])
    corrupt_bytes = set(corruption[:first])

    mx = [
        ["#" if (x, y) in corrupt_bytes else "." for x in range(size + 1)]
        for y in range(size + 1)
    ]
    print_mx(mx)

    # Find shortest path using dijkstra's
    distance: dict[tuple[int, int], int | float] = {
        (x, y): float("inf") for x in range(size + 1) for y in range(size + 1)
    }
    distance[(0, 0)] = 0
    queue = [(0, 0)]
    while queue:
        curr = queue.pop(0)
        if distance[curr] > distance[(size, size)]:
            continue
        for neighbour in neighbours(mx, curr):
            if distance[neighbour] > distance[curr] + 1:
                distance[neighbour] = distance[curr] + 1
                queue.append(neighbour)

    print("Distance to end:", distance[(size, size)])


if __name__ == "__main__":
    main()
