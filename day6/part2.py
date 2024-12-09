import enum
import sys
from dataclasses import dataclass, field


class Direction(enum.Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __str__(self):
        match self:
            case Direction.LEFT:
                return "<"
            case Direction.UP:
                return "^"
            case Direction.RIGHT:
                return ">"
            case Direction.DOWN:
                return "v"
        
    def __repr__(self):
        return f"Direction: {str(self)}"


def move_in_direction(
    location: tuple[int, int], direction: Direction
) -> tuple[int, int]:
    match direction:
        case Direction.LEFT:
            return (location[0], location[1] - 1)
        case Direction.RIGHT:
            return (location[0], location[1] + 1)
        case Direction.UP:
            return (location[0] - 1, location[1])
        case Direction.DOWN:
            return (location[0] + 1, location[1])
    



@dataclass
class Agent:
    location: tuple[int, int]
    direction: Direction
    turns: list[tuple[tuple[int, int], Direction]] = field(default_factory=lambda: [])
    loop_inducing_obstacles: list[tuple[int, int]] = field(default_factory=lambda: [])

    # exploration: pretending there's a new obstacle and seeing where it goes
    exploration_turns: list[tuple[tuple[int, int], Direction]] = field(
        default_factory=lambda: []
    )
    new_obstacle: tuple[tuple[int, int], Direction] | None = None

    def __str__(self):
        return str(self.direction)

    def next_location(
        self, mx: list[list[str]], size: tuple[int, int]
    ) -> tuple[tuple[int, int], str | None]:
        new_pos = move_in_direction(self.location, self.direction)
        if not (0 <= new_pos[0] < size[0] and 0 <= new_pos[1] < size[1]):
            return new_pos, None

        return new_pos, mx[new_pos[0]][new_pos[1]]

    def step(self, mx: list[list[str]], size: tuple[int, int]) -> bool:
        next_pos, tile = self.next_location(mx, size)

        if self.new_obstacle is not None:  # exploring
            if tile is None:
                # didn't work out lol
                # reset
                self.location = self.new_obstacle[0]
                self.direction = self.new_obstacle[1]
                self.new_obstacle = None
            else:
                match tile:
                    case "#":
                        if (self.location, self.direction) in self.turns or (
                            self.location,
                            self.direction,
                        ) in self.exploration_turns:
                            self.loop_inducing_obstacles.append(
                                move_in_direction(
                                    self.new_obstacle[0],  # pyright: ignore
                                    self.new_obstacle[1],  # pyright: ignore
                                )
                            )
                            # cool, found a loop, reset
                            print("found a loop:", self.new_obstacle)
                            self.location = self.new_obstacle[0]
                            self.direction = self.new_obstacle[1]
                            self.new_obstacle = None
                        else:
                            self.exploration_turns.append((self.location, self.direction))
                            self.turn()
                    case _:
                        self.location = next_pos
        else:
            if tile is None:
                return False
            match tile:
                case "#":
                    self.turns.append((self.location, self.direction))
                    self.turn()
                case _:
                    mx[self.location[0]][self.location[1]] = "X"

                    # Any time we don't have to turn, actually pretend we do and go down that way
                    self.new_obstacle = next_pos, self.direction
                    self.exploration_turns = [(self.location, self.direction)]
                    self.turn()

        return True

    

    def turn(self):
        if self.direction.value == len(Direction) - 1:
            self.direction = Direction(0)
        else:
            self.direction = Direction(self.direction.value + 1)


def print_mx(mx: list[list[str]], agents: list[Agent]):
    for y in range(len(mx)):
        for x in range(len(mx[0])):
            if agents[0].location == (y, x):
                print(str(agents[0]), end="")
            else:
                print(mx[y][x], end="")
        print()
    print()


def main():
    # if len(sys.argv) != 2:
    #     raise ValueError("expected: inputfile")

    # with open(sys.argv[1]) as infile:
    with open("data/example_input") as infile:
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
    agent_start_location = agent.location
    while agent.step(mx, mx_size):
        # print_mx(mx, agents=[agent])
        # print()
        pass

    print("Places visited", "".join("".join(line) for line in mx).count("X"))
    
    print("Number of possible timeloop obstacles:", len([loc for loc in agent.loop_inducing_obstacles]))


if __name__ == "__main__":
    main()
