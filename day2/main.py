import itertools
import sys
from typing import Iterable


# Part One
def strictly_monotonous(differences: Iterable[int]) -> bool:
    return all(d > 0 for d in differences) or all(d < 0 for d in differences)


def values_are_between(values: Iterable[int], start: int, end: int) -> bool:
    """Check whether all values of a tuple are within the inclusive range [start,end]"""
    return all(start <= abs(v) <= end for v in values)


def safe(report: tuple[int, ...]) -> bool:
    """Check whether a report is safe

    The report must be strictly monotonous, and the differences between consecutive
    values must be between [1,3] (both inclusive).
    """
    differences = tuple(report[i] - report[i - 1] for i in range(1, len(report)))
    return strictly_monotonous(differences) and values_are_between(differences, 1, 3)


# Part Two
def versions_with_k_dropped(
    report: tuple[int, ...], k_dropped: int
) -> list[tuple[int, ...]]:
    """Generate all versions of a report with `k_dropped` elements removed"""
    if k_dropped > len(report) - 1:
        raise ValueError("cannot drop all elements")
    return list(itertools.combinations(report, r=len(report) - k_dropped))


def partly_safe(report: tuple[int, ...], k_dropped: int) -> bool:
    """Check whether a report is safe, allowing for removal of `k_dropped` values"""
    return any(safe(r) for r in versions_with_k_dropped(report, k_dropped))


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        reports = [tuple(map(int, line.strip().split(" "))) for line in infile]

    print("Safe Reports: " + str(len([r for r in reports if safe(r)])))
    print(
        "Safe Reports with 1 level removed: "
        + str(len([r for r in reports if partly_safe(r, k_dropped=1)]))
    )


if __name__ == "__main__":
    main()
