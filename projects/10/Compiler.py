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
l = ["<symbol> + </symbol>","<symbol> - </symbol>","<symbol> * </symbol>","<symbol> / </symbol>","<symbol> & </symbol>","<symbol> | </symbol>","<symbol> > </symbol>","<symbol> < </symbol>","<symbol> = </symbol>"]
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
        if text[i].startswith(' " ') and text[i].endswith('"'):
            text[i] = '"' + text[i][3:-2] + '"'
        elif (text[i][0:2] != ' "' and text[i][0] != '"') or text[i][-1] != '"':
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
    for i in range(len(text)):
        text[i] = text[i].strip()
        text[i] = re.sub(r"\s+", " ", text[i])
    for i in text:
        if i.startswith("/*"):
            f = True
        if f:
            r.append(i)
        if i.endswith("*/"):
            f = False
        if i.startswith("//"):
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
        elif not i[0].isdigit():
            xml.append(f"<identifier> {i} </identifier>")
        else:
            print("error:", i)

    xml.append("</tokens>\n")
    return xml


def compiler(text: list):
    text.remove("<tokens>")
    text.remove("</tokens>\n")
    xml = ["<class>"]
    Class = compileClass(text)
    for i in Class:
        xml.append("  "+i)
    xml.append("</class>")
    return xml


def compileClass(text:list):
    xml = ["<keyword> class </keyword>"]
    text.remove("<keyword> class </keyword>")
    for i in text:
        if i.startswith("<identifier> ") and i.endswith(" </identifier>"):
            xml.append(i)
            text.remove(i)
            break
    f0 = False
    ClassVarDec = []
    for i in text:
        if i == "<keyword> static </keyword>" or i == "<keyword> field </keyword>":
            f0 = True
        if f0:
            ClassVarDec.append(i)
        if i == "<symbol> ; </symbol>":
            f0 = False
        if i == "<keyword> constructor </keyword>" or i == "<keyword> method </keyword>" or i == "<keyword> function </keyword>":
            break
    xml.append("<classVarDec>")
    for i in ClassVarDec:
        xml.append("  "+i)
    xml.append("</classVarDec>")
    text1 = []
    SubroutineStart = -1
    f1 = False
    b = 0
    for i in text:
        if i == "<symbol> { </symbol>":
            b += 1
        if i == "<symbol> } </symbol>":
            b -= 1
        if i == "<keyword> constructor </keyword>" or i == "<keyword> method </keyword>" or i == "<keyword> function </keyword>":
            f1 = True
            SubroutineStart = b+1
        if f1:
            text1.append(i)
        if b == SubroutineStart and i == "<symbol> } </symbol>":
            f1 = False
            Subroutine = compileSubroutine(text1)
            xml.append("<classVarDec>")
            for j in Subroutine:
                xml.append("  "+j)
            xml.append("</classVarDec>")
    return xml


def compileSubroutine(text:list):
    xml = []
    f = False
    ParameterList = []
    for i in text:
        if i == "<symbol> ) </symbol>":
            f = False
            break
        if f:
            ParameterList.append(i)
        if i == "<symbol> ( </symbol>":
            f = True
    xml.append("<parameterList>")
    for i in ParameterList:
        xml.append("  "+i)
        text.remove(i)
    xml.append("</parameterList>")
    text.remove("<symbol> ( </symbol>")
    text.remove("<symbol> ) </symbol>")
    if text[-1] == "<symbol> } </symbol>":
        text.pop()
    SubroutineBody = compileSubroutineBody(text)
    xml.append("<subroutineBody>")
    for i in SubroutineBody:
        xml.append("  "+i)
    xml.append("</subroutineBody>")
    return xml


