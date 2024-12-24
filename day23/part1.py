import sys
from itertools import combinations


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        edges = set(
            map(
                lambda x: tuple(sorted(x.split("-"))), infile.read().strip().split("\n")
            )
        )

    nodes = set(node for edge in edges for node in edge)

    clicks: list[tuple[str, str, str]] = []
    for three_nodes in combinations(nodes, r=3):
        if any(x.startswith("t") for x in three_nodes):
            if all(
                (n1, n2) in edges for n1, n2 in combinations(sorted(three_nodes), r=2)
            ):
                clicks.append(three_nodes)

    print("Number of clicks containing a node starting with t:", len(clicks))


if __name__ == "__main__":
    main()
