import sys

import numpy as np

# Part 1


def get_diagonals(mx: np.ndarray) -> list:
    return get_straight_diagonals(mx) + get_straight_diagonals(np.fliplr(mx))


def get_straight_diagonals(mx: np.ndarray) -> list:
    diagonals = []
    for i in range(0, mx.shape[0]):
        diagonals.append(np.diagonal(mx, offset=i))
    for i in range(1, mx.shape[1]):
        # starts from 1 to avoid getting center diagonal twice
        diagonals.append(np.diagonal(mx, offset=-i))
    return diagonals


def main():
    if len(sys.argv) != 2:
        raise ValueError("expected: inputfile")

    with open(sys.argv[1]) as infile:
        text = infile.read()

    mx = np.array([np.array(list(line)) for line in text.strip().split("\n")])

    # Part 1
    horizontals = ["".join(row.tolist()) for row in mx]
    verticals = ["".join(row.tolist()) for row in mx.transpose()]
    diagonals = ["".join(row.tolist()) for row in get_diagonals(mx)]

    word = "XMAS"
    word_reversed = "".join(reversed(list(word)))

    word_count = sum(
        candidate.count(word) + candidate.count(word_reversed)
        for candidate in horizontals + verticals + diagonals
    )

    print(f"Occurrences of word {word} in matrix:", word_count)

    # Part 2
    cross_mas_count = 0
    for row in range(mx.shape[0]):
        for col in range(mx.shape[1]):
            if (
                mx[row, col] == "A"
                and 0 < row < mx.shape[0] - 1
                and 0 < col < mx.shape[1] - 1
            ):
                cross_straight = "".join(
                    [mx[row - 1, col - 1], mx[row, col], mx[row + 1, col + 1]]
                )
                cross_reversed = "".join(
                    [mx[row + 1, col - 1], mx[row, col], mx[row - 1, col + 1]]
                )
                cross_mas_count += (
                    (cross_straight == "MAS")
                    + (cross_straight == "SAM")
                    + (cross_reversed == "MAS")
                    + (cross_reversed == "SAM")
                ) == 2
    print("X-MAS count", cross_mas_count)


if __name__ == "__main__":
    main()
