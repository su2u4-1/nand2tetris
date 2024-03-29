class xml:
    def __init__(self, text: str, tag: str, sp: int):
        self.content = text
        self.text = f"<{tag}> {text} </{tag}>"
        self.tag = tag
        self.sp = sp


def main(text1, text2):
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
    compiler(text, classname)
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
    gsp = {"className": 0, "functionName": 0, "field": 0, "static": 0}
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
            gsymbol[now.content] = ["className", "className", gsp["className"]]
            gsp["className"] += 1
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
                gsymbol[now.content] = [vartype0, varvalue, gsp[varvalue]]
                gsp[varvalue] += 1
            elif source[sp - 1].content == ",":
                gsymbol[now.content] = [vartype0, varvalue, gsp[varvalue]]
                gsp[varvalue] += 1
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
                gsymbol[now.content] = [source[sp - 1].content, "functionName", gsp["functionName"]]
                gsp["functionName"] += 1
        elif now.tag == "symbol":
            if now.content == "(":
                lsymbol[lia] = {}
                lsp[lia] = {"local": 0, "argument": 0}
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
                lsymbol[lia][now.content] = [source[sp - 1].content, "argument", lsp[lia]["argument"]]
                lsp[lia]["argument"] += 1
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
                lsymbol[lia][now.content] = [vartype1, "local", lsp[lia]["local"]]
                lsp[lia]["local"] += 1
            elif source[sp - 1].content == ",":
                lsymbol[lia][now.content] = [vartype1, "local", lsp[lia]["local"]]
                lsp[lia]["local"] += 1
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


def compiler(d: dict[int:list], classname):
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
                code.extend(compileExpression(d[6][1], classname))
                code.append("pop that 0")
        elif di[-1] == "doStatement":
            de = {}
            for i in range(1, len(d) - 1):
                de[i - 1] = d[i]
            code.extend(compileSubroutineCall(de, classname))
            code.append("pop temp 0")
        elif di[-1] == "returnStatement":
            if d[1][0] == "str_symbol" and d[1][1] == ";":
                code.append("push constant 0")
            else:
                code.extend(compileExpression(d[1][1], classname))
            code.append("return")
        '''for key, value in d.items():
            if value[0].startswith("dict_"):
                di.append(value[0][5:])
                compile(value[1], classname)
            else:
                tag = value[0][4:]
                content = value[1]'''

    def compileExpression(d: dict[int, list[str, str | dict]], classname):
        content = []
        c = []
        e = []
        for v in d.values():
            if v[0].startswith("dict_term"):
                e.append(compileTerm(v[1], classname))
            else:
                if v[1] == "+":
                    c.append("add")
                elif v[1] == "-":
                    c.append("sub")
                elif v[1] == "*":
                    c.append("call Math.multiply 2")
                elif v[1] == "/":
                    c.append("call Math.divide 2")
                elif v[1] == "&":
                    c.append("and")
                elif v[1] == "|":
                    c.append("or")
                elif v[1] == ">":
                    c.append("gt")
                elif v[1] == "<":
                    c.append("lt")
                elif v[1] == "=":
                    c.append("eq")
        n = 2
        for i in c:
            e.insert(n, [i])
            n += 2
        for i in e:
            content.extend(i)
        return content

    def compileTerm(d: dict[int, list[str, str | dict]], classname):
        content = []
        if 1 in d and d[0][1] in ["-", "~"] and d[1][0] == "dict_term":
            content.extend(compileTerm(d[1][1], classname))
            if d[0][1] == "-":
                content.append("neg")
            elif d[0][1] == "~":
                content.append("not")
        elif 5 in d and d[0][0] == "str_identifier" and d[1][1] == "." and d[2][0] == "str_identifier" and d[3] == ["str_symbol", "("]:
            content.extend(compileSubroutineCall(d, classname))
        elif 3 in d and d[0][0] == "str_identifier" and d[1][1] == "(" and d[2][0] == "dict_expressionList" and d[3][1] == ")":
            content.extend(compileSubroutineCall(d, classname))
        elif 2 in d and d[0][1] == "(" and d[1][0] == "dict_expression" and d[2][1] == ")":
            content.extend(compileExpression(d[1][1], classname))
        elif 3 in d and d[0][0] == "str_identifier" and d[1][1] == "[" and d[2][0] == "dict_expression" and d[3][1] == "]":
            if d[2][1] in local_symbol:
                content.append(f"push local {local_symbol[d[2][1]][2]}")
            else:
                content.append(f"push {gs[d[2][1]][1]} {gs[d[2][1]][2]}")
            content.extend(compileExpression(d[3][1], classname))
            content.append("add")
            content.append("pop pointer 1")
            content.append("push that 0")
        elif 0 in d and 1 not in d:
            if d[0][0] == "str_integerConstant":
                content.append(f"push constant {d[0][1]}")
            if d[0][0] == "str_stringConstant":
                content.append(f"push constant {len(d[0][1])}")
                content.append("call String.new 1")
                for i in d[0][1]:
                    content.append(f"push constant {ord(i)}")
                    content.append("call String.appendChar 2")
            if d[0][0] == "str_keywordConstant":
                if d[0][1] == "true":
                    content.append("push constant 1")
                    content.append("neg")
                elif d[0][1] == "false":
                    content.append("push constant 0")
                elif d[0][1] == "null":
                    content.append("push constant 0")
                elif d[0][1] == "this":
                    content.append("push pointer 0")
            if d[0][0] == "str_identifier":
                if d[0][1] in local_symbol:
                    content.append(f"push local {local_symbol[d[0][1]][2]}")
                else:
                    content.append(f"push {gs[d[0][1]][1]} {gs[d[0][1]][2]}")
        return content

    def compileSubroutineCall(d: dict[int, list[str, str | dict]], classname):
        content = []
        if d[2][0] == "dict_expressionList":
            mode = 1
            t, n = compileExpressionList(d[2][1], classname)
            content.extend(t)
        elif d[4][0] == "dict_expressionList":
            mode = 0
            t, n = compileExpressionList(d[4][1], classname)
            content.extend(t)
        if mode == 1:
            content.append(f"call {classname}.{d[0][1]} {n}")
        else:
            content.append(f"call {d[0][1]}.{d[2][1]} {n}")
        return content

    def compileExpressionList(d: dict[int, list[str, str | dict]], classname):
        content = []
        n = 0
        for v in d.values():
            if v[0] == "dict_expression":
                n += 1
                content.extend(compileExpression(v[1], classname))
        return content, n

    return compile(d, classname)
