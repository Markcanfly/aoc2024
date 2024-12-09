import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict


@dataclass
class Vec:
    y: int
    x: int

    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.y + other.y, self.x + other.x)

    def __sub__(self, other: "Vec") -> "Vec":
        return Vec(self.y - other.y, self.x - other.x)

    def __eq__(self, other) -> bool:
        return self.y == other.y and self.x == other.x

    def __lt__(self, other) -> bool:
        return self.y < other.y and self.x < other.x

    def __le__(self, other) -> bool:
        return self.y <= other.y and self.x <= other.x

    def __hash__(self) -> int:
        return hash((self.y, self.x))


def print_mx(mx: list[str], antinodes: list[Vec]):
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            if Vec(y, x) in antinodes:
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
    size = (len(mx), len(mx[0]))

    antenna_positions: DefaultDict[str, list[Vec]] = defaultdict(list)
    for y in range(size[0]):
        for x in range(size[1]):
            tile = mx[y][x]
            if tile != ".":
                antenna_positions[tile].append(Vec(y, x))

    antinodes: list[Vec] = []
    for antennae in antenna_positions.values():
        for a1, a2 in itertools.permutations(antennae, r=2):
            antinode = a2 + (a2 - a1)
            if Vec(0, 0) <= antinode < Vec(size[0], size[1]):
                # within board
                antinodes.append(antinode)

    print("Number of unique antinodes within board:", len(frozenset(antinodes)))
    print_mx(mx, list(antinodes))


if __name__ == "__main__":
    main()
