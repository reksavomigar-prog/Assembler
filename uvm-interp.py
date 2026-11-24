import argparse


def mask(n: int) -> int:
    return 2 ** n - 1  #


reg = 0
mem = [0] * 50  #[cite: 1]


def execute(bytecode: bytes) -> None:
    global reg

    for i in range(0, len(bytecode), 4):
        cmd = int.from_bytes(bytecode[i : i + 4], "little")
        op = cmd & 0b111

        if op == 0:
            const = (cmd >> 3) & mask(24)
            reg = const
        elif op == 1:
            reg = mem[reg]
        elif op == 7:
            addr = (cmd >> 3) & mask(15)
            mem[addr] = reg
        elif op == 4:
            addr = (cmd >> 3) & mask(15)
            reg = int(reg >= mem[addr])
        else:
            raise ValueError(f"Неизвестный код операции: {op}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Интерпретатор УВМ")
    parser.add_argument(
        "binary",
        nargs="?",
        default="uvm-output.bin",
    )
    args = parser.parse_args()

    with open(args.binary, "rb") as f:
        bytecode = f.read()  #[cite: 1]

    execute(bytecode)  #[cite: 1]
    print("reg:", reg)
    print("mem:", mem)


if __name__ == "__main__":
    main()