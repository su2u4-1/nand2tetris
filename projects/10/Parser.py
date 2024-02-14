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


# 移除列表裡的特定元素
def removeE(l: list, e):
    t = []
    if type(e) == list:
        e = set(e)
        for i in l:
            if i not in e:
                t.append(i)
    else:
        for i in l:
            if i != e:
                t.append(i)
    return t


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

    def Compile(self):
        for i in range(len(self.source)):
            if self.source[i].text == "<end> exit </end>":
                break
            if self.f == "class":
                self.CompilerClass(self.source[i], self.source[i + 1])
            elif self.f == "subroutineDec":
                self.ComplierSubroutineDec(self.source[i], self.source[i + 1])

    def CompilerClass(self, now: xml, next: xml):
        if now.tag == "keyword" and now.content == "class":
            self.CodeList.append("<class>")
            self.ia += 1
            self.CodeList.append("  " * self.ia + now.text)
        elif now.tag == "symbol" and now.content == "{":
            self.CodeList.append("  " * self.ia + now.text)
            self.CodeList.append("<subroutineDec>")
            self.ia += 1
            self.f = "subroutineDec"
        elif now.tag == "symbol" and now.content == "}":
            self.ia -= 1
            self.f = "class"
            self.CodeList.append("  " * self.ia + now.text)
            self.CodeList.append("</subroutineDec>")
        elif now.tag == "identifier":
            self.CodeList.append("  " * self.ia + now.text)
        elif next.tag == "end" and next.content == "exit":
            self.CodeList.append("</class>")

    def ComplierSubroutineDec(self, now: xml, next: xml):
        pass
