def compiler(text: list):
    ls, gs = variableAnalysis(text)
    print(gs)
    print(ls)
    return text

def variableAnalysis(text: list):
    sp = 0
    gsymbol = {}
    gsp = 0
    lsymbol = {}
    lsp = {}
    lia = 0
    np = 0
    source = text
    def Class():
        
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
        global var, vartype0
        now = source[sp]
        if now.tag == "keyword" and now.content in ["field", "static", "int", "char", "boolean"]:
            if now.content in ["field", "static"]:
                var = now.content
        elif now.tag == "identifier":
            if source[sp - 2].content in ["field", "static"]:
                vartype0 = source[sp - 1].content
                gsymbol[now.content] = [vartype0, var, gsp]
                gsp += 1
            elif source[sp - 1].content == ",":
                gsymbol[now.content] = [vartype0, var, gsp]
                gsp += 1
        elif now.tag == "symbol":
            if now.content == ";":
                return
        sp += 1
        ClassVarDec()
    def SubroutineDec():
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
