import os, Preprocessor, Parser, Compiler


def listAllFiles(path: str):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
        else:
            result += listAllFiles(os.path.join(path, f))
    return result


if __name__ == "__main__":
    path = input("file or path:")
    if path.endswith(".jack"):
        result = [path]
    else:
        if "D:\\nand2tetris\\" in path:
            result = listAllFiles(path)
        else:
            result = listAllFiles("D:\\nand2tetris\\" + path)
    for i in result:
        if i.endswith(".jack"):
            f = open(i, "r")
            sourceCode = f.readlines()
            f.close()
            processedSourceCode = Preprocessor.main(sourceCode)
            vmcode = Compiler.main(processedSourceCode, Parser.main(processedSourceCode))
            f = open(i.split(".")[0] + ".vm", "w")
            f.write("\n".join(vmcode) + "\n")
            f.close()
