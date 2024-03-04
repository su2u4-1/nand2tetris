class xml:
    def __init__(self, text: str, tag: str):
        self.content = text
        self.text = f"<{tag}> {text} </{tag}>"
        self.tag = tag


source: list[xml]


def grammarAnalyzer(text: list):
    global source, ia, sp, CodeList, gsymbol, gsp, lsymbol, lsp, lia
    CodeList = []
    ia = 0
    sp = 0
    gsymbol = {}
    gsp = 0
    lsymbol = {}
    lsp = {}
    lia = 0
    for i in range(len(text)):
        text[i] = xml(text[i][0], text[i][1])
    source = text
    CompileClass()
    return CodeList


def callCompile(tag: str):
    global ia, sp
    addCode(f"<{tag}>")
    ia += 1
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
    ia -= 1
    addCode(f"</{tag}>")


def addCode(text: str):
    global ia, sp
    CodeList.append("  " * ia + text)


def CompileClass():
    global sp, gsp
    now = source[sp]
    if now.tag == "keyword":
        if now.content == "class":
            addCode(now.text)
        elif now.content in ["field", "static"]:
            callCompile("classVarDec")
        elif now.content in ["constructor", "function", "method"]:
            callCompile("subroutineDec")
    elif now.tag == "identifier":
        gsymbol[now.content] = ["className", "className", gsp]
        gsp += 1
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "{":
            addCode(now.text)
        elif now.content == "}":
            addCode(now.text)
            return
    sp += 1
    CompileClass()


def CompileClassVarDec():
    global sp, gsp
    now = source[sp]
    if now.tag == "keyword" and now.content in ["field", "static", "int", "char", "boolean"]:
        addCode(now.text)
        if now.content in ["int", "char", "boolean"]:
            vartype = now.content
        else:
            var = now.content
    elif now.tag == "identifier":
        if source[sp - 1].content in ["field", "static"]:
            vartype = now.content
        if source[sp - 2].content in ["field", "static"]:
            gsymbol[now.content] = [vartype, var, gsp]
            gsp += 1
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == ",":
            addCode(now.text)
        elif now.content == ";":
            addCode(now.text)
            return
    sp += 1
    CompileClassVarDec()


def CompileSubroutineDec():
    global sp, gsp, lia
    now = source[sp]
    if now.tag == "identifier":
        if source[sp - 2].content in ["constructor", "function", "method"]:
            gsymbol[now.content] = ["functionName", "functionName", gsp]
            gsp += 1
        addCode(now.text)
    elif now.tag == "keyword" and now.content in ["constructor", "function", "method", "int", "char", "boolean", "void"]:
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "(":
            addCode(now.text)
            lsymbol[lia] = {}
            lsp[lia] = 0
            callCompile("parameterList")
            lia += 1
        elif now.content == ")":
            addCode(now.text)
        elif now.content == "{":
            callCompile("subroutineBody")
            return
    sp += 1
    CompileSubroutineDec()


def CompileParameterList():
    global sp, lsp
    sp += 1
    now = source[sp]
    if now.tag == "keyword" and now.content in ["int", "char", "boolean"]:
        addCode(now.text)
    elif now.tag == "identifier":
        if source[sp - 1].tag == "identifier" or source[sp - 1].content in ["int", "char", "boolean"]:
            lsymbol[lia][now.content] = [source[sp - 1].content, "argument", lsp[lia]]
            lsp[lia] += 1
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == ")":
            sp -= 1
            return
        elif now.content == ",":
            addCode(now.text)
    CompileParameterList()


def CompileSubroutineBody():
    global sp, lsp, lia
    now = source[sp]
    if now.tag == "symbol":
        if now.content == "{":
            addCode(now.text)
        elif now.content == "}":
            addCode(now.text)
            return
    elif now.tag == "keyword":
        if now.content == "var":
            lsymbol[lia] = {}
            lsp[lia] = 0
            callCompile("varDec")
            lia += 1
        elif now.content in ["let", "do", "if", "while", "return"]:
            callCompile("statements")
            sp -= 1
    sp += 1
    CompileSubroutineBody()


