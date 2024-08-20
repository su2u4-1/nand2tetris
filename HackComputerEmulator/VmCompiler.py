import os, sys


def translator(text):
    r = []
    command = ["@256\nD=M\n@SP\nA=M\nM=D"]
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
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "sub":
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "neg":
            command.append(f"@SP\nA=M-1\nD=M\nD=D-M\nM=D-M")
        elif text[i][0] == "eq":
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})")
        elif text[i][0] == "gt":
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JLT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})")
        elif text[i][0] == "lt":
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JGT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})")
        elif text[i][0] == "and":
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=D&M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "or":
            command.append(f"@SP\nA=M-1\nD=M\nA=A-1\nD=D|M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "not":
            command.append(f"@SP\nA=M-1\nM=!M")
        elif text[i][0] == "push":
            if text[i][1] == "argument":
                command.append(f"@ARG\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "local":
                command.append(f"@LCL\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "this":
                command.append(f"@THIS\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "that":
                command.append(f"@THAT\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
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
                error += 1
                print("line", i, text[i], "\n------\n", command[-1], "\n------")
        elif text[i][0] == "pop":
            if text[i][1] == "argument":
                command.append(f"@ARG\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "local":
                command.append(f"@LCL\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "this":
                command.append(f"@THIS\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "that":
                command.append(f"@THAT\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
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
                error += 1
                print("line", i, text[i], "\n------\n", command[-1], "\n------")
        elif text[i][0] == "label":
            try:
                command.append(f"({functionname}${text[i][1]})")
            except:
                command.append(f"({name}${text[i][1]})")
        elif text[i][0] == "goto":
            command.append(f"@{name}${text[i][1]}\n0;JMP")
        elif text[i][0] == "if-goto":
            command.append(f"@SP\nM=M-1\nA=M\nD=M\n@{name}${text[i][1]}\nD;JNE")
        elif text[i][0] == "call":
            command.append(f"@return{i}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@SP\nD=M\n@{text[i][2]}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{text[i][1]}\n0;JMP\n(return{i})")
        elif text[i][0] == "function":
            functionname = text[i][1]
            command.append(f"({text[i][1]})\n@SP\nD=M\n@R13\nM=D\n@{text[i][2]}\nD=A\n@loop-{i}\nD;JEQ\n(loop{i})\n@SP\nM=M+1\nD=M\nA=M-1\nM=0\n@{text[i][2]}\nD=D-A\n@R13\nD=D-M\n@loop{i}\nD;JLT\n(loop-{i})")
        elif text[i][0] == "return":
            command.append(f"@LCL\nD=M\n@FRAME{i}\nM=D\n@5\nA=D-A\nD=M\n@RET\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n@FRAME{i}\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n@FRAME{i}\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n@FRAME{i}\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n@FRAME{i}\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n@RET\nA=M\n0;JMP")
        else:
            error += 1
            print("line", i, text[i], "\n------\n", command[-1], "\n------")
    command = "\n".join(command) + "\n(END)\n@END\n0;JMP\n"
    if error > 0:
        print(f"Error x{error}")
        exit()
    else:
        return command


def listAllFiles(path: str):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("file or path:")
    path = os.path.abspath(path)

    if path.endswith(".vm"):
        filename = path.split("\\")[-1]
        source = [f"name {filename.split('.')[0]}"]
        with open(path, "r") as f:
            source += f.readlines()
        code = translator(source)
        with open(path.split(".")[0] + ".asm", "w") as f:
            f.write(code)
        print(f"Compile {filename} successfully")
    else:
        p = listAllFiles(path)
        source = []
        filename = []
        for i in p:
            if i.endswith(".vm"):
                filename.append(i.split("\\")[-1])
                with open(i, "r") as f:
                    if filename[-1] == "Sys.vm":
                        source = ["name Sys"] + f.readlines() + source
                    else:
                        source += [f"name {filename[-1].split('.')[0]}"] + f.readlines()
        code = translator(source)
        with open(path.split(".")[0] + ".asm", "w") as f:
            f.write(code)
        for i in filename:
            print(f"Compile {i} successfully")
