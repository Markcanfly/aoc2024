import sys
from typing import Generator


def print_mx(mx: list[list[int]]):
    for row in mx:
        print(row)


def in_mx(mx: list[list[int]], coordinates: tuple[int, int]) -> bool:
    return 0 <= coordinates[0] < len(mx[0]) and 0 <= coordinates[1] < len(mx)


def neighbours(
    mx: list[list[int]], curr: tuple[int, int]
) -> Generator[tuple[int, int], None, None]:
    # ←→↑↓
    for next in [
        (curr[0], curr[1] - 1),
        (curr[0], curr[1] + 1),
        (curr[0] - 1, curr[1]),
        (curr[0] + 1, curr[1]),
    ]:
        if in_mx(mx, next) and mx[next[1]][next[0]] - mx[curr[1]][curr[0]] == 1:
            yield next


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        mx = [list(map(int, list(line.strip()))) for line in infile]

    zeroes_reach: dict[tuple[int, int], set[tuple[int, int]]] = dict()
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            if mx[y][x] == 0:
                zeroes_reach[(x, y)] = set()
    print(zeroes_reach)

    for zero in zeroes_reach:
        # BFS
        visited = []
        to_visit = list(neighbours(mx, zero))
        while to_visit:
            current = to_visit.pop(0)
            visited.append(current)
            to_visit.extend(n for n in neighbours(mx, current) if n not in visited)
            if mx[current[1]][current[0]] == 9:
                zeroes_reach[zero].add(current)
    print(zeroes_reach)

    total_score = sum([len(peaks) for peaks in zeroes_reach.values()])
    print("Total Score:", total_score)


if __name__ == "__main__":
    main()
