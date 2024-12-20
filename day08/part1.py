import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict


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


def print_mx(mx: list[str], antinodes: list[Vec]):
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            if Vec(x, y) in antinodes:
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
    for y in range(size[1]):
        for x in range(size[0]):
            tile = mx[y][x]
            if tile != ".":
                antenna_positions[tile].append(Vec(x, y))

    antinodes: list[Vec] = []
    for antennae in antenna_positions.values():
        for a1, a2 in itertools.permutations(antennae, r=2):
            antinode = a2 + (a2 - a1)
            if Vec(0, 0) <= antinode < Vec(size[1], size[0]):
                # within board
                antinodes.append(antinode)

    print("Number of unique antinodes within board:", len(frozenset(antinodes)))
    print_mx(mx, list(antinodes))


if __name__ == "__main__":
    main()
