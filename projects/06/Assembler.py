import re

comp = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "A+D": "0000010", "D-A": "0010011", "A-D": "0000111", "D&A": "0000000", "A&D": "0000000", "D|A": "0010101", "A|D": "0010101", "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010", "M+D": "1000010", "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "M&D": "1000000", "D|M": "1010101", "M|D": "1010101"}
jump = {"Null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
symbol = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15, "SCREEN": 16384, "KBD": 24576}


def assemble(path):
    symbolList = []
    n1 = 0
    r = []
    err = False
    error = []
    pattern = re.compile(r"^Null$|^[MDA]+$")
    f = open(path, "r")
    text = f.readlines()
    for i in range(len(text)):
        text[i] = re.sub(r"\s+", "", text[i])
    for i in text:
        if i[0:2] == "//" or i == "\n" or i == "":
            r.append(i)
    for i in r:
        text.remove(i)
    r = []
    flag = False
    for i in range(len(text)):
        if text[i][0] == "(":
            if text[i][-1] == ")":
                r.append(text[i])
                t = text[i][1:-1]
                if t in symbol:
                    err = True
                    error.append(f"{text[i]}\nline {i+1} L command repeat label definition")
                else:
                    symbol[t] = n1
            else:
                err = True
                error.append(f"{text[i]}\nline {i+1} L command ')' not found")
        elif text[i][0] == "@":
            try:
                n = int(text[i][1:])
                if n >= 0:
                    bi = format(n, "b")
                    while len(bi) < 15:
                        bi = "0" + bi
                    text[i] = "0" + bi
                    n1 += 1
                else:
                    err = True
                    error.append(f"{text[i]}\nline {i+1} A command is negative number")
            except:
                n1 += 1
                symbolList.append(i)
        else:
            if "=" in text[i] and ";" in text[i]:
                text[i] = text[i].split("=")
                text[i][1] = text[i][1].split(";")
                flag = True
            elif "=" in text[i]:
                text[i] = text[i].split("=") + ["Null"]
                flag = True
            elif ";" in text[i]:
                text[i] = ["Null"] + text[i].split(";")
                flag = True
            else:
                err = True
                error.append(f"{text[i]}\nline {i+1} command '@', '=' or ';' not found")
            if flag:
                flag = False
                try:
                    t1 = comp[text[i][1]]
                except:
                    t1 = ""
                    err = True
                    error.append(f"{text[i]}\nline {i+1} C command comp")
                try:
                    t2 = jump[text[i][2]]
                except:
                    t2 = ""
                    err = True
                    error.append(f"{text[i]}\nline {i+1} C command jump")
                t0 = ["0", "0", "0"]
                if "M" in text[i][0]:
                    t0[2] = "1"
                if "D" in text[i][0]:
                    t0[1] = "1"
                if "A" in text[i][0]:
                    t0[0] = "1"
                if not bool(pattern.match(text[i][0])):
                    err = True
                    error.append(f"{text[i]}\nline {i+1} C command dest")
                t0 = t0[0] + t0[1] + t0[2]
                text[i] = "111" + t1 + t0 + t2
                n1 += 1
    n0 = 16
    for i in symbolList:
        t = text[i][1:]
        if t in symbol:
            text[i] = f"@{symbol[t]}"
        else:
            symbol[t] = n0
            text[i] = f"@{symbol[t]}"
            n0 += 1
        n = int(text[i][1:])
        if n >= 0:
            bi = format(n, "b")
            while len(bi) < 15:
                bi = "0" + bi
            text[i] = "0" + bi
            n1 += 1
        else:
            err = True
            error.append(f"{text[i]}\nline {i+1} A command is negative number")
    for i in r:
        text.remove(i)
    text = "\n".join(text)
    f.close()
    if err:
        print(f"Error x{len(error)}")
        for i in error:
            print(i)
    else:
        path = path.split(".")
        f = open(path[0] + ".hack", "w")
        f.write(text)
        f.close()


if __name__ == "__main__":
    path = input("file path and name:")
    assemble(path)
