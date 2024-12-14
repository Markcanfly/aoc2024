import sys
from functools import reduce


def extract_robot(raw_robot: str) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        map(
            lambda x: tuple(map(int, x.split(","))),
            raw_robot.strip().removeprefix("p=").split(" v="),
        )
    )  # pyright: ignore


def coord_within(
    coord: tuple[int, int], topleft: tuple[int, int], bottomright: tuple[int, int]
) -> bool:
    return (
        topleft[0] <= coord[0] < bottomright[0]
        and topleft[1] <= coord[1] < bottomright[1]
    )


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        robots = [extract_robot(line) for line in infile]

    iter = 100
    size_x = 101
    size_y = 103

    robots_final_positions = [
        (
            (robot[0][0] + robot[1][0] * iter) % size_x,
            (robot[0][1] + robot[1][1] * iter) % size_y,
        )
        for robot in robots
    ]

    quadrants: dict[tuple[tuple[int, int], tuple[int, int]], int] = {
        (corner1, corner2): 0
        for corner1, corner2 in (
            ((0, 0), (size_x // 2, size_y // 2)),
            ((size_x // 2 + 1, 0), (size_x, size_y // 2)),
            ((0, size_y // 2 + 1), (size_x // 2, size_y)),
            ((size_x // 2 + 1, size_y // 2 + 1), (size_x, size_y)),
        )
    }

    for robot_pos in robots_final_positions:
        for topleft, bottomright in quadrants:
            if coord_within(robot_pos, topleft, bottomright):
                quadrants[(topleft, bottomright)] += 1
                break

    print("Safety Factor:", reduce(lambda acc, val: acc * val, quadrants.values()))


if __name__ == "__main__":
    main()
