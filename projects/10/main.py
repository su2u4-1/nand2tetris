import os, Preprocessor, Parser


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
        if "D:\\nand2tetris\\" in path:
            result = listAllFiles(path)
        else:
            result = listAllFiles("D:\\nand2tetris\\" + path)
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
