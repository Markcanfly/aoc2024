import sys


def mix(value: int, secret: int) -> int:
    return value ^ secret


def prune(secret: int) -> int:
    return secret % 16777216


def next_secret(secret: int) -> int:
    secret = prune(mix(secret * 64, secret))
    secret = prune(mix(secret // 32, secret))
    secret = prune(mix(secret * 2048, secret))
    return secret


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        initial_numbers = tuple(map(int, infile.read().strip().split("\n")))

    results: dict[int, list[int]] = {number: [number] for number in initial_numbers}

    up_to = 2000
    for _ in range(up_to):
        for number in initial_numbers:
            results[number].append(next_secret(results[number][-1]))

    # for number in initial_numbers:
    #     print(f"{number}: {results[number][-1]}")

    print("Sum of 2000th secret numbers:", sum(res[-1] for res in results.values()))


if __name__ == "__main__":
    main()
