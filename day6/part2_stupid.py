import enum
import sys
from dataclasses import dataclass, field

COUNT_LOL = 0

class Direction(enum.Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


@dataclass
class Agent:
    location: tuple[int, int]
    direction: Direction

    turns: list[tuple[tuple[int, int], Direction]] = field(default_factory=lambda: [])

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

    def step(self, mx: list[list[str]], size: tuple[int, int]) -> bool | tuple[int,int]:
        global COUNT_LOL
        next, tile = self.next_pos(mx, size)
        if tile is None:
            return False
        match tile:
            case "#" | "O":
                if (self.location, self.direction) in self.turns:
                    print("Time loop!", (self.location,self.direction))
                    COUNT_LOL += 1
                    return False
                self.turn()
            case _:
                self.location = next
                mx[self.location[0]][self.location[1]] = "X"
        return True

    def turn(self):
        self.turns.append((self.location, self.direction))
        self.direction = Direction((self.direction.value + 1) % len(Direction))


def print_mx(mx: list[list[str]], agents: list[Agent]):
    for line in mx:
        print("".join(line))


def main():
    # if len(sys.argv) != 2:
    #     raise ValueError("expected: inputfile")

    # with open(sys.argv[1]) as infile:
    with open("data/input") as infile:
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
    agent_initial_location = agent.location
    while agent.step(mx, mx_size):
        # print_mx(mx, agents=[agent])
        # print()
        pass

    print("Places visited", "".join("".join(line) for line in mx).count("X"))

    # Use the visited places thing to generate all possible locations for an obstacle
    # Go through all matrices and put an obstacle on an already visited
    for y in range(mx_size[0]):
        for x in range(mx_size[1]):
            if mx[y][x] == "X" and (y,x) != agent_initial_location:
                extra_obstacle_mx = [list(line) for line in text.strip().split("\n")]
                
                agent_positions = [
                    (y, x)
                    for y in range(len(extra_obstacle_mx))
                    for x in range(len(extra_obstacle_mx[0]))
                    if extra_obstacle_mx[y][x] == "^" or extra_obstacle_mx[y][x] == ">" or extra_obstacle_mx[y][x] == "v" or extra_obstacle_mx[y][x] == "<"
                ]
                agents = []
                for y_, x_ in agent_positions:
                    match extra_obstacle_mx[y_][x_]:
                        case "<":
                            a = Agent((y_, x_), Direction.LEFT)
                        case "^":
                            a = Agent((y_, x_), Direction.UP)
                        case ">":
                            a = Agent((y_, x_), Direction.RIGHT)
                        case "v":
                            a = Agent((y_, x_), Direction.DOWN)
                    agents.append(a)  # pyright: ignore
                    extra_obstacle_mx[y_][x_] = "."

                extra_obstacle_mx[y][x] = "O"
                agent = agents[0]
                while agent.step(extra_obstacle_mx, mx_size):
                    # print_mx(extra_obstacle_mx, agents=[agent])
                    # print()
                    pass
    print(COUNT_LOL)
    



if __name__ == "__main__":
    main()
