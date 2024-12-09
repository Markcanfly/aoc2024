import itertools
import sys
from functools import reduce
from typing import Generator


def op_combinations(length: int) -> itertools.product:
    return itertools.product(("+", "*", "||"), repeat=length)


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
            case "||":
                return int(f"{current_result}{value}")
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

    # for eq in equations:
    #     print("---")
    #     print(eq)
    #     for eq_op in all_possible_versions(eq):
    #         print(correct_equation(eq_op), end=" ")
    #         print_eq(eq_op)


if __name__ == "__main__":
    main()

"""
➜  day7 uv run python -m cProfile part2.py data/input
Total Calibration Result: 249943041417600
         96715724 function calls in 24.235 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   24.235   24.235 {built-in method builtins.exec}
        1    0.000    0.000   24.235   24.235 part2.py:1(<module>)
        1    0.002    0.002   24.235   24.235 part2.py:51(main)
      850    2.137    0.003   24.233    0.029 {built-in method builtins.any}
  6747297    1.536    0.000   17.722    0.000 part2.py:19(correct_equation)
  6747297    5.799    0.000   16.187    0.000 {built-in method _functools.reduce}
 76467804   10.387    0.000   10.387    0.000 part2.py:24(perform_op_with_acc)
  6747532    4.373    0.000    4.374    0.000 part2.py:11(all_possible_versions)
      850    0.001    0.000    0.001    0.000 part2.py:7(op_combinations)
     1700    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
      852    0.000    0.000    0.000    0.000 {built-in method builtins.len}
      850    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 typing.py:392(inner)
        1    0.000    0.000    0.000    0.000 typing.py:1449(__getitem__)
        1    0.000    0.000    0.000    0.000 {built-in method _io.open}
      616    0.000    0.000    0.000    0.000 part2.py:66(<genexpr>)
        1    0.000    0.000    0.000    0.000 typing.py:1458(copy_with)
        1    0.000    0.000    0.000    0.000 typing.py:1242(__init__)
        4    0.000    0.000    0.000    0.000 typing.py:1454(<genexpr>)
        4    0.000    0.000    0.000    0.000 <frozen codecs>:319(decode)
        6    0.000    0.000    0.000    0.000 typing.py:1188(__setattr__)
        1    0.000    0.000    0.000    0.000 typing.py:1147(__init__)
        3    0.000    0.000    0.000    0.000 typing.py:175(_type_check)
        1    0.000    0.000    0.000    0.000 typing.py:262(_collect_parameters)
        6    0.000    0.000    0.000    0.000 typing.py:1134(_is_dunder)
        4    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
        1    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        1    0.000    0.000    0.000    0.000 <frozen codecs>:309(__init__)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
       13    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
        6    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        3    0.000    0.000    0.000    0.000 typing.py:166(_type_convert)
        1    0.000    0.000    0.000    0.000 typing.py:295(_check_generic)
        4    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
        4    0.000    0.000    0.000    0.000 typing.py:1246(<genexpr>)
        1    0.000    0.000    0.000    0.000 <frozen codecs>:260(__init__)
"""
