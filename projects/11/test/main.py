import os
from JackTokenizer import *
from CompilationEngine import *


def listAllFiles(path: str):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
        else:
            result += listAllFiles(os.path.join(path, f))
    return result


def turn_xml(code: list):
    for i in range(len(code)):
        code[i] = f"<{code[i][1]}> {code[i][0]} </{code[i][1]}>"
    return code


if __name__ == "__main__":
    path = input("file or path:")
    if path.endswith(".jack"):
        result = [path]
    else:
        if "C:\\Users\\joey2\\code\\nand2tetris\\" in path:
            result = listAllFiles(path)
        else:
            result = listAllFiles("C:\\Users\\joey2\\code\\nand2tetris\\" + path)
    for i in result:
        if i.endswith(".jack"):
            with open(i, "r") as f:
                source = f.readlines()
            compiler = CompilationEngine()
            tokens = tokenizer(source)
            exit()
            xml = compiler.main(tokens)
            with open(i.split(".")[0] + "_M.xml", "w") as f:
                f.write("\n".join(xml))
