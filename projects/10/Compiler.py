import os, re

symbolList = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
keyList = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
]
temp = []


def dim(text, temp):
    for i in range(len(text)):
        if type(text[i]) == list:
            temp = dim(text[i], temp)
        else:
            temp.append(text[i])
    return temp


def elementText(text):
    text = dim(text, [])
    f = False
    for i in range(len(text)):
        if '"' in text[i]:
            t = text[i].split('"')
            text[i] = [t[0], '"', t[1]]
    text = dim(text, [])
    for i in range(len(text)):
        if text[i] == '"':
            if f:
                f = False
                te += " " + text[i]
                text[i] = te
            else:
                f = True
                te = ""
        if f:
            te += " " + text[i]
            text[i] = ""
    while "" in text:
        text.remove("")
    r = []
    for i in range(len(text)):
        if text[i][:3] == ' " ' and text[i][-1] == '"':
            text[i] = '"' + text[i][3:-2] + '"'
        elif (text[i][0:2] != '" ' and text[i][0:2] != '"') or text[i][-1] != '"':
            if text[i] in symbolList:
                continue
            else:
                for k in symbolList:
                    if k in text[i]:
                        t = text[i].split(k,1)
                        t = [t[0], k, t[1]]
                        text[i] = elementText(t)
                        break
    for i in r:
        text.remove(i)
    return dim(text, [])


def compilerText(text: list):
    r = []
    f = False
    for i in text:
        if "/*" in i:
            f = True
        if f:
            r.append(i)
        if "*/" in i:
            f = False
        if i[:2] == "//":
            r.append(i)
    for i in r:
        text.remove(i)
    for i in range(len(text)):
        if "//" in text[i]:
            text[i] = text[i].split("//")[0]
        text[i] = text[i].strip()
        text[i] = re.sub(r"\s+", " ", text[i])
    while "" in text:
        text.remove("")
    temp = []
    f = False
    for i in text:
        temp += elementText(i.split())
    t = dim(temp, [])
    while "" in t:
        t.remove("")

    xml = ["<tokens>"]
    for i in t:
        if i in keyList:
            xml.append(f"<keyword> {i} </keyword>")
        elif i in symbolList:
            if i == "&":
                xml.append(f"<symbol> &amp; </symbol>")
            elif i == ">":
                xml.append(f"<symbol> &gt; </symbol>")
            elif i == "<":
                xml.append(f"<symbol> &lt; </symbol>")
            else:
                xml.append(f"<symbol> {i} </symbol>")
        elif i.isdigit() and int(i) < 32768:
            xml.append(f"<integerConstant> {i} </integerConstant>")
        elif i[0] == i[-1] == '"':
            xml.append(f"<stringConstant> {i[1:-1]} </stringConstant>")
        else:
            xml.append(f"<identifier> {i} </identifier>")

    xml.append("</tokens>\n")
    return xml


def file(path):
    result = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            result.append(os.path.join(path, f))
        else:
            result += file(os.path.join(path, f))
    return result


if __name__ == "__main__":
    path = input("file or path:")
    if ".jack" in path:
        result = [path]
    else:
        if "C:\\Users\\joey2\\桌面\\nand2tetris\\" in path:
            result = file(path)
        else:
            result = file("C:\\Users\\joey2\\桌面\\nand2tetris\\" + path)
    for i in result:
        if ".jack" in i:
            f = open(i, "r")
            text = compilerText(f.readlines())
            f.close()
            f = open(i.split(".")[0] + "_T.xml", "w")
            f.write("\n".join(text))
            f.close()
