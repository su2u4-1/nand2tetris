import os, sys
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
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("file or path:")
    dir = os.getcwd()

    if dir not in path:
        path = dir + "\\" + path
    if path.endswith(".jack"):
        result = [path]
    else:
        result = listAllFiles(path)

    for i in result:
        if i.endswith(".jack"):
            with open(i, "r") as f:
                source = f.readlines()
            tokens = tokenizer(source)
            compiler = CompilationEngine(tokens)
            xml = compiler.main()
            with open(i.split(".")[0] + "_M.xml", "w") as f:
                f.write("\n".join(xml))
