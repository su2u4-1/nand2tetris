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


class Compiler:
    def __init__(self, text: list[xml]):
        self.source = text
        self.CodeList = []
        self.ia = 0
        self.f = "class"

    def addCode(self, text: str):
        self.CodeList.append("  " * self.ia + text)

    def Compile(self):
        for i in range(len(self.source)):
            if self.source[i].text == "<end> exit </end>":
                break
            match self.f:
                case "class":
                    self.CompilerClass(self.source[i], self.source[i + 1])
                case "subroutineDec":
                    self.ComplierSubroutineDec(self.source[i], self.source[i + 1])
                case "parameterList":
                    self.CompilerParameterList(self.source[i], self.source[i + 1])
                case "subroutineBody":
                    self.CompilerSubroutineBody(self, self.source[i], self.source[i + 1])

    def CompilerClass(self, now: xml, next: xml):
        if now.tag == "keyword" and now.content == "class":
            self.CodeList.append("<class>")
            self.ia += 1
            self.addCode(now.text)
        elif now.tag == "symbol" and now.content == "{":
            self.addCode(now.text)
            self.addCode("<subroutineDec>")
            self.ia += 1
            self.f = "subroutineDec"
        elif now.tag == "identifier":
            self.addCode(now.text)
        elif next.tag == "end" and next.content == "exit":
            self.CodeList.append("</class>")

    def ComplierSubroutineDec(self, now: xml, next: xml):
        if now.tag == "symbol":
            if now.content == "(":
                self.addCode(now.text)
                self.addCode("<parameterList>")
                self.ia += 1
                self.f = "parameterList"
            elif now.content == "{":
                self.addCode("<subroutineBody>")
                self.addCode(now.text)
                self.ia += 1
                self.f = "subroutineBody"
            elif now.content == "}":
                self.ia -= 1
                self.f = "class"
                self.addCode("</subroutineDec>")
                self.addCode(now.text)
        elif now.tag == "keyword" and now.content in ["function", "method", "constructor", "int", "char", "boolean", "void"]:
            self.addCode(now.text)
        elif now.tag == "identifier":
            self.addCode(now.text)

    def CompilerParameterList(self, now: xml, next: xml):
        pass

    def CompilerSubroutineBody(self, now: xml, next: xml):
        pass
