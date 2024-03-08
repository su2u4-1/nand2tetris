class xml:
    def __init__(self, text: str, tag: str, sp: int):
        self.content = text
        self.text = f"<{tag}> {text} </{tag}>"
        self.tag = tag
        self.sp = sp


def compiler(text1, text2):
    global ls, gs
    ls, gs = variableAnalysis(text1)
    print(gs)
    print(ls)
    code = compile(text2)
    print(code)
    return code


def variableAnalysis(text: list[xml]):
    sp = 0
    gsymbol = {}
    gsp = 0
    lsymbol = {}
    lsp = {}
    lia = 0
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
                gsymbol[now.content] = [source[sp - 1].content, "functionName", gsp]
                gsp += 1
        elif now.tag == "symbol":
            if now.content == "(":
                lsymbol[lia] = {}
                lsp[lia] = 0
                ParameterList()
            elif now.content == "{":
                SubroutineBody()
                lia += 1
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


def compile(text: list[str]):
    for i in range(len(text)):
        s = len(text[i])
        text[i] = text[i].strip()
        s -= len(text[i])
        if " " in text[i]:
            text[i] = text[i].split()
            text[i] = xml(text[i][1], text[i][0], s / 2)
        elif text[i][0:2] == "</":
            text[i] = xml(text[i][2:-1], "endLabel", s / 2)
        else:
            text[i] = xml(text[i][1:-1], "startLabel", s / 2)
    dec(text)


def dec(text: list[xml]):
    pass
