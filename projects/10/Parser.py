import re

symbolL = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
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
opList = [
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


class xml:
    def __init__(self, text: str, tag: str):
        self.content = text
        self.text = f"<{tag}> {text} </{tag}>"
        self.tag = tag


def grammarAnalyzer(text: list):
    for i in range(len(text)):
        text[i] = xml(text[i][0], text[i][1])
    text.append(xml("exit", "end"))
    compile = Compiler(text)
    code = compile.Compile()
    for i in code:
        print(i)
    return code


class Compiler:
    def __init__(self, text: list[xml]):
        self.source = text
        self.CodeList = []
        self.ia = 0
        self.sp = 0

    def callCompile(self, tag: str):
        print(self.sp, self.source[self.sp].content, tag)
        if self.sp >= 305:
            for i in self.CodeList:
                print(i)
            exit()
        self.addCode(f"<{tag}>")
        self.ia += 1
        match tag:
            case "class":
                self.CompileClass()
            case "classVarDec":
                self.CompileClassVarDec()
            case "subroutineDec":
                self.CompileSubroutineDec()
            case "parameterList":
                self.CompileParameterList()
            case "subroutineBody":
                self.CompileSubroutineBody()
            case "varDec":
                self.CompileVarDec()
            case "statements":
                self.CompileStatements()
            case "letStatement":
                self.CompileLetStatement()
            case "ifStatement":
                self.CompileIfStatement()
            case "whileStatement":
                self.CompileWhileStatement()
            case "doStatement":
                self.CompileDoStatement()
            case "returnStatement":
                self.CompileReturnStatement()
            case "expression":
                self.CompileExpression()
            case "expressionList":
                self.CompileExpressionList()
            case "term":
                self.CompileTerm()
        self.ia -= 1
        self.addCode(f"</{tag}>")

    def addCode(self, text: str):
        self.CodeList.append("  " * self.ia + text)

    def Compile(self):
        self.callCompile("class")
        return self.CodeList

    def CompileClass(self):
        now = self.source[self.sp]
        next = self.source[self.sp]
        if now.tag == "keyword" and now.content == "class":
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == "{":
                self.addCode(now.text)
            elif now.content == "}":
                self.addCode(now.text)
                return
        if now.content in ["field", "static"]:
            self.callCompile("classVarDec")
        elif now.content in ["constructor", "function", "method"]:
            self.callCompile("subroutineDec")
        self.sp += 1
        self.CompileClass()

    def CompileClassVarDec(self):
        now = self.source[self.sp]
        if now.tag == "keyword" and now.content in ["field", "static", "int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ",":
                self.addCode(now.text)
            elif now.content == ";":
                self.addCode(now.text)
                return
        self.sp += 1
        self.CompileClassVarDec()

    def CompileSubroutineDec(self):
        now = self.source[self.sp]
        if now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "keyword" and now.content in ["constructor", "function", "method"]:
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == "(":
                self.addCode(now.text)
                self.callCompile("parameterList")
            elif now.content == ")":
                self.addCode(now.text)
            elif now.content == "{":
                self.callCompile("subroutineBody")
                return
        self.sp += 1
        self.CompileSubroutineDec()

    def CompileParameterList(self):
        self.sp += 1
        now = self.source[self.sp]
        if now.tag == "keyword" and now.content in ["int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ")":
                self.sp -= 1
                return
            elif now.content == ",":
                self.addCode(now.text)
        self.CompileParameterList()

    def CompileSubroutineBody(self):
        now = self.source[self.sp]
        if now.tag == "symbol":
            if now.content == "{":
                self.addCode(now.text)
            elif now.content == "}":
                self.addCode(now.text)
                return
        elif now.tag == "keyword":
            if now.content == "var":
                self.callCompile("varDec")
            elif now.content in ["let", "do", "if", "while", "return"]:
                self.callCompile("statements")
        self.sp += 1
        self.CompileSubroutineBody()

    def CompileVarDec(self):
        now = self.source[self.sp]
        if now.tag == "keyword" and now.content in ["var", "int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ",":
                self.addCode(now.text)
            elif now.content == ";":
                self.addCode(now.text)
                return
        elif now.tag == "identifier":
            self.addCode(now.text)
        self.sp += 1
        self.CompileVarDec()

    def CompileStatements(self):
        now = self.source[self.sp]
        if now.tag == "keyword" and now.content in ["if", "let", "do", "while", "return"]:
            self.callCompile(f"{now.content}Statement")
        elif now.tag == "symbol" and now.content == "}":
            return
        self.sp += 1
        self.CompileStatements()

    def CompileLetStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        if now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "keyword" and now.content == "let":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ",":
                self.addCode(now.text)
            elif now.content == ";":
                self.addCode(now.text)
                self.sp -= 1
                return
            elif now.content == "[":
                self.addCode(now.text)
                self.callCompile("expression")
            elif now.content == "]":
                self.addCode(now.text)
            elif now.content == "=":
                self.addCode(now.text)
                self.callCompile("expression")
        self.CompileLetStatement()

    def CompileIfStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        next = self.source[self.sp + 1]
        if now.tag == "keyword" and now.content in ["if", "else"]:
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == "(":
                self.callCompile("expression")
            elif now.content == ")":
                self.addCode(now.text)
            elif now.content == "{":
                self.callCompile("statements")
            elif now.content == "}":
                self.addCode(now.text)
                if next.tag != "keyword" or next.content != "else":
                    return
        self.CompileIfStatement()

    def CompileWhileStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        if now.tag == "keyword" and now.content == "while":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == "(":
                self.callCompile("expression")
            elif now.content == ")":
                self.addCode(now.text)
            elif now.content == "{":
                self.callCompile("statements")
            elif now.content == "}":
                self.addCode(now.text)
                return
        self.CompileWhileStatement()

    def CompileDoStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        if now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "keyword" and now.content == "do":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ";":
                self.addCode(now.text)
                return
            elif now.content in [".", ")"]:
                self.addCode(now.text)
            elif now.content == "(":
                self.addCode(now.text)
                self.callCompile("expressionList")
        self.CompileDoStatement()

    def CompileReturnStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        next = self.source[self.sp + 1]
        if now.tag == "keyword" and now.content == "return":
            self.addCode(now.text)
            if next.tag == "symbol" or next.content == ";":
                self.addCode(next.text)
                return
            else:
                self.callCompile("expression")
        self.CompileReturnStatement()

    def CompileExpression(self, f=False):
        now = self.source[self.sp]
        if now.tag == "symbol" and now.content in ["+", "-", "*", "/", "&", "|", "<", ">", "="] and f:
            self.addCode(now.text)
        elif now.tag == "symbol" and now.content in [";", ")", "]", "}", ","]:
            self.sp -= 1
            return
        else:
            self.callCompile("term")
        self.sp += 1
        self.CompileExpression(True)

    def CompileExpressionList(self, f=False):
        now = self.source[self.sp]
        if now.tag == "symbol" and now.content == "," and f:
            self.addCode(now.text)
        elif now.tag == "symbol" and now.content == ")":
            return
        else:
            self.callCompile("expression")
        self.sp += 1
        self.CompileExpressionList(True)

    def CompileTerm(self, f=False):
        now = self.source[self.sp]
        previous = self.source[self.sp - 1]
        self.sp += 1
        next = self.source[self.sp]
        if now.tag in ["integerConstant", "stringConstant"] or (
            now.tag == "keyword" and now.content in ["true", "false", "null", "this"]
        ):
            self.addCode(now.text)
            self.sp -= 1
            return
        elif now.tag in "identifier":
            self.addCode(now.text)
            if next.tag != "symbol" or next.content not in ["(", ".", "["]:
                self.sp -= 1
                return
        elif now.tag == "symbol" and now.content in ["(", ")", "[", "]", "-", "~", "."]:
            self.addCode(now.text)
            if now.content == "(":
                if previous.tag == "identifier":
                    self.callCompile("expressionList")
                else:
                    self.callCompile("expression")
            elif now.content == "[":
                self.callCompile("expression")
            elif now.content in ["]", ")"]:
                self.sp -= 1
                return
            elif now.content in ["-", "~"]:
                self.callCompile("term")
                self.sp -= 1
                return
        self.CompileTerm()
