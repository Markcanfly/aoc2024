import itertools
import sys
from functools import reduce
from typing import Generator


def op_combinations(length: int) -> itertools.product:
    return itertools.product("+*", repeat=length)


def all_possible_versions(
    constants: tuple[int, tuple[int, ...]],
) -> Generator[tuple[int, tuple[tuple[int, str], ...]], None, None]:
    ops = op_combinations(len(constants[1]) - 1)
    for op_combo in ops:
        yield (constants[0], tuple(zip(constants[1], itertools.chain([""], op_combo))))


def correct_equation(
    equation_with_ops: tuple[int, tuple[tuple[int, str], ...]],
) -> bool:
    """equation: (15, ((5, ""), (7, "*"), ...))"""

    def perform_op_with_acc(current_result: int, next_part: tuple[int, str]) -> int:
        value, op = next_part
        match op:
            case "":
                # first value
                return value
            case "+":
                return current_result + value
            case "*":
                return current_result * value
            case _:
                raise ValueError("invalid operation:", op)

    return equation_with_ops[0] == reduce(perform_op_with_acc, equation_with_ops[1], 0)


def print_eq(equation_with_ops: tuple[int, tuple[tuple[int, str], ...]]):
    print(
        f"{equation_with_ops[0]} ==",
        f"{' '.join([f'{equation_with_ops[1][i][0]} {equation_with_ops[1][i+1][1]}' for i in range(len(equation_with_ops[1]) - 1)] + [str(equation_with_ops[1][-1][0])])}",
    )


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        raw_equations = [line.strip().split(": ") for line in infile]
    equations = [
        (int(eq[0]), tuple(map(int, eq[1].split(" ")))) for eq in raw_equations
    ]

    correct = [
        equation
        for equation in equations
        if any(map(correct_equation, all_possible_versions(equation)))
    ]
    print("Total Calibration Result:", sum(cor[0] for cor in correct))


if __name__ == "__main__":
    main()