def compileSubroutineBody(text:list):
    xml = []
    t = []
    f = False
    for i in text:
        if i == "<keyword> var </keyword>":
            f = True
            VarDec = []
        if f:
            VarDec.append(i)
            t.append(i)
        if i == "<keyword> ; </keyword>":
            f = False
            xml.append("<varDec>")
            for j in VarDec:
                xml.append("  "+j)
            xml.append("</VarDec>")
        if not f and i != "<keyword> var </keyword>" and i != "<symbol> { </symbol>":
            break
    for i in t:
        text.remove(i)
    if text[-1] == "<symbol> } </symbol>":
        text.pop()
    Statements = compileStatements(text)
    xml.append("<statements>")
    for i in Statements:
        xml.append("  "+i)
    xml.append("</statements>")
    return xml


def compileStatements(text:list):
    xml = []
    b = 0
    f = [False,False,False,False,False,False]
    whileStart = -1
    ifStart = -1
    elseStart = -1
    te = [[],[],[],[],[]]
    for i in range(len(text)):
        if text[i] == "<symbol> { </symbol>":
            b += 1
        if text[i] == "<symbol> } </symbol>":
            b -= 1
        if text[i] == "<keyword> do </keyword>":
            f[0] = True
        elif text[i] == "<keyword> let </keyword>":
            f[1] = True
        elif text[i] == "<keyword> while </keyword>":
            f[2] = True
            whileStart = b+1
        elif text[i] == "<keyword> return </keyword>":
            f[3] = True
        elif text[i] == "<keyword> if </keyword>":
            f[4] = True
            ifStart = b+1
        elif text[i] == "<keyword> else </keyword>":
            f[5] = True
            elseStart = b+1
        if f[0]:
            te[0].append(text[i])
        elif f[1]:
            te[1].append(text[i])
        elif f[2]:
            te[2].append(text[i])
        elif f[3]:
            te[3].append(text[i])
        elif f[4]:
            te[4].append(text[i])
        elif f[5]:
            te[4].append(text[i])
        if text[i] == "<symbol> ; </symbol>":
            if f[0]:
                f[0] = False
                xml.append("<doStatement>")
                for j in te[0]:
                    xml.append("  "+j)
                xml.append("</doStatement>")
                te[0] = []
            if f[1]:
                f[1] = False
                Lat = compileLet(te[1])
                xml.append("<letStatement>")
                for j in Lat:
                    xml.append("  "+j)
                xml.append("</letStatement>")
                te[1] = []
            if f[3]:
                f[3] = False
                Return = compileReturn(te[2])
                xml.append("<returnStatement>")
                for j in Return:
                    xml.append("  "+j)
                xml.append("</returnStatement>")
                te[3] = []
        if text[i] == "<symbol> } </symbol>":
            if b == whileStart:
                f[2] = False
                While = compileWhile(te[3])
                xml.append("<whileStatement>")
                for j in While:
                    xml.append("  "+j)
                xml.append("</whileStatement>")
                te[2] = []
            elif b == ifStart:
                f[4] = False
                if text[i+1] != "<keyword> else </keyword>":
                    If = compileIf(te[4])
                    xml.append("<ifStatement>")
                    for j in If:
                        xml.append("  "+j)
                    xml.append("</ifStatement>")
                    te[4] = []
            elif b == elseStart:
                f[5] = False
                If = compileIf(te[4])
                xml.append("<ifStatements>")
                for j in If:
                    xml.append("  "+j)
                xml.append("</ifStatements>")
                te[4] = []
    return xml


def compileLet(text:list):
    xml = []
    b = 0
    f0 = False
    text0 = []
    for i in text:
        if text[i] == "<symbol> [ </symbol>":
            b += 1
        if text[i] == "<symbol> ] </symbol>":
            b -= 1
        if i == "<symbol> [ </symbol>" and b == 1:
            f0 = True
            start = b
        if f0:
            text0.append(i)
        else:
            xml.append(i)
        if i == "<symbol> ] </symbol>" and b == start:
            f0 = False
            t0 = compileExpression(text0)
            xml.append("<expression>")
            for j in t0:
                xml.append("  "+j)
            xml.append("</expression>")
            break
    ans = compileExpression(text[text.index("<symbol> = </symbol>")+1:len(text)])
    xml.append("<expression>")
    for i in ans:
        xml.append("  "+i)
    xml.append("</expression>")
    return xml


