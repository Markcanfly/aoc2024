import enum
import sys
from dataclasses import dataclass


class Direction(enum.Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


@dataclass
class Agent:
    location: tuple[int, int]
    direction: Direction

    def __str__(self):
        match self.direction:
            case Direction.LEFT:
                return "<"
            case Direction.UP:
                return "^"
            case Direction.RIGHT:
                return ">"
            case Direction.DOWN:
                return "v"
        return "?"

    def next_pos(
        self, mx: list[list[str]], size: tuple[int, int]
    ) -> tuple[tuple[int, int], str | None]:
        match self.direction:
            case Direction.LEFT:
                new_pos = (self.location[0], self.location[1] - 1)
                if self.location[1] == 0:
                    return new_pos, None
            case Direction.RIGHT:
                new_pos = (self.location[0], self.location[1] + 1)
                if self.location[1] == size[1] - 1:
                    return new_pos, None
            case Direction.UP:
                new_pos = (self.location[0] - 1, self.location[1])
                if self.location[0] == 0:
                    return new_pos, None
            case Direction.DOWN:
                new_pos = (self.location[0] + 1, self.location[1])
                if self.location[0] == size[0] - 1:
                    return new_pos, None
        return new_pos, mx[new_pos[0]][new_pos[1]]

    def step(self, mx: list[list[str]], size: tuple[int, int]) -> bool:
        next, tile = self.next_pos(mx, size)
        if tile is None:
            return False
        match tile:
            case "#":
                self.turn()
            case _:
                self.location = next
                mx[self.location[0]][self.location[1]] = "X"
        return True

    def turn(self):
        if self.direction.value == len(Direction) - 1:
            self.direction = Direction(0)
        else:
            self.direction = Direction(self.direction.value + 1)


def print_mx(mx: list[list[str]], agents: list[Agent]):
    for line in mx:
        print("".join(line))


def main():
    if len(sys.argv) != 2:
        raise ValueError("expected: inputfile")

    with open(sys.argv[1]) as infile:
        text = infile.read()

    mx = [list(line) for line in text.strip().split("\n")]
    mx_size = (len(mx), len(mx[0]))

    # extract agent
    agent_positions = [
        (y, x)
        for y in range(len(mx))
        for x in range(len(mx[0]))
        if mx[y][x] == "^" or mx[y][x] == ">" or mx[y][x] == "v" or mx[y][x] == "<"
    ]
    agents = []
    for y, x in agent_positions:
        match mx[y][x]:
            case "<":
                a = Agent((y, x), Direction.LEFT)
            case "^":
                a = Agent((y, x), Direction.UP)
            case ">":
                a = Agent((y, x), Direction.RIGHT)
            case "v":
                a = Agent((y, x), Direction.DOWN)
        agents.append(a)  # pyright: ignore
        mx[y][x] = "X"

    agent = agents[0]
    while agent.step(mx, mx_size):
        print_mx(mx, agents=[agent])
        print()

    print("Places visited", "".join("".join(line) for line in mx).count("X"))


if __name__ == "__main__":
    main()
