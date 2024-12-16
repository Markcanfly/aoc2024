import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Literal


def is_within(pos: tuple[int, int], mx: list[str]) -> bool:
    return 0 <= pos[1] < len(mx) and 0 <= pos[0] < len(mx[0])


@dataclass
class Runner:
    loc: tuple[int, int]
    board: list[str]
    end: tuple[int, int]
    global_visited: dict[
        tuple[tuple[int, int], Literal["<", ">", "^", "v"]], float | int
    ]
    direction: Literal["<", ">", "^", "v"] = ">"
    cost: int | float = 0
    path: list[tuple[int, int]] = field(default_factory=list)

    @property
    def done(self):
        return self.loc == self.end

    def neighbours(
        self,
    ) -> list[tuple[tuple[int, int], int, Literal["<", ">", "^", "v"]]]:
        """
        Returns:
            list of (next_pos, next_cost, next_dir)
        """
        match self.direction:
            case "<":
                nbs = [
                    ((self.loc[0] - 1, self.loc[1]), self.cost + 1, "<"),
                    ((self.loc[0], self.loc[1] - 1), self.cost + 1001, "^"),
                    ((self.loc[0], self.loc[1] + 1), self.cost + 1001, "v"),
                ]
            case ">":
                nbs = [
                    ((self.loc[0] + 1, self.loc[1]), self.cost + 1, ">"),
                    ((self.loc[0], self.loc[1] - 1), self.cost + 1001, "^"),
                    ((self.loc[0], self.loc[1] + 1), self.cost + 1001, "v"),
                ]
            case "^":
                nbs = [
                    ((self.loc[0], self.loc[1] - 1), self.cost + 1, "^"),
                    ((self.loc[0] - 1, self.loc[1]), self.cost + 1001, "<"),
                    ((self.loc[0] + 1, self.loc[1]), self.cost + 1001, ">"),
                ]
            case "v":
                nbs = [
                    ((self.loc[0], self.loc[1] + 1), self.cost + 1, "v"),
                    ((self.loc[0] - 1, self.loc[1]), self.cost + 1001, "<"),
                    ((self.loc[0] + 1, self.loc[1]), self.cost + 1001, ">"),
                ]

        return [
            n
            for n in nbs
            if is_within(n[0], self.board) and self.board[n[0][1]][n[0][0]] != "#"
        ]  # pyright: ignore

    def step(self) -> list["Runner"]:
        if self.global_visited[(self.loc, self.direction)] < self.cost:
            self.cost = float("infinity")
            return []
        self.global_visited[(self.loc, self.direction)] = self.cost
        self.path.append(self.loc)

        next_positions = self.neighbours()

        if not next_positions and not self.done:
            # ran into a wall
            self.cost = float("infinity")
            return []

        self.loc, self.cost, self.direction = next_positions[0]

        other_agents: list["Runner"] = []
        for location, cost, direction in next_positions[1:]:
            other_agents.append(
                Runner(
                    location,
                    self.board,
                    self.end,
                    self.global_visited,
                    direction,
                    cost,
                    path=self.path.copy(),
                )
            )

        return other_agents


def print_board(board: list[str], runners: list[Runner]):
    runner_coords = {runner.loc: runner.direction for runner in runners}
    for y in range(len(board)):
        for x in range(len(board[0])):
            if (x, y) in runner_coords:
                print(runner_coords[(x, y)], end="")
            else:
                print(board[y][x], end="")
        print()


def print_paths(board: list[str], nodes: set[tuple[int, int]]):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if (x, y) in nodes:
                print("O", end="")
            else:
                print(board[y][x], end="")
        print()


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        board = [line.strip() for line in infile]

    start = [
        (x, y)
        for x in range(len(board[0]))
        for y in range(len(board))
        if board[y][x] == "S"
    ][0]

    finish = [
        (x, y)
        for x in range(len(board[0]))
        for y in range(len(board))
        if board[y][x] == "E"
    ][0]

    global_visited: dict[
        tuple[tuple[int, int], Literal["<", ">", "^", "v"]], float | int
    ] = defaultdict(lambda: float("inf"))
    runners: list[Runner] = [Runner(start, board, finish, global_visited)]

    best_cost = float("inf")
    winners: list[Runner] = []
    while runners:
        current_runners = runners.copy()
        for runner in current_runners:
            new_runners = runner.step()
            if runner.done:
                runners.remove(runner)
                if runner.cost <= best_cost:
                    winners.append(runner)
                    best_cost = runner.cost
                continue
            if runner.cost > best_cost or runner.cost == float("inf"):
                runners.remove(runner)
                continue
            runners += new_runners

    winner_paths = set(
        node for winner in winners if winner.cost == best_cost for node in winner.path
    )
    print_paths(board, winner_paths)
    print("Winner path nodes", len(winner_paths) + 1)


if __name__ == "__main__":
    main()
