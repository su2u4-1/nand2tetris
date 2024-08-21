import sys
import os.path

import pygame

import JackCompiler.main
import VmCompiler
import AsmAssembler


def compile(path: str) -> list[str]:
    if os.path.isfile(path):
        if path.endswith(".jack"):
            vm_code = JackCompiler.main.main(path, "return")
            asm_code = VmCompiler.translator([f"name {path.split('\\')[-1].split(".")[0]}"] + vm_code)
            binary = AsmAssembler.assemble(asm_code)
            return binary
        elif path.endswith(".vm"):
            with open(path, "r") as f:
                vm_code = f.readlines()
            asm_code = VmCompiler.translator([f"name {path.split('\\')[-1].split(".")[0]}"] + vm_code)
            binary = AsmAssembler.assemble(asm_code)
            return binary
        elif path.endswith(".asm"):
            binary = AsmAssembler.main([path], "return")
            return binary
        elif path.endswith(".hack"):
            with open(path, "r") as f:
                binary = f.readlines()
            return binary
        else:
            print(f"{path.split(".")[-1]} is the wrong file type")
            exit()
    else:
        print(f"{path} is not a file")


def main(binary: list[str]) -> int:
    pygame.init()
    W, H = 512, 256
    pygame.display.set_caption("Hack Computer Emulator")
    screen = pygame.display.set_mode((W, H), pygame.SHOWN)
    clock = pygame.time.Clock()
    index = 0
    D_register = 0
    A_register = 0
    memory = [0 for _ in range(24577)]
    screen.fill((255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 1
            elif event.type == pygame.KEYDOWN:
                c = event.unicode
                if len(c) == 1:
                    memory[24576] = ord(c)

        if index >= len(binary):
            pygame.quit()
            return 0
        tl = [index, binary[index]]
        instruction = binary[index]
        if instruction[0] == "0":
            A_register = int("0b" + instruction, base=2)
            if A_register > 32767 or A_register < -32768:
                pygame.quit()
                return 2
            index += 1
        else:
            comp = instruction[3:10]
            dest = instruction[10:13]
            jump = instruction[13:16]
            t0 = D_register
            if comp[0] == "0":
                t1 = A_register
            else:
                t1 = memory[A_register]
            if comp[1] == "1":
                t0 = 0
            if comp[2] == "1":
                t0 = -t0 - 1
            if comp[3] == "1":
                t1 = 0
            if comp[4] == "1":
                t1 = -t1 - 1
            if comp[5] == "0":
                result = (t0 & 0xFFFF) & (t1 & 0xFFFF)
                if result >= 0x8000:
                    result -= 0x10000
            else:
                result = t0 + t1
            if comp[6] == "1":
                result = -result - 1
            if result > 32767 or result < -32768:
                return 3
            if dest[2] == "1":
                memory[A_register] = result
            if dest[0] == "1":
                A_register = result
            if dest[1] == "1":
                D_register = result
            if (jump[0] == "1" and result < 0) or (jump[1] == "1" and result == 0) or (jump[2] == "1" and result > 0):
                index = A_register
                if index > 24576 or index < 0:
                    return 4
            else:
                index += 1

        # TODO
        for i in range(256):
            for j in range(32):
                t = memory[16384 + j]
                t = format(t, "016b")
                for k in range(16):
                    if t[k] == "1":
                        screen.set_at((i, j * 16 + k), (0, 0, 0))
                    else:
                        screen.set_at((i, j * 16 + k), (255, 255, 255))

        pygame.display.update()
        clock.tick(60)

        log.append(str([memory[:10], memory[16384:16394], memory[24576], A_register, D_register] + tl))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("file path:")
    path = os.path.abspath(path)

    binary = compile(path)
    for i in binary:
        print(i)
    log: list[str] = []
    n = main(binary)
    with open("log", "w+") as f:
        for i in log:
            f.write(i + "\n")
    print("end code:", n)
    """
    error code:
    0: normal
    1: closed manually
    2: The value set by A command is out of range
    3: The calculation result exceeds the 16-bit range
    4: Memory access out of range
    """
