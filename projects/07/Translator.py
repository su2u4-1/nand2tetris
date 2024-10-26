# not arg command
nac = {
    "add": "@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D",
    "sub": "@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M-1\nM=D",
    "neg": "@SP\nA=M-1\nD=M\nD=D-M\nM=D-M",
    "eq": "@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{0}\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@END{0}\n0;JMP\n(TRUE{0})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{0})",
    "gt": "@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{0}\nD;JLT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{0}\n0;JMP\n(TRUE{0})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{0})",
    "lt": "@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{0}\nD;JGT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{0}\n0;JMP\n(TRUE{0})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{0})",
    "and": "@SP\nA=M-1\nD=M\nA=A-1\nD=D&M\n@SP\nM=M-1\nA=M-1\nM=D",
    "or": "@SP\nA=M-1\nD=M\nA=A-1\nD=D|M\n@SP\nM=M-1\nA=M-1\nM=D",
    "not": "@SP\nA=M-1\nM=!M",
}
# one arg command
oac = {}
# two arg command
tac0 = {
    "push": "@{0}\nD=M\n@{1}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D",
    "pop": "@{0}\nD=M\n@{1}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D",
}
tac1 = {"push": "@{0}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D", "pop": "@SP\nM=M-1\nA=M\nD=M\n@{0}\nM=D"}
t0 = {"argument": "ARG", "local": "LCL", "this": "THIS", "that": "THAT"}
t1 = {"static": "{0}.{1}", "pointer": "{2}", "temp": "R{3}"}
t2 = {"0": "THIS", "1": "THAT"}


def translator(path):
    name = path.split("\\")[-1].split(".")[0]
    r = []
    command = []
    err = False
    error = []
    f = open(path, "r")
    text = f.readlines()
    for i in text:
        if i[0:2] == "//" or i == "\n" or i == "":
            r.append(i)
    for i in r:
        text.remove(i)
    for i in range(len(text)):
        text[i] = text[i].split()
        if len(text[i]) == 1:
            if text[i][0] in nac:
                command.append(nac[text[i][0]].format(i))
            else:
                err = True
                error.append(f"line {i} {text[i]}")
        elif len(text[i]) == 2:
            if text[i][0] in oac:
                com = ""
                command.append(com)
            else:
                err = True
                error.append(f"line {i} {text[i]}")
        elif len(text[i]) == 3:
            if text[i][0] in tac0:
                if text[i][1] in t0:
                    command.append(tac0[text[i][0]].format(t0[text[i][1]], text[i][2]))
                elif text[i][1] in t1:
                    try:
                        command.append(
                            tac1[text[i][0]].format(t1[text[i][1]].format(name, text[i][2], t2[text[i][2]], 5 + int(text[i][2])))
                        )
                    except:
                        command.append(tac1[text[i][0]].format(t1[text[i][1]].format(name, text[i][2], 0, 5 + int(text[i][2]))))
                elif text[i][1] == "constant":
                    command.append(f"@{text[i][2]}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D")
                else:
                    err = True
                    error.append(f"line {i} {text[i]}")
            else:
                err = True
                error.append(f"line {i} {text[i]}")
    command.append("(END)\n@END\n0;JMP")
    command = "\n".join(command)
    f.close()
    if err:
        print(f"Error x{len(error)}")
        for i in error:
            print(i)
    else:
        path = path.split(".")
        f = open(path[0] + ".asm", "w")
        f.write(command)
        f.close()


if __name__ == "__main__":
    path = input("file path and name:")
    translator(path)
