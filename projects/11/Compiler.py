class xml:
    def __init__(self, text: str, tag: str):
        self.content = text
        self.text = f"<{tag}> {text} </{tag}>"
        self.tag = tag


source: list[xml]


def compiler(text: list):
    global source, sp, gsymbol, gsp, lsymbol, lsp, lia
    sp = 0
    gsymbol = {}
    gsp = 0
    lsymbol = {}
    lsp = {}
    lia = 0
    source = text
    CompileClass()
    print(gsymbol)
    print(lsymbol)
    return text


def callCompile(tag: str):
    match tag:
        case "class":
            CompileClass()
        case "classVarDec":
            CompileClassVarDec()
        case "subroutineDec":
            CompileSubroutineDec()
        case "parameterList":
            CompileParameterList()
        case "subroutineBody":
            CompileSubroutineBody()
        case "varDec":
            CompileVarDec()
        case "statements":
            CompileStatements()
        case "letStatement":
            CompileLetStatement()
        case "ifStatement":
            CompileIfStatement()
        case "whileStatement":
            CompileWhileStatement()
        case "doStatement":
            CompileDoStatement()
        case "returnStatement":
            CompileReturnStatement()
        case "expression":
            CompileExpression()
        case "expressionList":
            CompileExpressionList()
        case "term":
            CompileTerm()


def CompileClass():
    global sp, gsp
    now = source[sp]
    if now.tag == "keyword":
        if now.content in ["field", "static"]:
            callCompile("classVarDec")
        elif now.content in ["constructor", "function", "method"]:
            callCompile("subroutineDec")
    elif now.tag == "identifier":
        gsymbol[now.content] = ["className", "className", gsp]
        gsp += 1
    elif now.tag == "symbol":
        if now.content == "}":
            return
    sp += 1
    CompileClass()


def CompileClassVarDec():
    global sp, gsp, var, vartype0
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
    CompileClassVarDec()


def CompileSubroutineDec():
    global sp, gsp, lia
    now = source[sp]
    if now.tag == "identifier":
        if source[sp - 2].content in ["constructor", "function", "method"]:
            gsymbol[now.content] = [source[sp - 1].content, "functionName", gsp]
            gsp += 1
    elif now.tag == "symbol":
        if now.content == "(":
            lsymbol[lia] = {}
            lsp[lia] = 0
            callCompile("parameterList")
        elif now.content == "{":
            callCompile("subroutineBody")
            lia += 1
            return
    sp += 1
    CompileSubroutineDec()


def CompileParameterList():
    global sp, lsp
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
    CompileParameterList()


def CompileSubroutineBody():
    global sp, lsp, lia
    now = source[sp]
    if now.tag == "symbol" and now.content == "}":
        return
    elif now.tag == "keyword":
        if now.content == "var":
            callCompile("varDec")
        elif now.content in ["let", "do", "if", "while", "return"]:
            callCompile("statements")
            sp -= 1
    sp += 1
    CompileSubroutineBody()


def CompileVarDec():
    global sp, lsp, vartype1
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
    CompileVarDec()


def CompileStatements():
    global sp
    now = source[sp]
    if now.tag == "keyword" and now.content in ["if", "let", "do", "while", "return"]:
        callCompile(f"{now.content}Statement")
        sp -= 1
    elif now.tag == "symbol" and now.content == "}":
        return
    sp += 1
    CompileStatements()


def CompileLetStatement():
    global sp
    now = source[sp]
    sp += 1
    if now.tag == "symbol":
        if now.content == ";":
            sp -= 1
            return
        elif now.content == "[":
            callCompile("expression")
        elif now.content == "=":
            callCompile("expression")
    CompileLetStatement()


def CompileIfStatement():
    global sp
    now = source[sp]
    sp += 1
    next = source[sp + 1]
    if now.tag == "symbol":
        if now.content == "(":
            callCompile("expression")
        elif now.content == "{":
            callCompile("statements")
        elif now.content == "}":
            if next.tag != "keyword" or next.content != "else":
                return
    CompileIfStatement()


def CompileWhileStatement():
    global sp
    now = source[sp]
    sp += 1
    if now.tag == "symbol":
        if now.content == "(":
            callCompile("expression")
        elif now.content == "{":
            callCompile("statements")
        elif now.content == "}":
            return
    CompileWhileStatement()


def CompileDoStatement():
    global sp
    now = source[sp]
    sp += 1
    if now.tag == "symbol":
        if now.content == ";":
            return
        elif now.content == "(":
            callCompile("expressionList")
    CompileDoStatement()


def CompileReturnStatement():
    global sp
    now = source[sp]
    if now.tag == "keyword" and now.content == "return":
        pass
    elif now.tag == "symbol" or now.content == ";":
        return
    else:
        callCompile("expression")
        sp -= 1
    sp += 1
    CompileReturnStatement()


def CompileExpression(f=False):
    global sp
    now = source[sp]
    if now.tag == "symbol" and now.content in ["+", "-", "*", "/", "&", "|", "<", ">", "="] and f:
        pass
    elif now.tag == "symbol" and now.content in [";", ")", "]", "}", ","]:
        return
    else:
        callCompile("term")
        sp -= 1
    sp += 1
    CompileExpression(True)


def CompileExpressionList(f=False):
    global sp
    now = source[sp]
    if now.tag == "symbol" and now.content == "," and f:
        pass
    elif now.tag == "symbol" and now.content == ")":
        return
    else:
        callCompile("expression")
        sp -= 1
    sp += 1
    CompileExpressionList(True)


def CompileTerm(f=False):
    global sp
    now = source[sp]
    previous = source[sp - 1]
    sp += 1
    next = source[sp]
    if now.tag in ["integerConstant", "stringConstant"] or (now.tag == "keyword" and now.content in ["true", "false", "null", "this"]):
        return
    elif now.tag in "identifier":
        if next.tag != "symbol" or next.content not in ["(", ".", "["]:
            return
    elif now.tag == "symbol" and now.content in ["(", ")", "[", "]", "-", "~", "."]:
        if now.content == "(":
            if previous.tag == "identifier":
                callCompile("expressionList")
            else:
                callCompile("expression")
        elif now.content == "[":
            callCompile("expression")
        elif now.content in ["]", ")"]:
            return
        elif now.content in ["-", "~"]:
            callCompile("term")
            return
    CompileTerm()
