import sys
from functools import cache


@cache
def blink(number: int) -> int | tuple[int, int]:
    if number == 0:
        return 1
    elif len(str_item := str(number)) % 2 == 0:
        return int(str_item[: len(str_item) // 2]), int(str_item[len(str_item) // 2 :])
    else:
        return 2024 * number


@cache
def count_splits_into(number: int, after: int) -> int:
    """Find out how many numbers this will split into after an arbitrary number of iterations"""
    if after == 0:
        return 1
    match blink(number):
        case (n1, n2):
            return count_splits_into(n1, after - 1) + count_splits_into(n2, after - 1)
        case next_number:
            return count_splits_into(next_number, after - 1)


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        lst = list(map(int, infile.read().strip().split(" ")))

    iterations = 75
    print(sum(count_splits_into(starter, iterations) for starter in lst))


if __name__ == "__main__":
    main()
