import os, Preprocessor, Parser


def listAllFiles(path):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
        else:
            result += listAllFiles(os.path.join(path, f))
    return result


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
            xml = Parser.grammarAnalyzer(Preprocessor.Txml(processedSourceCode))
            f.close()
            f = open(i.split(".")[0] + "_M.xml", "w")
            f.write("\n".join(xml))
            f.close()
