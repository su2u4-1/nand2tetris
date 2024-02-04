def translator(path):
    name = path.split("\\")[-1].split(".")[0]
    r = []
    command = ["@256\nD=M\n@SP\nA=M\nM=D"]
    err = False
    error = []
    f = open(path, "r")
    text = f.readlines()
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
        if text[i][0] == "add":
            command.append("@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "sub":
            command.append("@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "neg":
            command.append("@SP\nA=M-1\nD=M\nD=D-M\nM=D-M")
        elif text[i][0] == "eq":
            command.append(
                f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})"
            )
        elif text[i][0] == "gt":
            command.append(
                f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JLT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})"
            )
        elif text[i][0] == "lt":
            command.append(
                f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JGT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})"
            )
        elif text[i][0] == "and":
            command.append("@SP\nA=M-1\nD=M\nA=A-1\nD=D&M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "or":
            command.append("@SP\nA=M-1\nD=M\nA=A-1\nD=D|M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "not":
            command.append("@SP\nA=M-1\nM=!M")
        elif text[i][0] == "push":
            if text[i][1] == "argument":
                command.append(f"@ARG\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "local":
                command.append(f"@LCL\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "this":
                command.append(f"@THIS\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "that":
                command.append(f"@THAt\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "static":
                command.append(f"@{name}.{text[i][2]}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "pointer":
                if text[i][2] == "0":
                    command.append(f"@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
                elif text[i][2] == "1":
                    command.append(f"@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "temp":
                command.append(f"@R{5+int(text[i][2])}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "constant":
                command.append(f"@{text[i][2]}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D")
            else:
                err = True
                error.append(f"line {i} {text[i]}")
        elif text[i][0] == "pop":
            if text[i][1] == "argument":
                command.append(f"@ARG\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "local":
                command.append(f"@LCL\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "this":
                command.append(f"@THIS\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "that":
                command.append(f"@THAt\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "static":
                command.append(f"@SP\nM=M-1\nA=M\nD=M\n@{name}.{text[i][2]}\nM=D")
            elif text[i][1] == "pointer":
                if text[i][2] == "0":
                    command.append(f"@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D")
                elif text[i][2] == "1":
                    command.append(f"@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D")
            elif text[i][1] == "temp":
                command.append(f"@SP\nM=M-1\nA=M\nD=M\n@R{5+int(text[i][2])}\nM=D")
            else:
                err = True
                error.append(f"line {i} {text[i]}")
        elif text[i][0] == "label":
            command.append(f"({name}${text[i][1]})")
        elif text[i][0] == "goto":
            command.append(f"@{name}${text[i][1]}\n0;JMP")
        elif text[i][0] == "if-goto":
            command.append(f"@SP\nM=M-1\nA=M\nD=M\n@{name}${text[i][1]}\nD;JNE")
        else:
            err = True
            error.append(f"line {i} {text[i]}")
        # print(i, text[i], command[-1])
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
