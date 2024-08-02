from typing import NoReturn
from JackTokenizer import Token, Tokens


class CompilationEngine:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.code: list[str] = []
        self.point = 0
        self.now = self.tokens[0]
        self.gv = {}
        self.lv = {}
        self.varCount = {"static": 0, "field": 0, "argument": 0, "local": 0}

    def error(self, des: str, line: int) -> NoReturn:
        print(des, f"[line: {line}]")
        exit()

    def next(self) -> None:
        self.point += 1
        if self.point > len(self.tokens):
            self.error("Wrong end of file", self.tokens[-1].line)
        self.now = self.tokens[self.point - 1]

    def main(self) -> list[str]:
        self.compileClass()
        return self.code

    def compileClass(self) -> None:
        self.next()
        if self.now != Token("class", "keyword"):
            self.error("missing keyword 'class'", self.now.line)
        self.next()
        if self.now.type != "identifier":
            self.error(f"class name must be identifier, not {self.now.type}", self.now.line)
        self.class_name = self.now.content
        self.next()
        if self.now != Token("{", "symbol"):
            self.error("missing symbol '{'", self.now.line)
        self.next()
        while self.now == Tokens(["static", "field"], "keyword"):
            self.compileClassVarDec()
            self.next()
        while self.now == Tokens(["constructor", "function", "method"], "keyword"):
            self.compileSubroutine()
            self.next()
        if self.now != Token("}", "symbol"):
            self.error("bracket '}' is not closed", self.now.line)

    def compileClassVarDec(self) -> None:
        scope_type = self.now.content
        self.next()
        if self.now.type != "identifier" and self.now != Tokens(["int", "boolean", "char"], "keyword"):
            self.error("variable type must be int, boolean, char or identifier", self.now.line)
        var_type = self.now.content
        self.next()
        if self.now.type != "identifier":
            self.error(f"variable name must be identifier, not {self.now.type} '{self.now.content}'", self.now.line)
        self.gv[self.now.content] = [scope_type, var_type, self.varCount[scope_type]]
        self.varCount[scope_type] += 1
        self.next()
        while self.now != Token(";", "symbol"):
            if self.now != Token(",", "symbol"):
                self.error("missing symbol ','", self.now.line)
            self.next()
            if self.now.type != "identifier":
                self.error(f"variable name must be identifier, not {self.now.type} '{self.now.content}'", self.now.line)
            self.gv[self.now.content] = [scope_type, var_type, self.varCount[scope_type]]
            self.varCount[scope_type] += 1
            self.next()

    def compileSubroutine(self) -> None:
        pass

    def compileArgumentList(self) -> None:
        pass

    def compileVarDec(self) -> None:
        pass

    def compileStatements(self) -> None:
        pass

    def compileDo(self) -> None:
        pass

    def compileLet(self) -> None:
        pass

    def compileWhile(self) -> None:
        pass

    def compileReturn(self) -> None:
        pass

    def compileIf(self) -> None:
        pass

    def compileExpression(self) -> None:
        pass

    def compileTerm(self) -> None:
        pass

    def compileExpressionList(self) -> None:
        pass
