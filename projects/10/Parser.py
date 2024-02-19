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

    def addCode(self, text: str):
        self.CodeList.append("  " * self.ia + text)

    def Compile(self):
        self.addCode("<class>")
        self.ia += 1
        self.CompileClass()
        self.ia -= 1
        self.addCode("</class>")
        return self.CodeList

    def CompileClass(self):
        now = self.source[self.sp]
        next = self.source[self.sp]
        if now.tag == "keyword" and now.content == "class":
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == "{" and next.tag == "keyword":
                self.addCode(now.text)
            elif now.content == "}":
                self.addCode(now.text)
                return
        if now.content in ["field", "static"]:
            self.addCode("<classVarDec>")
            self.ia += 1
            self.CompileClassVarDec()
            self.ia -= 1
            self.addCode("</classVarDec>")
        elif now.content in ["constructor", "function", "method"]:
            self.addCode("<subroutineDec>")
            self.ia += 1
            self.CompileSubroutineDec()
            self.ia -= 1
            self.addCode("</subroutineDec>")
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
                self.addCode("<parameterList>")
                self.ia += 1
                self.sp += 1
                self.CompileParameterList()
                self.ia -= 1
                self.addCode("</paprameterList>")
            elif now.content == ")":
                self.addCode(now.text)
            elif now.content == "{":
                self.addCode("<subroutineBody>")
                self.ia += 1
                self.CompileSubroutineBody()
                self.ia -= 1
                self.addCode("</subroutineBody>")
                return
        self.sp += 1
        self.CompileSubroutineDec()

    def CompileParameterList(self):
        now = self.source[self.sp]
        if now.tag == "keyword" and now.content in ["int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ")":
                return
            elif now.content == ",":
                self.addCode(now.text)
        self.sp += 1
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
                self.addCode("<varDec>")
                self.ia += 1
                self.CompileVarDec()
                self.ia -= 1
                self.addCode("</varDec>")
            elif now.content in ["let","do","if","while","return"]:
                self.addCode("<statements>")
                self.ia += 1
                self.CompileStatements()
                self.ia -= 1
                self.addCode("</statements>")
        self.sp += 1
        self.CompileSubroutineBody()

    def CompileVarDec(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileVarDec()

    def CompileStatements(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileStatements()

    def CompileLetStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileLetStatement()

    def CompileIfStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileIfStatement()

    def CompileWhileStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileWhileStatement()

    def CompileDoStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileDoStatement()

    def CompileReturnStatement(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileReturnStatement()

    def CompileSubroutineCall(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileSubroutineCall()

    def CompileExpression(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileExpression()

    def CompileExpressionList(self):
        now = self.source[self.sp]
        self.sp += 1
        self.CompileExpressionList()
