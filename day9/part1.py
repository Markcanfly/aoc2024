import sys


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        line = infile.read().strip()

    disk = []
    for idx, elem in enumerate(line):
        if idx % 2 == 0:
            id = idx // 2
            disk.append(int(elem) * str(id))
        else:
            disk.append(int(elem) * ".")

    disk = list("".join(disk))  # condense

    for idx, elem in enumerate(disk):
        if elem == "." and idx != len(disk) - 1:
            while (popped := disk.pop()) == ".":
                pass
            disk[idx] = popped
            # print("".join(disk))

    print("".join(disk))

    checksum = sum(idx * int(elem) for idx, elem in enumerate(disk))
    print("Checksum:", checksum)


if __name__ == "__main__":
    main()
