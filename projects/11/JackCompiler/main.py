import os, sys, traceback
from JackTokenizer import *
from CompilationEngine import *


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

    if path.endswith(".jack"):
        result = [path]
    else:
        result = listAllFiles(path)

    for i in result:
        if i.endswith(".jack"):
            filename = i.split('\\')[-1]
            with open(i, "r") as f:
                source = f.readlines()
            tokens = tokenizer(source)
            compiler = CompilationEngine(tokens)
            try:
                code = compiler.main()
            except CompileError as e:
                print("error file:", filename)
                _, _, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback)
                print(e.m())
                op = input("Enter any to close, enter 'show' to display all tokens:")
                if op == "show":
                    for i in range(len(tokens)):
                        print(i, tokens[i])
                exit()
            with open(i.split(".")[0] + ".vm", "w") as f:
                f.write("\n".join(code) + "\n")
            print(f"Compile {filename} successfully")
