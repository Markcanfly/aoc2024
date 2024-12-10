import sys


def print_disk(disk: list):
    print("".join("".join(map(str, el)) for el in disk))


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        line = infile.read().strip()

    disk = []
    for idx, elem in enumerate(line):
        if idx % 2 == 0:
            id = idx // 2
            disk.append(int(elem) * [id])
        else:
            if int(elem) > 0:
                disk.append(int(elem) * ["."])

    print_disk(disk)
    BIG_DISK = len(disk) > 90

    # Cache empty places and length
    empty_places = {idx: len([p for p in b if p == "."]) for idx, b in enumerate(disk)}
    length = {idx: len(b) for idx, b in enumerate(disk)}

    for endblock_i in range(len(disk) - 1, -1, -1):
        endblock = disk[endblock_i]
        if not empty_places[endblock_i] == length[endblock_i]:
            # Find first block with sufficient empty places left
            for startblock_i in range(endblock_i):
                if empty_places[startblock_i] >= length[endblock_i]:
                    startblock = disk[startblock_i]
                    start = length[startblock_i] - empty_places[startblock_i]
                    for idx, el in enumerate(endblock):
                        startblock[start + idx] = el
                    disk[endblock_i] = length[endblock_i] * ["."]
                    empty_places[startblock_i] -= length[endblock_i]
                    if not BIG_DISK:
                        print_disk(disk)
                    break
    if BIG_DISK:
        print_disk(disk)
    flattened_disk = [b for fragment in disk for b in fragment]
    checksum = sum(idx * val for idx, val in enumerate(flattened_disk) if val != ".")
    print("Checksum:", checksum)


if __name__ == "__main__":
    main()
