import sys
from collections import defaultdict
from pprint import pprint
from typing import Generator


def in_mx(mx: list[str], coordinates: tuple[int, int]) -> bool:
    return 0 <= coordinates[0] < len(mx[0]) and 0 <= coordinates[1] < len(mx)


def neighbours(
    mx: list[str], curr: tuple[int, int]
) -> Generator[tuple[int, int], None, None]:
    # ←→↑↓
    for next in [
        (curr[0], curr[1] - 1),
        (curr[0], curr[1] + 1),
        (curr[0] - 1, curr[1]),
        (curr[0] + 1, curr[1]),
    ]:
        if in_mx(mx, next) and mx[next[1]][next[0]] == mx[curr[1]][curr[0]]:
            yield next


def is_corner_in(mx: list[str], curr: tuple[int, int], dir: tuple[int, int]) -> bool:
    color = mx[curr[1]][curr[0]]
    neighbour1 = (
        mx[curr[1]][curr[0] + dir[0]] if 0 <= curr[0] + dir[0] < len(mx[0]) else "OUT"
    )
    neighbour2 = (
        mx[curr[1] + dir[1]][curr[0]] if 0 <= curr[1] + dir[1] < len(mx[1]) else "OUT"
    )
    neighbour_across = (
        mx[curr[1] + dir[1]][curr[0] + dir[0]]
        if 0 <= curr[0] + dir[0] < len(mx[0]) and 0 <= curr[1] + dir[1] < len(mx[1])
        else "OUT"
    )
    outer_corner = color != neighbour1 and color != neighbour2
    inner_corner = (
        color == neighbour1 and color == neighbour2 and color != neighbour_across
    )
    return outer_corner or inner_corner


def corner_count(mx: list[str], curr: tuple[int, int]) -> int:
    return sum(
        is_corner_in(mx, curr, direction)
        for direction in ((1, 1), (1, -1), (-1, 1), (-1, -1))
    )


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        mx = [line.strip() for line in infile]

        # (total_degree, total_node_count)
        color_props: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])

        # BFS
        visited = []
        for x in range(len(mx)):
            for y in range(len(mx[0])):
                node = (x, y)
                to_visit = [node]
                while to_visit:
                    next = to_visit.pop(0)
                    if next not in visited:
                        visited.append(next)

                        next_neighbours = list(neighbours(mx, next))
                        to_visit.extend(
                            neigh for neigh in next_neighbours if neigh not in visited
                        )

                        color_props[node][0] += 1
                        color_props[node][1] += corner_count(mx, next)

        pprint(color_props)
        total_cost = sum(area * sides for area, sides in color_props.values())
        print("Total Cost:", total_cost)


if __name__ == "__main__":
    main()
