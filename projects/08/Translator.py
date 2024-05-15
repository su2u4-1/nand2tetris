import os


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
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "sub":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "neg":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nD=D-M\nM=D-M")
        elif text[i][0] == "eq":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})")
        elif text[i][0] == "gt":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JLT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})")
        elif text[i][0] == "lt":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE{i}\nD;JGT\n@SP\nM=M-1\nA=M-1\nM=0\n@END{i}\n0;JMP\n(TRUE{i})\n@SP\nM=M-1\nA=M-1\nM=-1\n(END{i})")
        elif text[i][0] == "and":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=D&M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "or":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nD=M\nA=A-1\nD=D|M\n@SP\nM=M-1\nA=M-1\nM=D")
        elif text[i][0] == "not":
            command.append(f"//{text[i]}\n@SP\nA=M-1\nM=!M")
        elif text[i][0] == "push":
            if text[i][1] == "argument":
                command.append(f"//{text[i]}\n@ARG\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "local":
                command.append(f"//{text[i]}\n@LCL\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "this":
                command.append(f"//{text[i]}\n@THIS\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "that":
                command.append(f"//{text[i]}\n@THAT\nD=M\n@{text[i][2]}\nA=D+A\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "static":
                command.append(f"//{text[i]}\n@{name}.{text[i][2]}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "pointer":
                if text[i][2] == "0":
                    command.append(f"//{text[i]}\n@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
                elif text[i][2] == "1":
                    command.append(f"//{text[i]}\n@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "temp":
                command.append(f"//{text[i]}\n@R{5+int(text[i][2])}\nD=M\n@SP\nM=M+1\nA=M-1\nM=D")
            elif text[i][1] == "constant":
                command.append(f"//{text[i]}\n@{text[i][2]}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D")
            else:
                error += 1
                print("line", i, text[i], "\n------\n", command[-1], "\n------")
        elif text[i][0] == "pop":
            if text[i][1] == "argument":
                command.append(f"//{text[i]}\n@ARG\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "local":
                command.append(f"//{text[i]}\n@LCL\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "this":
                command.append(f"//{text[i]}\n@THIS\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "that":
                command.append(f"//{text[i]}\n@THAT\nD=M\n@{text[i][2]}\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D")
            elif text[i][1] == "static":
                command.append(f"//{text[i]}\n@SP\nM=M-1\nA=M\nD=M\n@{name}.{text[i][2]}\nM=D")
            elif text[i][1] == "pointer":
                if text[i][2] == "0":
                    command.append(f"//{text[i]}\n@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D")
                elif text[i][2] == "1":
                    command.append(f"//{text[i]}\n@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D")
            elif text[i][1] == "temp":
                command.append(f"//{text[i]}\n@SP\nM=M-1\nA=M\nD=M\n@R{5+int(text[i][2])}\nM=D")
            else:
                error += 1
                print("line", i, text[i], "\n------\n", command[-1], "\n------")
        elif text[i][0] == "label":
            command.append(f"//{text[i]}\n({functionname}${text[i][1]})")
        elif text[i][0] == "goto":
            command.append(f"//{text[i]}\n@{name}${text[i][1]}\n0;JMP")
        elif text[i][0] == "if-goto":
            command.append(f"//{text[i]}\n@SP\nM=M-1\nA=M\nD=M\n@{name}${text[i][1]}\nD;JNE")
        elif text[i][0] == "call":
            command.append(f"//{text[i]}\n@return{i}\nD=A\n@SP\nM=M+1\nA=M-1\nM=D\n@LCL\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@ARG\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THIS\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@THAT\nD=M\n@SP\nM=M+1\nA=M-1\nM=D\n@SP\nD=M\n@{text[i][2]}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{text[i][1]}\n0;JMP\n(return{i})")
        elif text[i][0] == "function":
            functionname = text[i][1]
            command.append(f"//{text[i]}\n({text[i][1]})\n@SP\nD=M\n@R13\nM=D\n@{text[i][2]}\nD=A\n@loop-{i}\nD;JEQ\n(loop{i})\n@SP\nM=M+1\nD=M\nA=M-1\nM=0\n@{text[i][2]}\nD=D-A\n@R13\nD=D-M\n@loop{i}\nD;JLT\n(loop-{i})")
        elif text[i][0] == "return":
            command.append(f"//{text[i]}\n@LCL\nD=M\n@FRAME{i}\nM=D\n@5\nA=D-A\nD=M\n@RET\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n@FRAME{i}\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n@FRAME{i}\nD=M\n@2\nA=D-A\nD=M\n@THIS\nM=D\n@FRAME{i}\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n@FRAME{i}\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n@RET\nA=M\n0;JMP")
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
        text = f.readlines()
        f.close()
        command = translator(text)
        path = path.split(".")
        f = open(path[0] + ".asm", "w")
        f.write(command)
        f.close()
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
        f = open(f"{path}\\{name}.asm", "w")
        f.write(command)
        f.close()


if __name__ == "__main__":
    path = input("file path and name:")
    main(path)
