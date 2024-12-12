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

                        color_props[node][0] += len(next_neighbours)
                        color_props[node][1] += 1

        properties = {
            first_node: (prop[1], 4 * prop[1] - prop[0])
            for first_node, prop in color_props.items()
        }
        pprint(properties)
        total_cost = sum(area * perimeter for area, perimeter in properties.values())
        print("Total Cost:", total_cost)


if __name__ == "__main__":
    main()