def CompileVarDec():
    global sp, lsp
    now = source[sp]
    if now.tag == "keyword" and now.content in ["var", "int", "char", "boolean"]:
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == ",":
            addCode(now.text)
        elif now.content == ";":
            addCode(now.text)
            return
    elif now.tag == "identifier":
        if source[sp - 2].content == "var":
            lsymbol[lia] = [source[sp - 1], "local", lsp[lia]]
            lsp[lia] += 1
        addCode(now.text)
    sp += 1
    CompileVarDec()


def CompileStatements():
    global sp, lsp
    now = source[sp]
    if now.tag == "keyword" and now.content in ["if", "let", "do", "while", "return"]:
        callCompile(f"{now.content}Statement")
        sp -= 1
    elif now.tag == "symbol" and now.content == "}":
        return
    sp += 1
    CompileStatements()


def CompileLetStatement():
    global sp, lsp
    now = source[sp]
    sp += 1
    if now.tag == "identifier":
        addCode(now.text)
    elif now.tag == "keyword" and now.content == "let":
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == ",":
            addCode(now.text)
        elif now.content == ";":
            addCode(now.text)
            sp -= 1
            return
        elif now.content == "[":
            addCode(now.text)
            callCompile("expression")
        elif now.content == "]":
            addCode(now.text)
        elif now.content == "=":
            addCode(now.text)
            callCompile("expression")
    CompileLetStatement()


def CompileIfStatement():
    global sp, lsp
    now = source[sp]
    sp += 1
    next = source[sp + 1]
    if now.tag == "keyword" and now.content in ["if", "else"]:
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "(":
            addCode(now.text)
            callCompile("expression")
        elif now.content == ")":
            addCode(now.text)
        elif now.content == "{":
            addCode(now.text)
            callCompile("statements")
        elif now.content == "}":
            addCode(now.text)
            if next.tag != "keyword" or next.content != "else":
                return
    CompileIfStatement()


def CompileWhileStatement():
    global sp, lsp
    now = source[sp]
    sp += 1
    if now.tag == "keyword" and now.content == "while":
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "(":
            addCode(now.text)
            callCompile("expression")
        elif now.content == ")":
            addCode(now.text)
        elif now.content == "{":
            addCode(now.text)
            callCompile("statements")
        elif now.content == "}":
            addCode(now.text)
            return
    CompileWhileStatement()


def CompileDoStatement():
    global sp, lsp
    now = source[sp]
    sp += 1
    if now.tag == "identifier":
        addCode(now.text)
    elif now.tag == "keyword" and now.content == "do":
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == ";":
            addCode(now.text)
            return
        elif now.content in [".", ")"]:
            addCode(now.text)
        elif now.content == "(":
            addCode(now.text)
            callCompile("expressionList")
    CompileDoStatement()


def CompileReturnStatement():
    global sp, lsp
    now = source[sp]
    if now.tag == "keyword" and now.content == "return":
        addCode(now.text)
    elif now.tag == "symbol" or now.content == ";":
        addCode(now.text)
        return
    else:
        callCompile("expression")
        sp -= 1
    sp += 1
    CompileReturnStatement()


def CompileExpression(f=False):
    global sp, lsp
    now = source[sp]
    if now.tag == "symbol" and now.content in ["+", "-", "*", "/", "&", "|", "<", ">", "="] and f:
        addCode(now.text)
    elif now.tag == "symbol" and now.content in [";", ")", "]", "}", ","]:
        return
    else:
        callCompile("term")
        sp -= 1
    sp += 1
    CompileExpression(True)


def CompileExpressionList(f=False):
    global sp, lsp
    now = source[sp]
    if now.tag == "symbol" and now.content == "," and f:
        addCode(now.text)
    elif now.tag == "symbol" and now.content == ")":
        return
    else:
        callCompile("expression")
        sp -= 1
    sp += 1
    CompileExpressionList(True)


def CompileTerm(f=False):
    global sp, lsp
    now = source[sp]
    previous = source[sp - 1]
    sp += 1
    next = source[sp]
    if now.tag in ["integerConstant", "stringConstant"] or (now.tag == "keyword" and now.content in ["true", "false", "null", "this"]):
        addCode(now.text)
        return
    elif now.tag in "identifier":
        addCode(now.text)
        if next.tag != "symbol" or next.content not in ["(", ".", "["]:
            return
    elif now.tag == "symbol" and now.content in ["(", ")", "[", "]", "-", "~", "."]:
        addCode(now.text)
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
