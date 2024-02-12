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
l = [
    "<symbol> + </symbol>",
    "<symbol> - </symbol>",
    "<symbol> * </symbol>",
    "<symbol> / </symbol>",
    "<symbol> &amp; </symbol>",
    "<symbol> | </symbol>",
    "<symbol> &gt; </symbol>",
    "<symbol> &lt; </symbol>",
    "<symbol> = </symbol>",
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
        if text[i].startswith(' " ') and text[i].endswith('"'):
            text[i] = '"' + text[i][3:-2] + '"'
        elif (text[i][0:2] != ' "' and text[i][0] != '"') or text[i][-1] != '"':
            if text[i] in symbolList:
                continue
            else:
                for k in symbolList:
                    if k in text[i]:
                        t = text[i].split(k, 1)
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
        xml.append("  " + i)
    xml.append("  <symbol> } </symbol>")
    xml.append("</class>\n")
    return xml


def compileClass(text: list):
    xml = ["<keyword> class </keyword>"]
    text.remove("<keyword> class </keyword>")
    for i in text:
        if i.startswith("<identifier> ") and i.endswith(" </identifier>"):
            xml.append(i)
            text.remove(i)
            break
    f0 = False
    ClassVarDec = []
    xml.append("<symbol> { </symbol>")
    for i in text:
        if i == "<keyword> static </keyword>" or i == "<keyword> field </keyword>":
            f0 = True
        if f0:
            ClassVarDec.append(i)
        if i == "<symbol> ; </symbol>":
            f0 = False
            xml.append("<classVarDec>")
            for i in ClassVarDec:
                xml.append("  " + i)
            xml.append("</classVarDec>")
            ClassVarDec = []
        if i == "<keyword> constructor </keyword>" or i == "<keyword> method </keyword>" or i == "<keyword> function </keyword>":
            break
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
            SubroutineStart = b
        if f1:
            text1.append(i)
        if b == SubroutineStart and i == "<symbol> } </symbol>":
            f1 = False
            Subroutine = compileSubroutine(text1)
            xml.append("<subroutineDec>")
            for j in Subroutine:
                xml.append("  " + j)
            xml.append("</subroutineDec>")
            text1 = []
    return xml


def compileSubroutine(text: list):
    xml = []
    f = False
    ParameterList = []
    for i in text:
        if i == "<symbol> ( </symbol>":
            break
        xml.append(i)
    for i in text:
        if i == "<symbol> ) </symbol>":
            f = False
            break
        if f:
            ParameterList.append(i)
        if i == "<symbol> ( </symbol>":
            f = True
    xml.append("<symbol> ( </symbol>")
    xml.append("<parameterList>")
    for i in ParameterList:
        xml.append("  " + i)
        text.remove(i)
    xml.append("</parameterList>")
    xml.append("<symbol> ) </symbol>")
    if text[-1] == "<symbol> } </symbol>":
        text.pop()
    SubroutineBody = compileSubroutineBody(text)
    xml.append("<subroutineBody>")
    for i in SubroutineBody:
        xml.append("  " + i)
    xml.append("</subroutineBody>")
    return xml


def compileSubroutineBody(text: list):
    xml = ["<symbol> { </symbol>"]
    f = False
    for i in range(len(text)):
        if text[i] == "<keyword> var </keyword>":
            f = True
            VarDec = []
        if f:
            VarDec.append(text[i])
        if text[i] == "<symbol> ; </symbol>":
            f = False
            xml.append("<varDec>")
            for j in VarDec:
                xml.append("  " + j)
            xml.append("</varDec>")
        if not f and text[i] in ["<keyword> do </keyword>","<keyword> let </keyword>","<keyword> while </keyword>","<keyword> return </keyword>","<keyword> if </keyword>"]:
            break
    text = text[i:]
    if text[-1] == "<symbol> } </symbol>":
        text.pop()
    Statements = compileStatements(text)
    xml.append("<statements>")
    for i in Statements:
        xml.append("  " + i)
    xml.append("</statements>")
    xml.append("<symbol> } </symbol>")
    return xml


def compileStatements(text: list):
    xml = []
    b = 0
    f = [False, False, False, False, False, False]
    whileStart = -1
    ifStart = -1
    elseStart = -1
    te = [[], [], [], [], []]
    for i in range(len(text)):
        if text[i] == "<symbol> { </symbol>":
            b += 1
        if text[i] == "<symbol> } </symbol>":
            b -= 1
        if not(f[0] or f[1] or f[2] or f[3] or f[4] or f[5]):
            if text[i] == "<keyword> do </keyword>":
                f[0] = True
            elif text[i] == "<keyword> let </keyword>":
                f[1] = True
            elif text[i] == "<keyword> while </keyword>":
                f[2] = True
                whileStart = b
            elif text[i] == "<keyword> return </keyword>":
                f[3] = True
            elif text[i] == "<keyword> if </keyword>":
                f[4] = True
                ifStart = b
            elif text[i] == "<keyword> else </keyword>":
                f[5] = True
                elseStart = b
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
                for j in compileDo(te[0]):
                    xml.append("  " + j)
                xml.append("</doStatement>")
                te[0] = []
            if f[1]:
                f[1] = False
                Lat = compileLet(te[1])
                xml.append("<letStatement>")
                for j in Lat:
                    xml.append("  " + j)
                xml.append("</letStatement>")
                te[1] = []
            if f[3]:
                f[3] = False
                Return = compileReturn(te[3])
                xml.append("<returnStatement>")
                for j in Return:
                    xml.append("  " + j)
                xml.append("</returnStatement>")
                te[3] = []
        if text[i] == "<symbol> } </symbol>":
            if f[2] and b == whileStart:
                f[2] = False
                While = compileWhile(te[2])
                xml.append("<whileStatement>")
                for j in While:
                    xml.append("  " + j)
                xml.append("</whileStatement>")
                te[2] = []
            elif f[4] and b == ifStart:
                f[4] = False
                if text[i + 1] != "<keyword> else </keyword>":
                    If = compileIf(te[4],False)
                    xml.append("<ifStatement>")
                    for j in If:
                        xml.append("  " + j)
                    xml.append("</ifStatement>")
                    te[4] = []
            elif f[5] and b == elseStart:
                f[5] = False
                If = compileIf(te[4],True)
                xml.append("<ifStatement>")
                for j in If:
                    xml.append("  " + j)
                xml.append("</ifStatement>")
                te[4] = []
    return xml


def compileDo(text: list):
    xml = []
    b = 0
    f = False
    t = []
    for i in text:
        if i == "<symbol> ) </symbol>":
            b -= 1
            if b == 0:
                f = False
                xml.append("<expressionList>")
                for j in compileExpressionList(t):
                    xml.append("  "+j)
                xml.append("</expressionList>")
        if f:
            t.append(i)
        else:
            xml.append(i)
        if i == "<symbol> ( </symbol>":
            b += 1
            if b == 1:
                f = True
    return xml


def compileLet(text: list):
    xml = [text[0],text[1]]
    if "<symbol> [ </symbol>" in text and "<symbol> ] </symbol>" in text:
        a = text[text.index("<symbol> [ </symbol>") + 1:text.index("<symbol> ] </symbol>")]
        xml.append("<symbol> [ </symbol>")
        xml.append("<expression>")
        for i in compileExpression(a):
            xml.append("  " + i)
        xml.append("</expression>")
        xml.append("<symbol> ] </symbol>")
    xml.append("<symbol> = </symbol>")
    a = text[text.index("<symbol> = </symbol>") + 1:]
    xml.append("<expression>")
    for i in compileExpression(a):
        xml.append("  " + i)
    xml.append("</expression>")
    if a[-1] == "<symbol> ; </symbol>":
        xml.append("<symbol> ; </symbol>")
    return xml


def compileWhile(text: list):
    xml = ["<keyword> while </keyword>"]
    f = False
    t = []
    b = 0
    start = -1
    for i in text:
        if i == "<symbol> ( </symbol>":
            b += 1
        if i == "<symbol> ) </symbol>":
            b -= 1
        if i == "<symbol> ) </symbol>" and start == b:
            f = False
            xml.append("<symbol> ( </symbol>")
            xml.append("<expression>")
            for j in compileExpression(t):
                xml.append("  " + j)
            xml.append("</expression>")
            xml.append("<symbol> ) </symbol>")
            if t[-1] == "<symbol> ; </symbol>":
                xml.append("<symbol> ; </symbol>")
            break
        if f:
            t.append(i)
        if i == "<symbol> ( </symbol>" and not f:
            f = True
            start = b-1
    t = []
    b = 0
    start = -1
    for i in text:
        if i == "<symbol> { </symbol>":
            b += 1
            if not f:
                f = True
                start = b-1
        if i == "<symbol> } </symbol>":
            b -= 1
        if f:
            t.append(i)
        if i == "<symbol> } </symbol>" and start == b:
            f = False
            xml.append("<symbol> { </symbol>")
            xml.append("<statements>")
            for j in compileStatements(t):
                xml.append("  " + j)
            xml.append("</statements>")
            xml.append("<symbol> } </symbol>")
            break
    return xml


def compileReturn(text: list):
    if text == ["<keyword> return </keyword>", "<symbol> ; </symbol>"]:
        return text
    else:
        xml = ["<keyword> return </keyword>"]
        a = compileExpression(text[1:-1])
        xml.append("<expression>")
        for i in a:
            xml.append("  " + i)
        xml.append("</expression>")
        xml.append("<symbol> ; </symbol>")
        return xml


def compileIf(text:list,f1:bool):
    xml = ["<keyword> if </keyword>"]
    b = 0
    f = False
    start = -1
    te = []
    for i in text:
        if i == "<symbol> ( </symbol>":
            b += 1
        if i == "<symbol> ( </symbol>" and not f:
            f = True
            start = b
        if f:
            te.append(i)
        if i == "<symbol> ) </symbol>" and b == start:
            f = False
            a = compileExpression(te[1:-1])
            xml.append("<symbol> ( </symbol>")
            xml.append("<expression>")
            for j in a:
                xml.append("  " + j)
            xml.append("</expression>")
            xml.append("<symbol> ) </symbol>")
            if te[-1] == "<symbol> ; </symbol>":
                xml.append("<symbol> ; </symbol>")
            break
        if i == "<symbol> ) </symbol>":
            b -= 1
    b = 0
    f = False
    start = -1
    te = []
    for i in text:
        if i == "<symbol> } </symbol>" and b == start:
            f = False
            a = compileStatements(te)
            xml.append("<symbol> { </symbol>")
            xml.append("<statements>")
            for j in a:
                xml.append("  " + j)
            xml.append("</statements>")
            xml.append("<symbol> } </symbol>")
            if f1:
                xml.append("<keyword> else </keyword>")
                f1 = False
            te = []
        if i == "<symbol> } </symbol>":
            b -= 1
        if f:
            te.append(i)
        if i == "<symbol> { </symbol>":
            b += 1
            f = True
            start = b
    return xml


def compileExpression(text: list):
    xml = []
    b = 0
    t = []
    for i in text:
        if i in ["<symbol> ( </symbol>","<symbol> [ </symbol>","<symbol> { </symbol>"]:
            b += 1
        if i in ["<symbol> ) </symbol>","<symbol> ] </symbol>","<symbol> } </symbol>"]:
            b -= 1
        if b == 0 and i != text[0] and i in l:
            te = compileTerm(t)
            xml.append("<term>")
            for j in te:
                xml.append("  "+j)
            xml.append("</term>")
            xml.append(i)
            t = []
        else:
            t.append(i)
    if t != []:
        te = compileTerm(t)
        xml.append("<term>")
        for j in te:
            xml.append("  "+j)
        xml.append("</term>")
    return xml


def compileTerm(text: list):
    xml = []
    b = 0
    f = False
    te = []
    if text[0].startswith("<integerConstant>") and text[0].endswith("</integerConstant>"):
        return [text[0]]
    elif text[0] in ["<keyword> true </keyword>","<keyword> false </keyword>","<keyword> null </keyword>","<keyword> this </keyword>"]:
        return [text[0]]
    elif text[0].startswith("<stringConstant>") and text[0].endswith("</stringConstant>"):
        return [text[0]]
    elif text[0].startswith("<identifier>") and text[0].endswith("</identifier>"):
        if len(text) > 1:
            if text[1] == "<symbol> [ </symbol>":
                for i in text:
                    if i == "<symbol> ] </symbol>":
                        b -= 1
                        if b == 0:
                            f = False
                            xml.append(text[0])
                            xml.append(text[1])
                            xml.append("<expression>")
                            for j in compileExpression(te):
                                xml.append("  "+j)
                            xml.append("</expression>")
                            xml.append("<symbol> ] </symbol>")
                            return xml
                    if f:
                        te.append(i)
                    if i == "<symbol> [ </symbol>":
                        b += 1
                        if b == 1:
                            f = True
            elif text[1] == "<symbol> ( </symbol>":
                for i in text:
                    if i == "<symbol> ) </symbol>":
                        b -= 1
                        if b == 0:
                            f = False
                            xml.append(text[0])
                            xml.append(text[1])
                            xml.append("<expressionList>")
                            for j in compileExpressionList(te):
                                xml.append("  "+j)
                            xml.append("</expressionList>")
                            xml.append("<symbol> ) </symbol>")
                            return xml
                    if f:
                        te.append(i)
                    if i == "<symbol> ( </symbol>":
                        b += 1
                        if b == 1:
                            f = True
            elif text[1] == "<symbol> . </symbol>":
                if text[2].startswith("<identifier>") and text[2].endswith("</identifier>"):
                    if text[3] == "<symbol> ( </symbol>":
                        for i in text:
                            if i == "<symbol> ) </symbol>":
                                b -= 1
                                if b == 0:
                                    f = False
                                    xml.append(text[0])
                                    xml.append(text[1])
                                    xml.append(text[2])
                                    xml.append(text[3])
                                    xml.append("<expressionList>")
                                    for j in compileExpressionList(te):
                                        xml.append("  "+j)
                                    xml.append("</expressionList>")
                                    xml.append("<symbol> ) </symbol>")
                                    return xml
                            if f:
                                te.append(i)
                            if i == "<symbol> ( </symbol>":
                                b += 1
                                if b == 1:
                                    f = True
            else:
                return [text[0]]
        else:
            return [text[0]]
    elif text[0] == "<symbol> ( </symbol>":
        for i in text:
            if i == "<symbol> ) </symbol>":
                b -= 1
                if b == 0:
                    f = False
                    xml.append("<symbol> ( </symbol>")
                    xml.append("<expression>")
                    for j in compileExpression(te):
                        xml.append("  "+j)
                    xml.append("</expression>")
                    xml.append("<symbol> ) </symbol>")
                    return xml
            if f:
                te.append(i)
            if i == "<symbol> ( </symbol>":
                b += 1
                if b == 1:
                    f = True
    elif text[0] in ["<symbol> ~ </symbol>","<symbol> - </symbol>"]:
        xml.append(text[0])
        xml.append("<term>")
        for j in compileTerm(text[1:]):
            xml.append("  "+j)
        xml.append("</term>")
        return xml
    print(text)
    print(xml)
    exit()


def compileExpressionList(text: list):
    xml = []
    b = 0
    t = []
    for i in text:
        if i in ["<symbol> ( </symbol>","<symbol> [ </symbol>","<symbol> { </symbol>"]:
            b += 1
        if i in ["<symbol> ) </symbol>","<symbol> ] </symbol>","<symbol> } </symbol>"]:
            b -= 1
        if b == 0 and i == "<symbol> , </symbol>":
            te = compileExpression(t)
            xml.append("<expression>")
            for j in te:
                xml.append("  "+j)
            xml.append("</expression>")
            xml.append(i)
            t = []
        else:
            t.append(i)
    if t != []:
        te = compileExpression(t)
        xml.append("<expression>")
        for j in te:
            xml.append("  "+j)
        xml.append("</expression>")
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
            text = compiler(text)
            f = open(i.split(".")[0] + "_M.xml", "w")
            f.write("\n".join(text))
            f.close()
