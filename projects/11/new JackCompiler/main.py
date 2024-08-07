import os.path, sys
from JackTokenizer import tokenizer, Token
from CompilationEngine import CompilationEngine, CompileError


def show(tokens: list[Token]) -> list[str]:
    n = tokens[0].line
    l = 0
    c = ""
    b: list[str] = []
    t = ""
    for i in tokens:
        if i.type == "symbol":
            if i.content == "{":
                l += 1
            elif i.content == "}":
                l -= 1
        if i.line > n:
            n += 1
            b.append(t)
            t = "    " * l
        if i.line > n:
            n += 1
            b.append(t)
            t = "    " * l
        while i.line > n:
            n += 1
        if i.line == n:
            if i.type in ["keyword", "identifier"] and c in ["keyword", "identifier", "string"]:
                t += f" {i.content}"
            elif i.type == "string":
                if c in ["keyword", "identifier"]:
                    t += f' "{i.content}"'
                else:
                    t += f'"{i.content}"'
            elif i.type == "symbol" and i.content in "+-*/><=&|":
                t += f" {i.content} "
            elif i.type == "symbol" and i.content == ",":
                t += ", "
            else:
                t += i.content
            c = i.type
    return b + ["\n"]


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
            debug = show(tokens)
            compiler = CompilationEngine(tokens)
            try:
                code = compiler.main()
            except CompileError as e:
                print(i, "line", e.token.line)
                print(e)
                debug += compiler.debug
                with open(i.split(".")[0] + "_error_log.txt", "w") as f:
                    f.write("\n".join(debug) + "\n")
                exit()
            with open(i.split(".")[0] + ".vm", "w") as f:
                f.write("\n".join(code) + "\n")
            print(f"Compile {filename} successfully")
