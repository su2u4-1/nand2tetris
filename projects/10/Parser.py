CodeList = []
ia = 0
sp = 0


class xml:
    def __init__(text: str, tag: str):
        content = text
        text = f"<{tag}> {text} </{tag}>"
        tag = tag


def grammarAnalyzer(text: list):
    global source
    for i in range(len(text)):
        text[i] = xml(text[i][0], text[i][1])
    text.append(xml("exit", "end"))
    source = text
    code = Compile()
    for i in code:
        print(i)
    return code


def callCompile(tag: str):
    print(sp, source[sp].content, tag)
    if sp >= 305:
        for i in CodeList:
            print(i)
        exit()
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
    CodeList.append("  " * ia + text)


def Compile():
    callCompile("class")
    return CodeList


def CompileClass():
    now = source[sp]
    next = source[sp]
    if now.tag == "keyword" and now.content == "class":
        addCode(now.text)
    elif now.tag == "identifier":
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "{":
            addCode(now.text)
        elif now.content == "}":
            addCode(now.text)
            return
    if now.content in ["field", "static"]:
        callCompile("classVarDec")
    elif now.content in ["constructor", "function", "method"]:
        callCompile("subroutineDec")
    sp += 1
    CompileClass()


def CompileClassVarDec():
    now = source[sp]
    if now.tag == "keyword" and now.content in ["field", "static", "int", "char", "boolean"]:
        addCode(now.text)
    elif now.tag == "identifier":
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
    now = source[sp]
    if now.tag == "identifier":
        addCode(now.text)
    elif now.tag == "keyword" and now.content in ["constructor", "function", "method"]:
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "(":
            addCode(now.text)
            callCompile("parameterList")
        elif now.content == ")":
            addCode(now.text)
        elif now.content == "{":
            callCompile("subroutineBody")
            return
    sp += 1
    CompileSubroutineDec()


def CompileParameterList():
    sp += 1
    now = source[sp]
    if now.tag == "keyword" and now.content in ["int", "char", "boolean"]:
        addCode(now.text)
    elif now.tag == "identifier":
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == ")":
            sp -= 1
            return
        elif now.content == ",":
            addCode(now.text)
    CompileParameterList()


def CompileSubroutineBody():
    now = source[sp]
    if now.tag == "symbol":
        if now.content == "{":
            addCode(now.text)
        elif now.content == "}":
            addCode(now.text)
            return
    elif now.tag == "keyword":
        if now.content == "var":
            callCompile("varDec")
        elif now.content in ["let", "do", "if", "while", "return"]:
            callCompile("statements")
    sp += 1
    CompileSubroutineBody()


def CompileVarDec():
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
        addCode(now.text)
    sp += 1
    CompileVarDec()


def CompileStatements():
    now = source[sp]
    if now.tag == "keyword" and now.content in ["if", "let", "do", "while", "return"]:
        callCompile(f"{now.content}Statement")
    elif now.tag == "symbol" and now.content == "}":
        return
    sp += 1
    CompileStatements()


def CompileLetStatement():
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
    now = source[sp]
    sp += 1
    next = source[sp + 1]
    if now.tag == "keyword" and now.content in ["if", "else"]:
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "(":
            callCompile("expression")
        elif now.content == ")":
            addCode(now.text)
        elif now.content == "{":
            callCompile("statements")
        elif now.content == "}":
            addCode(now.text)
            if next.tag != "keyword" or next.content != "else":
                return
    CompileIfStatement()


def CompileWhileStatement():
    now = source[sp]
    sp += 1
    if now.tag == "keyword" and now.content == "while":
        addCode(now.text)
    elif now.tag == "symbol":
        if now.content == "(":
            callCompile("expression")
        elif now.content == ")":
            addCode(now.text)
        elif now.content == "{":
            callCompile("statements")
        elif now.content == "}":
            addCode(now.text)
            return
    CompileWhileStatement()


def CompileDoStatement():
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
    now = source[sp]
    sp += 1
    next = source[sp + 1]
    if now.tag == "keyword" and now.content == "return":
        addCode(now.text)
        if next.tag == "symbol" or next.content == ";":
            addCode(next.text)
            return
        else:
            callCompile("expression")
    CompileReturnStatement()


def CompileExpression(f=False):
    now = source[sp]
    if now.tag == "symbol" and now.content in ["+", "-", "*", "/", "&", "|", "<", ">", "="] and f:
        addCode(now.text)
    elif now.tag == "symbol" and now.content in [";", ")", "]", "}", ","]:
        sp -= 1
        return
    else:
        callCompile("term")
    sp += 1
    CompileExpression(True)


def CompileExpressionList(f=False):
    now = source[sp]
    if now.tag == "symbol" and now.content == "," and f:
        addCode(now.text)
    elif now.tag == "symbol" and now.content == ")":
        return
    else:
        callCompile("expression")
    sp += 1
    CompileExpressionList(True)


def CompileTerm(f=False):
    now = source[sp]
    previous = source[sp - 1]
    sp += 1
    next = source[sp]
    if now.tag in ["integerConstant", "stringConstant"] or (now.tag == "keyword" and now.content in ["true", "false", "null", "this"]):
        addCode(now.text)
        sp -= 1
        return
    elif now.tag in "identifier":
        addCode(now.text)
        if next.tag != "symbol" or next.content not in ["(", ".", "["]:
            sp -= 1
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
            sp -= 1
            return
        elif now.content in ["-", "~"]:
            callCompile("term")
            sp -= 1
            return
    CompileTerm()
