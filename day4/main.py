import sys

# Part 1


def horizontal_forward(mx, row, col, word: str) -> bool:
    """check whether this character starts a horizontal forward occurrence of the word"""
    return mx[row][col : col + len(word)] == word


def horizontal_backward(mx, row, col, word: str) -> bool:
    """check whether this character starts a horizontal backward occurrence of the word"""
    return col - len(word) >= 0 and mx[row][col - len(word) : col] == word


def horizontal(mx, row, col, word: str) -> int:
    """number of horizontal occurrences of word that this mx[row][col] starts"""
    return horizontal_forward(mx, row, col, word) + horizontal_backward(
        mx, row, col, word
    )


def vertical(mx, row, col, word: str) -> int:
    """number of vertical occurrences of word that this mx[row][col] starts"""
    return 0


def diagonal(mx, row, col, word: str) -> int:
    """number of diagonal occurrences of word that this mx[row][col] starts"""
    return 0


def main():
    if len(sys.argv) != 2:
        raise ValueError("expected: inputfile")

    with open(sys.argv[1]) as infile:
        text = infile.read()

    chars_mx = text.split("\n")

    occurrences = 0
    word = "XMAS"
    for row in range(len(chars_mx)):
        for col in range(len(chars_mx[0])):
            occurrences += (
                horizontal(chars_mx, row, col, word)
                + vertical(chars_mx, row, col, word)
                + diagonal(chars_mx, row, col, word)
            )
    print(f"Occurrences of word {word} in matrix:", occurrences)


if __name__ == "__main__":
    main()
