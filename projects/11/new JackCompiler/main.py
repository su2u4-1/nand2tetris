import os.path, sys
from JackTokenizer import tokenizer, Token
from CompilationEngine import CompilationEngine


def show(tokens: list[Token]) -> None:
    n = tokens[0].line
    l = 0
    c = ""
    for i in tokens:
        if i.type == "symbol":
            if i.content == "{":
                l += 1
            elif i.content == "}":
                l -= 1
        if i.line > n:
            n += 1
            print("\n" + "    " * l, end="")
        if i.line > n:
            n += 1
            print("\n" + "    " * l, end="")
        while i.line > n:
            n += 1
        if i.line == n:
            if i.type in ["keyword", "identifier"] and c in ["keyword", "identifier", "string"]:
                print(f" {i.content}", end="")
            elif i.type == "string":
                if c in ["keyword", "identifier"]:
                    print(f' "{i.content}"', end="")
                else:
                    print(f'"{i.content}"', end="")
            elif i.type == "symbol" and i.content in "+-*/><=&|":
                print(f" {i.content} ", end="")
            elif i.type == "symbol" and i.content == ",":
                print(", ", end="")
            else:
                print(i.content, end="")
            c = i.type


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("file or path:")
    path = os.path.abspath(path)

    if path.endswith(".jack"):
        files = [path]
    else:
        files: list[str] = []
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                files.append(os.path.join(path, f))

    for i in files:
        if os.path.isfile(i) and i.endswith(".jack"):
            filename = i.split("\\")[-1]
            with open(i, "r") as f:
                source = f.readlines()
            tokens = tokenizer(source)
            show(tokens)
            compiler = CompilationEngine(tokens)
            code = compiler.main()
            exit()
            with open(i.split(".")[0] + ".vm", "w") as f:
                f.write("\n".join(code) + "\n")
            print(f"Compile {filename} successfully")
