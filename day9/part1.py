import sys


def print_disk(disk: list):
    print("".join(list(map(str, disk))))


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        line = infile.read().strip()

    disk = []
    for idx, elem in enumerate(line):
        if idx % 2 == 0:
            id = idx // 2
            disk.extend(int(elem) * [id])
        else:
            disk.extend(int(elem) * ["."])

    print_disk(disk)

    for idx, elem in enumerate(disk):
        if elem == "." and idx != len(disk) - 1:
            while (popped := disk.pop()) == ".":
                continue
            disk[idx] = popped
    print_disk(disk)

    checksum = sum(idx * int(elem) for idx, elem in enumerate(disk))
    print("Checksum:", checksum)


if __name__ == "__main__":
    main()
