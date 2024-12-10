import itertools
import sys
from math import log
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
    equation_left = equation_with_ops[0]
    total = 0
    # since all our operations add, if we run over the equation left
    # we can short circuit and return false
    for next, op in equation_with_ops[1]:
        match op:
            case "":
                total = next
            case "+":
                total += next
            case "*":
                total *= next
            case "||":
                total = 10 ** int(log(next, 10) + 1) * total + next
            case _:
                raise ValueError("invalid operation:", op)
        if total > equation_left:
            return False

    return total == equation_left


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
Total Calibration Result: 249943041417600
         32844822 function calls in 13.771 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   13.771   13.771 {built-in method builtins.exec}
        1    0.000    0.000   13.771   13.771 part2_impr.py:1(<module>)
        1    0.001    0.001   13.761   13.761 part2_impr.py:52(main)
      850    1.894    0.002   13.759    0.016 {built-in method builtins.any}
  6747297    6.392    0.000    7.672    0.000 part2_impr.py:19(correct_equation)
  6747532    4.192    0.000    4.193    0.000 part2_impr.py:11(all_possible_versions)
 19343989    1.280    0.000    1.280    0.000 {built-in method math.log}
        1    0.000    0.000    0.010    0.010 <frozen importlib._bootstrap>:1349(_find_and_load)
        1    0.000    0.000    0.010    0.010 <frozen importlib._bootstrap>:1304(_find_and_load_unlocked)
        1    0.000    0.000    0.010    0.010 <frozen importlib._bootstrap>:911(_load_unlocked)
        1    0.000    0.000    0.010    0.010 <frozen importlib._bootstrap>:806(module_from_spec)
        3    0.000    0.000    0.010    0.003 <frozen importlib._bootstrap>:480(_call_with_frames_removed)
        1    0.000    0.000    0.010    0.010 <frozen importlib._bootstrap_external>:1287(create_module)
        1    0.010    0.010    0.010    0.010 {built-in method _imp.create_dynamic}
      850    0.000    0.000    0.000    0.000 part2_impr.py:7(op_combinations)
     1700    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1240(_find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1520(find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1491(_get_spec)
      850    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
      855    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        4    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1593(find_spec)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.sum}
        1    0.000    0.000    0.000    0.000 typing.py:392(inner)
        1    0.000    0.000    0.000    0.000 typing.py:1449(__getitem__)
        1    0.000    0.000    0.000    0.000 {built-in method _io.open}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
      616    0.000    0.000    0.000    0.000 part2_impr.py:67(<genexpr>)
        5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:140(_path_stat)
        5    0.000    0.000    0.000    0.000 {built-in method posix.stat}
        1    0.000    0.000    0.000    0.000 typing.py:1458(copy_with)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:416(__enter__)
        1    0.000    0.000    0.000    0.000 typing.py:1242(__init__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:159(_path_isfile)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:150(_path_is_mode_type)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        5    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1469(_path_importer_cache)
       16    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:126(_path_join)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:304(acquire)
        1    0.000    0.000    0.000    0.000 {built-in method posix.getcwd}
        4    0.000    0.000    0.000    0.000 typing.py:1454(<genexpr>)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:733(_init_module_attrs)
        6    0.000    0.000    0.000    0.000 typing.py:1188(__setattr__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1588(_get_spec)
        4    0.000    0.000    0.000    0.000 <frozen codecs>:319(decode)
        1    0.000    0.000    0.000    0.000 typing.py:1147(__init__)
        3    0.000    0.000    0.000    0.000 typing.py:175(_type_check)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:162(__enter__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:802(spec_from_file_location)
        1    0.000    0.000    0.000    0.000 typing.py:262(_collect_parameters)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:420(__exit__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:426(_get_module_lock)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:124(setdefault)
        6    0.000    0.000    0.000    0.000 typing.py:1134(_is_dunder)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1295(exec_module)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:372(release)
        1    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:632(cached)
       32    0.000    0.000    0.000    0.000 {method 'rstrip' of 'str' objects}
        4    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
        7    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
       16    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
       18    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:611(_get_cached)
        1    0.000    0.000    0.000    0.000 {built-in method _imp.exec_dynamic}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:74(__new__)
       19    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:491(_verbose_message)
        7    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        3    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
        1    0.000    0.000    0.000    0.000 <frozen codecs>:309(__init__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1128(find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:185(_path_abspath)
        6    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:445(cb)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:232(__init__)
        6    0.000    0.000    0.000    0.000 {method 'rpartition' of 'str' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:982(find_spec)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:82(remove)
        3    0.000    0.000    0.000    0.000 typing.py:166(_type_convert)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:180(_path_isabs)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:645(parent)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:173(__exit__)
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1226(__exit__)
        3    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1222(__enter__)
        4    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:67(_relax_case)
        3    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 typing.py:295(_check_generic)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:79(__init__)
        5    0.000    0.000    0.000    0.000 {built-in method _imp.acquire_lock}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.is_builtin}
        4    0.000    0.000    0.000    0.000 typing.py:1246(<genexpr>)
        5    0.000    0.000    0.000    0.000 {built-in method _imp.release_lock}
        2    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        2    0.000    0.000    0.000    0.000 {method '__exit__' of '_thread.RLock' objects}
        1    0.000    0.000    0.000    0.000 {method 'pop' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _imp.find_frozen}
        2    0.000    0.000    0.000    0.000 {built-in method _thread.get_ident}
        1    0.000    0.000    0.000    0.000 {built-in method __new__ of type object at 0x1032d4990}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:599(__init__)
        1    0.000    0.000    0.000    0.000 {method 'remove' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _weakref._remove_dead_weakref}
        1    0.000    0.000    0.000    0.000 <frozen codecs>:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'pop' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _thread.allocate_lock}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:158(__init__)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:412(__init__)
        1    0.000    0.000    0.000    0.000 {built-in method posix.fspath}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:653(has_location)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1276(__init__)
"""
