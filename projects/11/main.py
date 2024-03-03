import os, Preprocessor, Parser, Compiler


def listAllFiles(path: str):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
        else:
            result += listAllFiles(os.path.join(path, f))
    return result


def xml(code: list):
    for i in range(len(code)):
        code[i] = f"<{code[i][1]}> {code[i][0]} </{code[i][1]}>"
    return code


if __name__ == "__main__":
    path = input("file or path:")
    if ".jack" in path:
        result = [path]
    else:
        if "C:\\Users\\joey2\\桌面\\nand2tetris\\" in path:
            result = listAllFiles(path)
        else:
            result = listAllFiles("C:\\Users\\joey2\\桌面\\nand2tetris\\" + path)
    for i in result:
        if ".jack" in i:
            f = open(i, "r")
            sourceCode = f.readlines()
            processedSourceCode = Preprocessor.preprocessor(sourceCode)
            tl = processedSourceCode.copy()
            f.close()
            f = open(i.split(".")[0] + "_T.xml", "w")
            f.write("\n".join(["<tokens>"] + xml(tl) + ["</tokens>\n"]))
            f.close()
            xmlcode = Parser.grammarAnalyzer(processedSourceCode)
            xmlcode[-1] += "\n"
            f = open(i.split(".")[0] + "_M.xml", "w")
            f.write("\n".join(xmlcode))
            f.close()
            vmCode = Compiler.compiler(processedSourceCode)
            # f = open(i.split(".")[0] + ".vm", "w")
            # f.write("\n".join(xml))
            # f.close()
