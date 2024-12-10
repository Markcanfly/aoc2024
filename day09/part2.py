import sys


def print_disk(disk: list):
    print("".join("".join(map(str, el)) for el in disk))


def all_empty(diskpart: list) -> bool:
    return all(x == "." for x in diskpart)


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

    # Cache empty places
    empty_places = {idx: len([p for p in b if p == "."]) for idx, b in enumerate(disk)}

    for endblock_i in range(len(disk) - 1, -1, -1):
        endblock = disk[endblock_i]
        if not all_empty(endblock):
            # Find first block with sufficient space left
            for startblock_i in range(len(disk)):
                if (
                    empty_places[startblock_i] >= len(endblock)
                    and startblock_i < endblock_i
                ):
                    startblock = disk[startblock_i]
                    start = len(startblock) - empty_places[startblock_i]
                    for idx, el in enumerate(endblock):
                        startblock[start + idx] = el
                    disk[endblock_i] = len(endblock) * ["."]
                    empty_places[startblock_i] -= len(endblock)
                    break
    print_disk(disk)
    flattened_disk = [b for fragment in disk for b in fragment]
    checksum = sum(idx * val for idx, val in enumerate(flattened_disk) if val != ".")
    print("Checksum:", checksum)


if __name__ == "__main__":
    main()
