nac = {"add":"@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D","sub":"@SP\nA=M-1\nD=M\nA=A-1\nD=D+M\n@SP\nM=M-1\nA=M-1\nM=D","neg":"@SP\nA=M-1\nD=M\nD=D-M\nM=D-M","eq":"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE\nD;JEQ\n@SP\nM=M-1\nA=M-1\nM=0\n@END\n0;JMP\n(TRUE)\n@SP\nM=M-1\nA=M-1\nM=-1\n(END)","gt":"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE\nD;JLT\n@SP\nM=M-1\nA=M-1\nM=0\n@END\n0;JMP\n(TRUE)\n@SP\nM=M-1\nA=M-1\nM=-1\n(END)","lt":"@SP\nA=M-1\nD=M\nA=A-1\nD=D-M\n@TRUE\nD;JGT\n@SP\nM=M-1\nA=M-1\nM=0\n@END\n0;JMP\n(TRUE)\n@SP\nM=M-1\nA=M-1\nM=-1\n(END)","and":"@SP\nA=M-1\nD=M\nA=A-1\nD=D&M\n@SP\nM=M-1\nA=M-1\nM=D","or":"@SP\nA=M-1\nD=M\nA=A-1\nD=D|M\n@SP\nM=M-1\nA=M-1\nM=D","not":"@SP\nA=M-1\nM=!M"}#not arg command
oac = {}#one arg command
tac0 = {}#two arg command
tac1 = {}

def translator(path):
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
                command.append(nac[text[i][0]])
            else:
                err = True
                error.append(f"line {i} {text[i]}")
        elif len(text[i]) == 2:
            if text[i][0] in oac:
                com = ""
                command.append()
            else:
                err = True
                error.append(f"line {i} {text[i]}")
        elif len(text[i]) == 3:
            if text[i][0] in tac0:
                com = ""
                command.append()
            else:
                err = True
                error.append(f"line {i} {text[i]}")
    print(text)
    f.close()
    path = path.split(".")
    if err:
        print(f"Error x{len(error)}")
        for i in error:
            print(i)
    else:
        f = open(path[0] + ".asm", "w")
        f.write()
        f.close()

if __name__ == "__main__":
    path = input("file path and name:")
    translator(path)