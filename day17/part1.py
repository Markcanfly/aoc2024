import sys
from typing import Literal


def combo(
    operand: Literal[0, 1, 2, 3, 4, 5, 6, 7],
    registers: dict[Literal["A", "B", "C"], int],
) -> int:  # pyright: ignore (can't handle complex matches)
    match operand:
        case n if 0 <= n <= 3:
            return n
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case 7:
            raise NotImplementedError("combo operand 7 is reserved")


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        raw_registers, raw_program = infile.read().split("\n\n")
        reg: dict[Literal["A", "B", "C"], int] = {
            reg: int(raw_registers.split("\n")[idx].removeprefix(f"Register {reg}: "))
            for idx, reg in enumerate(["A", "B", "C"])
        }  # pyright: ignore

        program = tuple(
            map(int, raw_program.strip().removeprefix("Program: ").split(","))
        )

        operations: list[
            tuple[Literal[0, 1, 2, 3, 4, 5, 6, 7], Literal[0, 1, 2, 3, 4, 5, 6, 7]]
        ] = list((program[idx], program[idx + 1]) for idx in range(0, len(program), 2))  # pyright: ignore (I promise it's correct)

    ptr = 0
    print_buffer = []
    while 0 <= ptr < len(operations):
        jumped = False
        opcode, operand = operations[ptr]
        match opcode:
            case 0:  # adv
                reg["A"] = reg["A"] // (2 ** combo(operand, reg))
            case 1:  # bxl
                reg["B"] = reg["B"] ^ operand
            case 2:  # bst
                reg["B"] = combo(operand, reg) % 8
            case 3:  # jnz
                if reg["A"] != 0:
                    jumped = True
                    ptr = operand
            case 4:  # bxc
                reg["B"] = reg["B"] ^ reg["C"]
            case 5:  # out
                print_buffer.append(combo(operand, reg) % 8)
            case 6:  # bdv
                reg["B"] = reg["A"] // (2 ** combo(operand, reg))
            case 7:  # cdv
                reg["C"] = reg["A"] // (2 ** combo(operand, reg))
        if not jumped:
            ptr += 1

    print(",".join(map(str, print_buffer)))


if __name__ == "__main__":
    main()
