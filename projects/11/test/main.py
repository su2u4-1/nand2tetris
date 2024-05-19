import os, sys, traceback
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
            try:
                xml = compiler.main()
            except CompileError as e:
                _, _, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback)
                print(e.m())
                op = input("Enter any to close, enter 'show' to display all tokens:")
                if op == "show":
                    for i in tokens:
                        print(i)
                exit()
            with open(i.split(".")[0] + "_M.xml", "w") as f:
                f.write("\n".join(xml))
