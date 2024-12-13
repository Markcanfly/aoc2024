import sys
from math import isclose

import numpy as np


def extract_machine(raw_machine: str) -> tuple[np.ndarray, np.ndarray]:
    parts = raw_machine.split("\n")
    return (
        np.array(
            [
                list(map(int, parts[0].removeprefix("Button A: X+").split(", Y+"))),
                list(map(int, parts[1].removeprefix("Button B: X+").split(", Y+"))),
            ]
        ).transpose(),
        np.array(list(map(int, parts[2].removeprefix("Prize: X=").split(", Y=")))),
    )


def is_round(number: np.float64) -> bool:
    return isclose(number, np.round(number))


def machine_cost(machine: tuple[np.ndarray, np.ndarray], a_cost, b_cost) -> int | None:
    A, b = machine
    x = np.linalg.solve(A, b)
    if (is_round(x[0]) and is_round(x[1])) and (0 <= x[0] and 0 <= x[1]):
        return int(a_cost * np.round(x[0]) + b_cost * np.round(x[1]))
    else:
        return None


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        raw_machines = infile.read().split("\n\n")

    machines = [extract_machine(machine) for machine in raw_machines]

    total_cost = sum(
        cost
        for machine in machines
        if (cost := machine_cost(machine, 3, 1)) is not None
    )
    print("Total cost of all viable machines:", total_cost)


if __name__ == "__main__":
    main()
