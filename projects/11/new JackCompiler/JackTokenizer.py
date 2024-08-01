from typing import Literal, Self

symbolList = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
keywordList = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "Int", "Char", "Boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
identifier = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Token:
    def __init__(self, content: str, type: Literal["keyword", "symbol", "string", "integer", "identifier"], line: int = -1) -> None:
        self.content = content
        self.type = type
        self.line = line

    def __eq__(self, other: Self) -> bool:
        return self.type == other.type and self.content == other.content

    def __str__(self) -> str:
        return f"<{self.type}> {self.content} [line: {self.line}]"


class Tokens:
    def __init__(self, content: list[str], type: Literal["keyword", "symbol", "string", "integer", "identifier"]) -> None:
        self.content = content
        self.type = type

    def __eq__(self, other: Token) -> bool:
        if self.type != other.type:
            return False
        for i in self.content:
            if i == other.content:
                return True
        return False


def is_integer(w: str) -> bool:
    if len(w) >= 1 and w[0] in "123456789":
        for i in w:
            if i not in "0123456789":
                return False
        else:
            return True
    elif w == "0":
        return True
    return False


def is_identifier(w: str) -> bool:
    if len(w) >= 1 and w[0] in identifier:
        for i in w:
            if i not in identifier + "0123456789":
                return False
        else:
            return True
    return False


def tokenizer(source: list[str]):
    def addcode(t):
        if len(t) > 0:
            if t in symbolList:
                code.append(Token(t, "symbol", line))
            elif t in keywordList:
                code.append(Token(t, "keyword", line))
            elif is_integer(t):
                code.append(Token(t, "integer", line))
            elif is_identifier(t):
                code.append(Token(t, "identifier", line))
            else:
                error.append((f"wrong identifier '{t}'", line))

    fs = False
    fc = False
    ts = ""
    tc = ""
    tw = ""
    error: list[tuple[str, int]] = []
    code: list[Token] = []

    for line, i in enumerate(source):
        for c in i:
            if tw.endswith("/"):
                addcode(tw[:-1])
                tw = ""
                if c == "/":
                    break
                elif c == "*":
                    fc = True
                else:
                    code.append(Token("/", "symbol", line))
            if fs:
                if c == '"':
                    if "\n" in ts:
                        error.append(("The string cannot contain newlines", line))
                    if '"' in ts:
                        error.append((f"The string cannot contain '{'"'}'", line))
                    code.append(Token(ts, "string", line))
                    fs = False
                    ts = ""
                else:
                    ts += c
            elif fc:
                if tc == "*" and c == "/":
                    fc = False
                tc = c
            elif c == '"':
                if len(tw) > 0:
                    error.append(("The string cannot be preceded by identifiers or keywords", line))
                    addcode(tw)
                fs = True
                ts = ""
            elif c == " " or c == "\n":
                addcode(tw)
                tw = ""
            elif c in symbolList and c != "/":
                addcode(tw)
                tw = ""
                code.append(Token(c, "symbol", line))
            else:
                tw += c

    if fs:
        error.append(("String is not closed", line))
    if fc:
        error.append(("Comment is not closed", line))
    if len(tw) > 0:
        addcode(tw)
    if len(error) > 0:
        for i in error:
            print(i[0], f"[line: {i[1]+1}]")
            print("source:", source[i[1]])
        exit()

    return code
