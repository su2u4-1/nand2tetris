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
    return code


class Compiler:
    def __init__(self, text: list[xml]):
        self.source = text
        self.CodeList = []
        self.ia = 0
        self.f = ["class"]

    def addCode(self, text: str):
        self.CodeList.append("  " * self.ia + text)

    def Compile(self):
        for i in range(len(self.source)):
            if self.source[i].text == "<end> exit </end>":
                break
            match self.f[-1]:
                case "class":
                    self.CompileClass(self.source[i], self.source[i + 1])
                case "classVarDec":
                    self.CompileClassVarDec(self.source[i], self.source[i + 1])
                case "subroutineDec":
                    self.CompileSubroutineDec(self.source[i], self.source[i + 1])
                case "parameterList":
                    self.CompileParameterList(self.source[i], self.source[i + 1])
                case "subroutineBody":
                    self.CompileSubroutineBody(self.source[i], self.source[i + 1])
                case "statements":
                    self.CompileStatements(self.source[i], self.source[i + 1])
                case "letStatement":
                    self.CompileLetStatement(self.source[i], self.source[i + 1])
                case "ifStatement":
                    self.CompileIfStatement(self.source[i], self.source[i + 1])
                case "whileStatement":
                    self.CompileWhileStatement(self.source[i], self.source[i + 1])
                case "doStatement":
                    self.CompileDoStatement(self.source[i], self.source[i + 1])
                case "returnStatement":
                    self.CompileReturnStatement(self.source[i], self.source[i + 1])
                case "expression":
                    self.CompileExpression(self.source[i], self.source[i + 1])
                case "expression1":
                    self.CompileExpression(self.source[i - 1], self.source[i])
                case "subroutineCall":
                    self.CompileSubroutineCall(self.source[i], self.source[i + 1])
                case _:
                    print("exit")
                    for j in self.CodeList:
                        print(j)
                    exit()
        return self.CodeList

    def CompileClass(self, now: xml, next: xml):
        if now.tag == "keyword":
            if now.content == "class":
                self.CodeList.append("<class>")
                self.ia += 1
                self.addCode(now.text)
            elif now.content == "field":
                self.addCode("<classVarDec>")
                self.ia += 1
                self.f.append("classVarDec")
                self.addCode(now.text)
            elif now.content in ["function", "method", "constructor"]:
                self.addCode("<subroutineDec>")
                self.ia += 1
                self.f.append("subroutineDec")
                self.addCode(now.text)
            else:
                print(f"CompileClass keyword error: {now.text}")
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif next.tag == "end" and next.content == "exit":
            self.CodeList.append("</class>")
        else:
            print(f"CompileClass error: {now.text}")

    def CompileClassVarDec(self, now: xml, next: xml):
        if now.tag == "keyword" and now.content in ["field", "int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ",":
                self.addCode(now.text)
            elif now.content == ";":
                self.addCode(now.text)
                self.ia -= 1
                self.f.pop()
            else:
                print(f"CompileClassVarDec symbol error: {now.text}")
        else:
            print(f"CompileClassVarDec error: {now.text}")

    def CompileSubroutineDec(self, now: xml, next: xml):
        if now.tag == "symbol":
            if now.content == "(":
                self.addCode(now.text)
                self.addCode("<parameterList>")
                self.ia += 1
                self.f.append("parameterList")
            elif now.content == "{":
                self.addCode("<subroutineBody>")
                self.ia += 1
                self.f.append("subroutineBody")
                self.addCode(now.text)
            elif now.content == "}":
                self.ia -= 1
                self.f.pop()
                self.addCode("</subroutineDec>")
                self.addCode(now.text)
            else:
                print(f"CompileSubroutineDec symbol error: {now.text}")
        elif now.tag == "keyword" and now.content in ["function", "method", "constructor", "int", "char", "boolean", "void"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        else:
            print(f"CompileSubroutineDec error: {now.text}")

    def CompileParameterList(self, now: xml, next: xml):
        if now.tag == "symbol":
            if now.content == ")":
                self.ia -= 1
                self.f.pop()
                self.addCode("</parameterList>")
                self.addCode(now.text)
            elif now.content == ",":
                self.addCode(now.text)
            else:
                print(f"CompileParameterList symbol error: {now.text}")
        elif now.tag == "keyword" and now.content in ["int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)
        else:
            print(f"CompileParameterList error: {now.text}")

    def CompileSubroutineBody(self, now: xml, next: xml):
        if now.tag == "symbol":
            if now.content == "}":
                self.addCode(now.text)
                self.ia -= 1
                self.f.pop()
                self.addCode("</subroutineBody>")
            elif now.content == "{":
                self.addCode(now.text)
                self.addCode("<statements>")
                self.ia += 1
                self.f.append("statements")
            else:
                print(f"CompilerSubroutineBody symbol error: {now.text}")
        elif now.tag == "keyword" and now.content == "var":
            self.addCode("<varDec>")
            self.ia += 1
            self.f.append("varDec")
            self.addCode(now.text)
        else:
            print(f"CompileSubroutineBody error: {now.text}")

    def CompileVarDec(self, now: xml, next: xml):
        if now.tag == "keyword" and now.content in ["var", "int", "char", "boolean"]:
            self.addCode(now.text)
        elif now.tag == "symbol":
            if now.content == ",":
                self.addCode(now.text)
            elif now.content == ";":
                self.addCode(now.text)
                self.ia -= 1
                self.f.pop()
                self.addCode("</varDec>")
            else:
                print(f"CompileVarDec symbol error: {now.text}")
        elif now.tag == "identifier":
            self.addCode(now.text)
        else:
            print(f"CompileVarDec error: {now.text}")

    def CompileStatements(self, now: xml, next: xml):
        if now.tag == "keyword" and now.content in ["let", "if", "while", "do", "return"]:
            self.addCode(f"<{now.content}Statement>")
            self.ia += 1
            self.f.append(f"{now.content}Statement")
            self.addCode(now.text)
        elif now.tag == "symbol" and now.content == "}":
            self.ia -= 1
            self.f.pop()
            self.addCode("</statements>")
            self.addCode(now.text)
        else:
            print(f"CompileStatements error: {now.text}")

    def CompileLetStatement(self, now: xml, next: xml):
        if now.tag == "identifier":
            self.addCode(now.text)
        elif now.tag == "synbol":
            if now.content in ["[", "="]:
                self.addCode(now.text)
                self.addCode("<expression>")
                self.ia += 1
                self.f.append("expression")
            elif now.content == ";":
                self.addCode(now.text)
                self.ia -= 1
                self.f.pop()
                self.addCode("</letStatement>")

    def CompileIfStatement(self, now: xml, next: xml):
        if now.tag == "symbol":
            if now.content == "(":
                self.addCode(now.text)
                self.addCode("<expression>")
                self.ia += 1
                self.f.append("expression")
            elif now.content == "{":
                self.addCode(now.text)
                self.addCode("<statements>")
                self.ia += 1
                self.f.append("statements")
            elif now.content == "}":
                if next.tag == "keyword" and next.content == "else":
                    self.addCode(now.text)
        elif now.tag == "keyword" and now.content == "else":
            self.addCode(now.text)

    def CompileWhileStatement(self, now: xml, next: xml):
        pass

    def CompileDoStatement(self, now: xml, next: xml):
        if now.tag == "symbol" and now.content == ";":
            self.addCode(now.text)
            self.ia -= 1
            self.f.pop()
            self.addCode("</doStatement>")
        elif now.tag == "identifier":
            self.addCode(now.text)
            self.f.append("subroutineCall")

    def CompileReturnStatement(self, now: xml, next: xml):
        if now.tag == "symbol" and now.content == ";":
            self.addCode(now.text)
            self.ia -= 1
            self.f.pop()
            self.addCode("</returnStatement>")
        else:
            self.addCode("<expression>")
            self.ia += 1
            self.f.append("expression1")

    def CompileSubroutineCall(self, now: xml, next: xml):
        if now.tag == "symbol":
            if now.content == ".":
                self.addCode(now.text)
            elif now.content == "(":
                self.addCode(now.text)
                self.addCode("<expressionList>")
                self.ia += 1
                self.f.append("expressionList")
            elif now.content == ")":
                self.addCode(now.text)
                self.f.pop()
        elif now.tag == "identifier":
            self.addCode(now.text)

    def CompileExpression(self, now: xml, next: xml):
        pass

    def CompileExpressionList(self, now: xml, next: xml):
        pass
