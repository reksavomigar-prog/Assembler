import argparse
import csv


def mask(n: int) -> int:
    return 2 ** n - 1


def asm_const(x: int) -> bytes:
    cmd = 0
    cmd |= (x & mask(24)) << 3
    return cmd.to_bytes(4, "little")


def asm_read() -> bytes:
    cmd = 1
    return cmd.to_bytes(4, "little")


def asm_write(b: int) -> bytes:
    cmd = 7
    cmd |= (b & mask(15)) << 3
    return cmd.to_bytes(4, "little")


def asm_ge(b: int) -> bytes:
    cmd = 4
    cmd |= (b & mask(15)) << 3
    return cmd.to_bytes(4, "little")


def parse_csv(filepath: str) -> list[dict]:
    program = []
    with open(filepath, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for line_num, row in enumerate(reader, start=1):
            if not row or not row[0].strip() or row[0].strip().startswith("#"):
                continue

            op = row[0].strip().lower()
            if line_num == 1 and op in ("op", "command", "cmd"):
                continue  # пропускаем заголовок таблицы, если он есть

            if op == "load":
                program.append({"op": "load", "A": 0, "B": int(row[1].strip())})
            elif op == "read":
                program.append({"op": "read", "A": 1})
            elif op == "ge":
                program.append({"op": "ge", "A": 4, "B": int(row[1].strip())})
            elif op == "write":
                program.append({"op": "write", "A": 7, "B": int(row[1].strip())})
            else:
                raise ValueError(f"Строка {line_num}: неизвестная команда '{op}'")

    return program


def asm(program: list[dict]) -> bytes:
    bytecode = bytearray()
    for cmd in program:
        op = cmd["op"]
        if op == "load":
            bytecode.extend(asm_const(cmd["B"]))
        elif op == "read":
            bytecode.extend(asm_read())
        elif op == "write":
            bytecode.extend(asm_write(cmd["B"]))
        elif op == "ge":
            bytecode.extend(asm_ge(cmd["B"]))
    return bytes(bytecode)


def practice() -> None:
    assert list(asm_const(1006)) == [0x70, 0x1F, 0x00, 0x00]
    assert list(asm_read()) == [0x01, 0x00, 0x00, 0x00]
    assert list(asm_write(713)) == [0x4F, 0x16, 0x00, 0x00]
    assert list(asm_ge(278)) == [0xB4, 0x08, 0x00, 0x00]


def main() -> None:
    practice()

    parser = argparse.ArgumentParser(description="Ассемблер УВМ")
    parser.add_argument("input", help="Путь к исходному CSV-файлу с программой")
    parser.add_argument("output", help="Путь к выходному двоичному файлу (.bin)")
    parser.add_argument(
        "--test",
        action="store_true",
        help="Режим тестирования: вывод промежуточного представления и байтов",
    )
    args = parser.parse_args()

    program = parse_csv(args.input)
    asm_result = asm(program)

    with open(args.output, "wb") as f:
        f.write(asm_result)

    if args.test:
        print("Промежуточное представление (поля и значения):")
        for cmd in program:
            fields = [f"{k}={v}" for k, v in cmd.items() if k != "op"]
            print(f"{cmd['op']}: {', '.join(fields)}")

        print("\nМашинный код (байты):")
        for i in range(0, len(asm_result), 4):
            chunk = asm_result[i : i + 4]
            print(", ".join(f"0x{b:02X}" for b in chunk))

    print(f"\nРазмер двоичного файла: {len(asm_result)} bytes")


if __name__ == "__main__":
    main()