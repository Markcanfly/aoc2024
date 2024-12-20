import sys
from itertools import groupby
from typing import Generator


def print_mx(mx: list[str]):
    print("\n".join(mx))


def distances_from(
    source_node: tuple[int, int], cutoff_node: tuple[int, int], mx: list[str]
) -> dict[tuple[int, int], int | float]:
    distance: dict[tuple[int, int], int | float] = {
        (x, y): float("inf") for x in range(len(mx[0])) for y in range(len(mx))
    }
    distance[source_node] = 0
    queue = [source_node]
    while queue:
        curr = queue.pop(0)
        if distance[curr] > distance[cutoff_node]:
            continue
        for neighbour in neighbours(curr, mx):
            if distance[neighbour] > distance[curr] + 1:
                distance[neighbour] = distance[curr] + 1
                queue.append(neighbour)
    return distance


def neighbours(
    curr: tuple[int, int],
    mx: list[str],
) -> Generator[tuple[int, int], None, None]:
    # ←→↑↓
    for neighbour in [
        (curr[0], curr[1] - 1),
        (curr[0], curr[1] + 1),
        (curr[0] - 1, curr[1]),
        (curr[0] + 1, curr[1]),
    ]:
        if is_within(neighbour, mx) and mx[neighbour[1]][neighbour[0]] != "#":
            yield neighbour


def cheat_neighbours(
    curr: tuple[int, int],
    mx: list[str],
) -> Generator[tuple[int, int], None, None]:
    # Direct neighbours
    for wall, neighbour in [
        ((curr[0], curr[1] - 1), (curr[0], curr[1] - 2)),
        ((curr[0], curr[1] + 1), (curr[0], curr[1] + 2)),
        ((curr[0] - 1, curr[1]), (curr[0] - 2, curr[1])),
        ((curr[0] + 1, curr[1]), (curr[0] + 2, curr[1])),
    ]:
        if (
            is_within(neighbour, mx)
            and mx[wall[1]][wall[0]] == "#"
            and mx[neighbour[1]][neighbour[0]] != "#"
        ):
            yield neighbour


def is_within(pos: tuple[int, int], mx: list[str]) -> bool:
    return 0 <= pos[1] < len(mx) and 0 <= pos[0] < len(mx[0])


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        mx = [line.strip() for line in infile]

    start = [
        (x, y) for x in range(len(mx[0])) for y in range(len(mx)) if mx[y][x] == "S"
    ][0]

    finish = [
        (x, y) for x in range(len(mx[0])) for y in range(len(mx)) if mx[y][x] == "E"
    ][0]

    distance_from_start = distances_from(start, cutoff_node=finish, mx=mx)
    distance_from_finish = distances_from(finish, cutoff_node=start, mx=mx)

    best_legal = distance_from_start[finish]
    saved_time_by_cheating: list[int] = []

    # find possible cheat edges and their scores
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            if mx[y][x] != "#":
                for neighbour in cheat_neighbours((x, y), mx):
                    cheat_score = (
                        distance_from_start[(x, y)]
                        + distance_from_finish[neighbour]
                        + 2
                    )
                    if cheat_score < best_legal:
                        saved_time_by_cheating.append(best_legal - cheat_score)  # pyright: ignore

    counts = [
        (psec, len(list(group)))
        for psec, group in groupby(sorted(saved_time_by_cheating))
    ]

    print(
        "Number of cheats that would save more than 100 picoseconds:",
        sum(count for psec, count in counts if psec >= 100),
    )


if __name__ == "__main__":
    main()
