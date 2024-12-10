import itertools
import sys
from typing import Callable


def consistent_with(li: tuple[int, ...], inverse_rules: set[tuple[int, int]]) -> bool:
    for combination in itertools.combinations(li, r=2):
        if combination in inverse_rules:
            return False
    return True


def rule_comparator(rules: set[tuple]) -> Callable[[int, int], int]:
    def compare(a: int, b: int) -> int:
        if (a, b) in rules:
            return -1
        elif (b, a) in rules:
            return 1
        else:
            return 0

    return compare


def main():
    if len(sys.argv) != 2:
        raise ValueError("expected: inputfile")

    with open(sys.argv[1]) as infile:
        text = infile.read()

    raw_rules, raw_lists = text.split("\n\n")

    rules = set(
        (int(rule.split("|")[0]), int(rule.split("|")[1]))
        for rule in raw_rules.strip().split("\n")
    )

    lists = [tuple(map(int, list.split(","))) for list in raw_lists.split()]

    # Part 1
    inverse_rules = set((b, a) for a, b in rules)
    consistent_lists = [li for li in lists if consistent_with(li, inverse_rules)]

    middle_page_numbers = [li[len(li) // 2] for li in consistent_lists]
    print("Sum of middle page numbers:", sum(middle_page_numbers))

    # Part 2
    # inconsistent_lists = [li for li in lists if not consistent_with(li, inverse_rules)]
    # fixed_inconsistent_lists = [
    #     tuple(sorted(li, key=cmp_to_key(rule_comparator(rules))))
    #     for li in inconsistent_lists
    # ]
    # fixed_middle_page_numbers = [li[len(li) // 2] for li in fixed_inconsistent_lists]
    # print(
    #     "Sum of middle page numbers of fixed inconsistent lists:",
    #     sum(fixed_middle_page_numbers),
    # )


if __name__ == "__main__":
    main()
