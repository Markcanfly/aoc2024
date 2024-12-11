import sys


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        lst = list(map(int, infile.read().strip().split(" ")))

    for s in range(25):
        if s < 5:
            print(" ".join(map(str, lst)))
        i = 0
        while i < len(lst):
            item = lst[i]
            if item == 0:
                lst[i] = 1
            elif len(str_item := str(item)) % 2 == 0:
                first, second = (
                    int(str_item[: len(str_item) // 2]),
                    int(str_item[len(str_item) // 2 :]),
                )
                lst[i] = first
                lst.insert(i + 1, second)
                i += 1  # skip next element
            else:
                lst[i] = item * 2024
            i += 1

    print("After 25 blinks:", len(lst))


if __name__ == "__main__":
    main()
