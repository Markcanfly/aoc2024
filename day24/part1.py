import sys
from enum import Enum


class Op(Enum):
    AND = "AND"
    XOR = "XOR"
    OR = "OR"


def perform_op(op: Op, a: bool, b: bool) -> bool:
    match op:
        case Op.AND:
            return a & b
        case Op.XOR:
            return a ^ b
        case Op.OR:
            return a | b


def main():
    if len(sys.argv) != 2:
        raise ValueError("1 argument expected: inputfile")

    with open(sys.argv[1]) as infile:
        raw_base_states, raw_gates = infile.read().split("\n\n")

    base_states = [
        ((w := line.split(": "))[0], bool(int(w[1])))
        for line in raw_base_states.split("\n")
    ]

    gates: dict[str, tuple[Op, tuple[str, str]]] = {
        (g := line.split(" -> "))[1]: (Op[(p := g[0].split(" "))[1]], (p[0], p[2]))
        for line in raw_gates.strip().split("\n")
    }

    evaluated: dict[str, bool] = {wire: state for wire, state in base_states}

    eval_stack = [wire for wire in gates if wire.startswith("z")]
    while eval_stack:
        wire = eval_stack.pop()
        if wire in evaluated:
            continue
        else:
            op, operands = gates[wire]
            w1, w2 = operands
            if not any(w in evaluated for w in (w1, w2)):
                eval_stack.extend((wire, w1, w2))
            elif w1 not in evaluated:
                eval_stack.extend((wire, w1))
            elif w2 not in evaluated:
                eval_stack.extend((wire, w2))
            else:
                evaluated[wire] = perform_op(op, evaluated[w1], evaluated[w2])

    z_number = int(
        "".join(
            str(int(evaluated[w]))
            for w in sorted(evaluated, reverse=True)
            if w.startswith("z")
        ),
        2,
    )
    print("z number:", z_number)


if __name__ == "__main__":
    main()
