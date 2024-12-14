import sys
import time


def longest_repeated(searchspace: str, char: str) -> int:
    rep = 0
    while char * (rep + 1) in searchspace:
        rep += 1
    return rep


def extract_robot(raw_robot: str) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        map(
            lambda x: tuple(map(int, x.split(","))),
            raw_robot.strip().removeprefix("p=").split(" v="),
        )
    )  # pyright: ignore


def create_map(
    size_x: int, size_y: int, robots: set[tuple[int, int]]
) -> list[tuple[str, int]]:
    lst: list[tuple[str, int]] = []
    for y in range(size_y):
        line: list[str] = []
        for x in range(size_x):
            if (x, y) in robots:
                line.append("█")
            else:
                line.append(" ")
        lst_str = "".join(line)
        lst.append((lst_str, longest_repeated(lst_str, "█")))
    return lst


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        robots = [extract_robot(line) for line in infile]

    size_x = 101
    size_y = 103

    iter = 0
    while True:
        robots_final_positions = set(
            (
                (robot[0][0] + robot[1][0] * iter) % size_x,
                (robot[0][1] + robot[1][1] * iter) % size_y,
            )
            for robot in robots
        )
        robot_map = create_map(size_x, size_y, robots_final_positions)
        max_robot_in_lines = max(count for _, count in robot_map)
        if (
            max_robot_in_lines > 10
        ):  # intuition: tree will have at least one long line of robots
            print(iter)
            for line, _ in robot_map:
                print(line)
            time.sleep(1)

        iter += 1


if __name__ == "__main__":
    main()