def compileWhile(text:list):
    pass


def compileReturn(text:list):
    if text == ["<keyword> return </keyword>","<symbol> ; </symbol>"]:
        return text
    else:
        xml = ["<keyword> return </keyword>"]
        a = compileExpression(text[1:-1])
        xml.append("<expression>")
        for i in a:
            xml.append("  "+i)
        xml.append("</expression>")
        xml.append("<symbol> ; </symbol>")
        return xml


def compileIf(text:list):
    xml = ["<keyword> if </keyword>"]
    b = 0
    f = False
    start = -1
    te = []
    for i in text:
        if i == "<symbol> ( </symbol>":
            b += 1
        elif i == "<symbol> ) </symbol>":
            b -= 1
        if i == "<symbol> ( </symbol>":
            f = True
            start = b
        if f:
            te.append(i)
        if i == "<symbol> ) </symbol>" and b == start:
            f = False
            a = compileExpression(te)
            xml.append("<symbol> ( </symbol>")
            xml.append("<expression>")
            for j in a:
                xml.append("  "+j)
            xml.append("</expression>")
            xml.append("<symbol> ) </symbol>")
            break
    b = 0
    f = False
    start = -1
    te = []
    for i in text:
        if i == "<symbol> { </symbol>":
            b += 1
        elif i == "<symbol> } </symbol>":
            b -= 1
        if i == "<symbol> { </symbol>":
            f = True
            start = b
        if f:
            te.append(i)
        if i == "<symbol> } </symbol>" and b == start:
            f = False
            a = compileStatements(te)
            xml.append("<symbol> { </symbol>")
            xml.append("<expression>")
            for j in a:
                xml.append("  "+j)
            xml.append("</expression>")
            xml.append("<symbol> } </symbol>")
    return xml


def compileExpression(text:list):
    xml = []
    te0 = []
    f = False
    b = [0,0]
    start = 0
    for i in range(len(text)):
        ti = isTerm(text,i)
        if i == "<symbol> [ </symbol>":
            b[0] += 1
        if i == "<symbol> ( </symbol>":
            b[1] += 1
        if ti[0] == 1:
            xml.append("<term>")
            xml.append("  "+ti[1])
            xml.append("</term>")
        elif ti[0] == 2:
            f = True
            start = b[ti[1]]
            xml.append("<term>")
            for j in compileTerm(te0,2):
                xml.append("  "+j)
            xml.append("</term>")
        elif text[i] in l:
            xml.append(text[i])
        if i == "<symbol> ] </symbol>":
            b[0] -= 1
        if i == "<symbol> ) </symbol>":
            b[1] -= 1
    return xml


def isTerm(text,i):
    token = text[i]
    nextToken = text[i+1]
    if token.startswith("<integerConstant>") and token.endswith("</integerConstant>"):
        return [1,token]
    elif token.startswith("<stringConstant>") and token.endswith("</stringConstant>"):
        return [1,token]
    elif token in ['<keyword> true </keyword>', '<keyword> false </keyword>', '<keyword> null </keyword>', '<keyword> this </keyword>']:
        return [1,token]
    elif token.startswith("<identifier>") and token.endswith("</identifier>"):
        # 如果後面跟隨的是[expression]或(expressionList)，則需要額外的檢查
        if nextToken == '<symbol> ( </symbol>':
            return [2,1]
        if nextToken == '<symbol> [ </symbol>':
            return [2,0]
    elif token == '<symbol> ( </symbol>':
        # 需要找到對應的閉括號
        return [3,None]
    elif token in ['<symbol> - </symbol>','<symbol> ~ </symbol>']:
        ti = isTerm(text,i+1)
        if ti[0] != -1:
            return [4,ti[1]]
    return [-1,None]


def compileTerm(text:list,d:int):
    pass


def compileExpressionList(text:list):
    pass


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
            text = compiler(text)
            f = open(i.split(".")[0] + "_M.xml", "w")
            f.write("\n".join(text))
            f.close()
