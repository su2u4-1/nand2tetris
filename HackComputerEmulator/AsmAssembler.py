import re, sys, os

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "A+D": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "A&D": "0000000",
    "D|A": "0010101",
    "A|D": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "M+D": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "M&D": "1000000",
    "D|M": "1010101",
    "M|D": "1010101",
}
jump = {"Null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
symbol = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
}


def listAllFiles(path: str):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
    return result


def assemble(source: list[str], filename):
    symbolList = []
    n1 = 0
    r = []
    err = False
    error = []
    pattern = re.compile(r"^Null$|^[MDA]+$")
    for i in range(len(source)):
        source[i] = re.sub(r"\s+", "", source[i])
    for i in source:
        if i[0:2] == "//" or i == "\n" or i == "":
            r.append(i)
    for i in r:
        source.remove(i)
    r = []
    flag = False
    for i in range(len(source)):
        if source[i][0] == "(":
            if source[i][-1] == ")":
                r.append(source[i])
                t = source[i][1:-1]
                if t in symbol:
                    err = True
                    error.append(f"{source[i]}\nline {i+1} L command repeat label definition")
                else:
                    symbol[t] = n1
            else:
                err = True
                error.append(f"{source[i]}\nline {i+1} L command ')' not found")
        elif source[i][0] == "@":
            try:
                n = int(source[i][1:])
                if n >= 0:
                    bi = format(n, "b")
                    while len(bi) < 15:
                        bi = "0" + bi
                    source[i] = "0" + bi
                    n1 += 1
                else:
                    err = True
                    error.append(f"{source[i]}\nline {i+1} A command is negative number")
            except:
                n1 += 1
                symbolList.append(i)
        else:
            if "=" in source[i] and ";" in source[i]:
                source[i] = source[i].split("=")
                source[i][1] = source[i][1].split(";")
                flag = True
            elif "=" in source[i]:
                source[i] = source[i].split("=") + ["Null"]
                flag = True
            elif ";" in source[i]:
                source[i] = ["Null"] + source[i].split(";")
                flag = True
            else:
                err = True
                error.append(f"{source[i]}\nline {i+1} command '@', '=' or ';' not found")
            if flag:
                flag = False
                try:
                    t1 = comp[source[i][1]]
                except:
                    t1 = ""
                    err = True
                    error.append(f"{source[i]}\nline {i+1} C command comp")
                try:
                    t2 = jump[source[i][2]]
                except:
                    t2 = ""
                    err = True
                    error.append(f"{source[i]}\nline {i+1} C command jump")
                t0 = ["0", "0", "0"]
                if "M" in source[i][0]:
                    t0[2] = "1"
                if "D" in source[i][0]:
                    t0[1] = "1"
                if "A" in source[i][0]:
                    t0[0] = "1"
                if not bool(pattern.match(source[i][0])):
                    err = True
                    error.append(f"{source[i]}\nline {i+1} C command dest")
                t0 = t0[0] + t0[1] + t0[2]
                source[i] = "111" + t1 + t0 + t2
                n1 += 1
    n0 = 16
    for i in symbolList:
        t = source[i][1:]
        if t in symbol:
            source[i] = f"@{symbol[t]}"
        else:
            symbol[t] = n0
            source[i] = f"@{symbol[t]}"
            n0 += 1
        n = int(source[i][1:])
        if n >= 0:
            bi = format(n, "b")
            while len(bi) < 15:
                bi = "0" + bi
            source[i] = "0" + bi
            n1 += 1
        else:
            err = True
            error.append(f"{source[i]}\nline {i+1} A command is negative number")
    for i in r:
        source.remove(i)
    if err:
        print("error file:", filename)
        print(f"Error x{len(error)}")
        for i in error:
            print(i)
        exit()
    else:
        return source


def main(paths, mode="default"):
    for i in paths:
        if i.endswith(".asm"):
            with open(i, "r") as f:
                source = f.readlines()
            filename = i.split("\\")[-1]
            binary = assemble(source, filename)
            if mode == "default":
                with open(i.split(".")[0] + ".hack", "w") as f:
                    f.write("\n".join(binary))
                    print(f"Assembled {filename} successfully")
            elif mode == "return":
                return binary


if __name__ == "__main__":
    if len(sys.argv) > 1:
        i = sys.argv[1]
    else:
        i = input("file or path:")
    i = os.path.abspath(i)

    if i.endswith(".asm"):
        paths = [i]
    else:
        paths = listAllFiles(i)

    main(paths)
