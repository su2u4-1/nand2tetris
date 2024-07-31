import os.path, sys
from JackTokenizer import tokenizer
from CompilationEngine import CompilationEngine


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("file or path:")
    path = os.path.abspath(path)

    if path.endswith(".jack"):
        files = [path]
    else:
        files = []
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                files.append(os.path.join(path, f))

    for i in files:
        if os.path.isfile(i) and i.endswith(".jack"):
            filename = i.split("\\")[-1]
            with open(i, "r") as f:
                source = f.readlines()
            tokens = tokenizer(source)
            compiler = CompilationEngine(tokens)
            code = compiler.main()
            for i in code:
                print(i)
            exit()
            with open(i.split(".")[0] + ".vm", "w") as f:
                f.write("\n".join(code) + "\n")
            print(f"Compile {filename} successfully")
