import os, re

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


def assembler(path):
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
                    if len(bi) > 15:
                        err = True
                        error.append(f"{text[i]}\nline {i+1} A command is too lone")
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
            if len(bi) > 15:
                err = True
                error.append(f"{text[i]}\nline {i+1} A command is too lone")
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


def translator(text):
    r = []
    command = ["@256\nD=A\n@SP\nM=D"]
    error = 0
    for i in text:
        if i == "" or i == "\n":
            r.append(i)
        elif i.split()[0] == "//":
            r.append(i)
    for i in r:
        text.remove(i)
    for i in range(len(text)):
        text[i] = text[i].split()
        while "//" in text[i]:
            text[i].pop()
    if [] in text:
        text.remove([])
    for i in range(len(text)):
        if text[i][0] == "name":
            name = text[i][1]
        elif text[i][0] == "add":
            command.append(f"//{text[i]}\n" + "@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "sub":
            command.append(f"//{text[i]}\n" + "@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "neg":
            command.append(f"//{text[i]}\n" + "@SP\nA=M-1\nD=M\nD=D-M\nM=D-M")
        elif text[i][0] == "eq":
            command.append(
                f"//{text[i]}\n"
                + f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})"
            )
        elif text[i][0] == "gt":
            command.append(
                f"//{text[i]}\n"
                + f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JLT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})"
            )
        elif text[i][0] == "lt":
            command.append(
                f"//{text[i]}\n"
                + f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JGT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})"
            )
        elif text[i][0] == "and":
            command.append(f"//{text[i]}\n" + "@SP\nA=M-1\nD=M\nA=A-1\nD=D&M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "or":
            command.append(f"//{text[i]}\n" + "@SP\nA=M-1\nD=M\nA=A-1\nD=D|M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "not":
            command.append(f"//{text[i]}\n" + "@SP\nA=M-1\nM=!M")
        elif text[i][0] == "push":
            if text[i][1] == "argument":
                command.append(f"//{text[i]}\n" + f"@ARG\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "local":
                command.append(f"//{text[i]}\n" + f"@LCL\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "this":
                command.append(f"//{text[i]}\n" + f"@THIS\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "that":
                command.append(f"//{text[i]}\n" + f"@THAT\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "static":
                command.append(f"//{text[i]}\n" + f"@{name}.{text[i][2]}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "pointer":
                if text[i][2] == "0":
                    command.append(f"//{text[i]}\n" + f"@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
                elif text[i][2] == "1":
                    command.append(f"//{text[i]}\n" + f"@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "temp":
                command.append(f"//{text[i]}\n" + f"@R{5+int(text[i][2])}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "constant":
                command.append(f"//{text[i]}\n" + f"@{text[i][2]}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D")
            else:
                error += 1
                print("line", i, text[i], "\n------\n", command[-1], "\n------")
        elif text[i][0] == "pop":
            if text[i][1] == "argument":
                command.append(f"//{text[i]}\n" + f"@ARG\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "local":
                command.append(f"//{text[i]}\n" + f"@LCL\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "this":
                command.append(f"//{text[i]}\n" + f"@THIS\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "that":
                command.append(f"//{text[i]}\n" + f"@THAT\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "static":
                command.append(f"//{text[i]}\n" + f"@SP\nM=M-1\nA=M\nD=M\n@{name}.{text[i][2]}\nM=D")
            elif text[i][1] == "pointer":
                if text[i][2] == "0":
                    command.append(f"//{text[i]}\n" + f"@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D")
                elif text[i][2] == "1":
                    command.append(f"//{text[i]}\n" + f"@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D")
            elif text[i][1] == "temp":
                command.append(f"//{text[i]}\n" + f"@SP\nM=M-1\nA=M\nD=M\n@R{5+int(text[i][2])}\nM=D")
            else:
                error += 1
                print("line", i, text[i], "\n------\n", command[-1], "\n------")
        elif text[i][0] == "label":
            command.append(f"//{text[i]}\n" + f"({functionname}${text[i][1]})")
        elif text[i][0] == "goto":
            command.append(f"//{text[i]}\n" + f"@{name}${text[i][1]}\n0;JMP")
        elif text[i][0] == "if-goto":
            command.append(f"//{text[i]}\n" + f"@SP\nM=M-1\nA=M\nD=M\n@{name}${text[i][1]}\nD;JNE")
        elif text[i][0] == "call":
            command.append(
                f"//{text[i]}\n"
                + f"@return{i}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@SP\nD=M\n@{text[i][2]}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{text[i][1]}\n0;JMP\n(return{i})"
            )
        elif text[i][0] == "function":
            functionname = text[i][1]
            command.append(
                f"//{text[i]}\n"
                + f"({text[i][1]})\n@SP\nD=M\n@R13\nM=D\n@{text[i][2]}\nD=A\n@loop-{i}\nD;JEQ\n(loop{i})\n@SP\nM=M+1\nD=M\nA=M-1\nM=0\n@{text[i][2]}\nD=D-A\n@R13\nD=D-M\n@loop{i}\nD;JLT\n(loop-{i})"
            )
        elif text[i][0] == "return":
            command.append(
                f"//{text[i]}\n"
                + f"@LCL\nD=M\n@FRAME{i}\nM=D\n@5\nA=D-A\nD=M\n@RET\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n@FRAME{i}\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n@FRAME{i}\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n@FRAME{i}\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n@FRAME{i}\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n@RET\nA=M\n0;JMP"
            )
        else:
            error += 1
            print("line", i, text[i], "\n------\n", command[-1], "\n------")
    command = "\n".join(command)
    if error > 0:
        print(f"Error x{error}")
        exit()
    else:
        return command


def file(path):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
        else:
            result += file(os.path.join(path, f))
    return result


def main(path):
    if ".vm" in path:
        name = path.split("\\")[-1].split(".")[0]
        text = [f"name {name}"]
        f = open(path, "r")
        text += f.readlines()
        f.close()
        command = translator(text)
        path = path.split(".")
        asmpath = path[0] + ".asm"
    else:
        if "C:\\Users\\joey2\\桌面\\nand2tetris\\" in path:
            result = file(path)
        else:
            result = file("C:\\Users\\joey2\\桌面\\nand2tetris\\" + path)
        text = []
        for i in result:
            if "Sys.vm" in i:
                text.append(f"name Sys")
                f = open(i, "r")
                text += f.readlines()
                f.close()
        for i in result:
            if "Sys.vm" not in i and ".vm" in i:
                name = i.split("\\")[-1].split(".")[0]
                text.append(f"name {name}")
                f = open(i, "r")
                text += f.readlines()
                f.close()
        command = translator(text)
        name = path.split("\\")[-1]
        asmpath = f"{path}\\{name}.asm"
    f = open(asmpath, "w")
    f.write(command)
    f.close()
    assembler(asmpath)


path = input("file path and name:")
main(path)
