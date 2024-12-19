import sys


def valid(string: str, words: set[str]) -> bool:
    candidates: list[str] = [string]
    while candidates:
        candidate = candidates.pop(0)
        for word in words:
            if candidate.startswith(word):
                rest = candidate.removeprefix(word)
                if rest == "":
                    return True
                if rest not in candidates:
                    candidates.append(rest)
    return False


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        raw_words, raw_strings = infile.read().split("\n\n")
    words = set(raw_words.strip().split(", "))
    strings = raw_strings.strip().split("\n")

    valid_strings = [string for string in strings if valid(string, words)]

    print("Number of valid strings:", len(valid_strings))


if __name__ == "__main__":
    main()
