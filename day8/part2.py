import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Generator


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec") -> "Vec":
        return Vec(self.x - other.x, self.y - other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other) -> bool:
        return self.x < other.x and self.y < other.y

    def __le__(self, other) -> bool:
        return self.x <= other.x and self.y <= other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Line:
    """Line defined as the equation x=my+b"""

    m: float
    b: float

    def grid_points(self, size: tuple[int, int]) -> Generator[Vec, None, None]:
        for x in range(size[1]):
            candidate_y = self.m * x + self.b
            candidate_vec = Vec(x, round(candidate_y))
            if (abs(candidate_y - round(candidate_y)) < 0.01) and Vec(
                0, 0
            ) <= candidate_vec < Vec(size[1], size[0]):  # only check whole numbers
                yield candidate_vec


def print_mx(mx: list[str], antinodes: list[Vec]):
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            if mx[y][x] != ".":
                print(mx[y][x], end="")
            elif Vec(y, x) in antinodes:
                print("#", end="")
            else:
                print(mx[y][x], end="")
        print()
    print()


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        mx = [line.strip() for line in infile]
    size = (len(mx[0]), len(mx))

    antenna_positions: DefaultDict[str, list[Vec]] = defaultdict(list)
    for y in range(size[0]):
        for x in range(size[1]):
            tile = mx[y][x]
            if tile != ".":
                antenna_positions[tile].append(Vec(x, y))

    lines: list[Line] = []
    for antennae in antenna_positions.values():
        for a1, a2 in itertools.combinations(antennae, r=2):
            # direction vector of line
            direction = a2 - a1
            m = direction.y / direction.x
            b = a2.y - a2.x * m
            new_line = Line(m, b)
            # print(new_line, a1, a2)
            lines.append(new_line)

    antinodes = [node for line in lines for node in line.grid_points(size)]

    print_mx(mx, antinodes)
    print("Unique Antinodes for lines:", len(frozenset(antinodes)))


if __name__ == "__main__":
    main()
