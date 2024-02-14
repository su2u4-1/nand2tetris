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


def xmlTag(text, tag):
    return f"<{tag}> {text} </{tag}>"


def equalTag(text, tag):
    return text.startswith(f"<{tag}>") and text.endswith(f"</{tag}>")


# 移除列表裡的特定元素
def removeE(l, e):
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
    for i in text:
        pass