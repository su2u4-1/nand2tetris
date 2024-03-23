class xml:
    def __init__(self, text: str, tag: str, sp: int):
        self.content = text
        self.text = f"<{tag}> {text} </{tag}>"
        self.tag = tag
        self.sp = sp


def compiler(text1, text2):
    global ls, gs, lvList, di, code
    lvList = []
    ls, gs = variableAnalysis(text1)
    print(gs, ls)
    text = structure(text2)
    print()
    walk_dict(text)
    classname = text[0][1][1][1]
    di = ["base"]
    code = []
    compile(text, classname)
    print()
    print(code)
    return code


def walk_dict(d, depth=0):
    for key, value in d.items():
        print("  " * depth + str(key), end=": ")
        if type(value) == list and value[0].startswith("dict_"):
            print("dict", value[0][5:])
            walk_dict(value[1], depth + 1)
        else:
            print(value[0][4:], value[1])


def variableAnalysis(text: list[xml]):
    sp = 0
    gsymbol = {}
    gsp = 0
    lsymbol = {}
    lsp = {}
    lia = ""
    np = 0
    source = text

    def Class():
        nonlocal gsp, sp
        now = source[sp]
        if now.tag == "keyword":
            if now.content in ["field", "static"]:
                ClassVarDec()
            elif now.content in ["constructor", "function", "method"]:
                SubroutineDec()
        elif now.tag == "identifier":
            gsymbol[now.content] = ["className", "className", gsp]
            gsp += 1
        elif now.tag == "symbol":
            if now.content == "}":
                return
        sp += 1
        Class()

    def ClassVarDec():
        global varvalue, vartype0
        nonlocal gsp, sp
        now = source[sp]
        if now.tag == "keyword" and now.content in ["field", "static", "int", "char", "boolean"]:
            if now.content in ["field", "static"]:
                varvalue = now.content
        elif now.tag == "identifier":
            if source[sp - 2].content in ["field", "static"]:
                vartype0 = source[sp - 1].content
                gsymbol[now.content] = [vartype0, varvalue, gsp]
                gsp += 1
            elif source[sp - 1].content == ",":
                gsymbol[now.content] = [vartype0, varvalue, gsp]
                gsp += 1
        elif now.tag == "symbol":
            if now.content == ";":
                return
        sp += 1
        ClassVarDec()

    def SubroutineDec():
        nonlocal sp, gsp, lia
        now = source[sp]
        if now.tag == "identifier":
            if source[sp - 2].content in ["constructor", "function", "method"]:
                lia = now.content
                gsymbol[now.content] = [source[sp - 1].content, "functionName", gsp]
                gsp += 1
        elif now.tag == "symbol":
            if now.content == "(":
                lsymbol[lia] = {}
                lsp[lia] = 0
                ParameterList()
            elif now.content == "{":
                SubroutineBody()
                return
        sp += 1
        SubroutineDec()

    def ParameterList():
        nonlocal sp
        sp += 1
        now = source[sp]
        if now.tag == "identifier":
            if source[sp - 1].tag == "identifier" or source[sp - 1].content in ["int", "char", "boolean"]:
                lsymbol[lia][now.content] = [source[sp - 1].content, "argument", lsp[lia]]
                lsp[lia] += 1
        elif now.tag == "symbol":
            if now.content == ")":
                sp -= 1
                return
        ParameterList()

    def SubroutineBody():
        nonlocal sp, np
        now = source[sp]
        if now.tag == "symbol":
            if now.content == "}":
                np -= 1
                if np == 0:
                    return
            elif now.content == "{":
                np += 1
        if now.tag == "keyword" and now.content == "var":
            VarDec()
        sp += 1
        SubroutineBody()

    def VarDec():
        global vartype1
        nonlocal sp
        now = source[sp]
        if now.tag == "symbol" and now.content == ";":
            return
        elif now.tag == "identifier":
            if source[sp - 2].content == "var":
                vartype1 = source[sp - 1].content
                lsymbol[lia][now.content] = [vartype1, "local", lsp[lia]]
                lsp[lia] += 1
            elif source[sp - 1].content == ",":
                lsymbol[lia][now.content] = [vartype1, "local", lsp[lia]]
                lsp[lia] += 1
        sp += 1
        VarDec()

    Class()
    return lsymbol, gsymbol


def structure(text: list[str]):
    def dec(elements: list[xml], index=0):
        nested_structure = {}
        stratum = 0
        while index < len(elements):
            now = elements[index]
            if now.tag == "startLabel":
                lvList.append(now.sp)
                nd, index = dec(elements, index + 1)
                nested_structure[stratum] = ["dict_" + now.content, nd]
            elif now.tag == "endLabel" and now.sp == lvList[-1]:
                lvList.pop()
                return nested_structure, index
            else:
                nested_structure[stratum] = ["str_" + now.tag, now.content]
            index += 1
            stratum += 1
        return nested_structure, index

    for i in range(len(text)):
        s = len(text[i])
        text[i] = text[i].strip()
        s -= len(text[i])
        if " " in text[i]:
            text[i] = text[i].split()
            text[i] = xml(text[i][1], text[i][0][1:-1], int(s / 2))
        elif text[i][0:2] == "</":
            text[i] = xml(text[i][2:-1], "endLabel", int(s / 2))
        else:
            text[i] = xml(text[i][1:-1], "startLabel", int(s / 2))
    return dec(text)[0]


def compile(d: dict[int:list], classname):
    global local_symbol
    if di[-1] == "subroutineDec":
        local_symbol = ls[d[2][1]]
        localn = 0
        for i in local_symbol.values():
            if i[1] == "local":
                localn += 1
        code.append(f"function {classname}.{d[2][1]} {localn}")
    elif di[-1] == "letStatement":
        if d[2][1] == "=":
            code.extend(compileExpression(d[3][1], classname))
            print(d[3][1])
            if d[1][1] in local_symbol:
                code.append(f"pop local {local_symbol[d[1][1]][2]}")
            else:
                code.append(f"pop {gs[d[1][1]][1]} {gs[d[1][1]][2]}")
        elif d[2][1] == "[":
            if d[1][1] in local_symbol:
                code.append(f"push local {local_symbol[d[1][1]][2]}")
            else:
                code.append(f"push {gs[d[1][1]][1]} {gs[d[1][1]][2]}")
            code.extend(compileExpression(d[3][1], classname))
            print(d[3][1])
            code.append("add")
            code.append("pop pointer 1")
            code.extend(compileExpression(d[3][1], classname))
            print(d[3][1])
            code.append("pop that 0")
            # this
    for key, value in d.items():
        if value[0].startswith("dict_"):
            di.append(value[0][5:])
            compile(value[1], classname)
        else:
            tag = value[0][4:]
            content = value[1]


# this
def compileExpression(d: dict[int:list], classname, content: list = None):
    print(rpn(d))
    return []
    content: list
    if content == None:
        content = []
    for value in d.values():
        if value[0].startswith("dict_"):
            di.append(value[0][5:])
            compileExpression(value[1], classname, content)
        else:
            content.append(value[1])
    return content


def rpn(d):
    content = []

    def a(d: dict[int, list[str, str | dict]]):
        for v in d.values():
            if v[0].startswith("dict_"):
                a(v[1])
            else:
                content.append(v[1])

    a(d)
    return content
