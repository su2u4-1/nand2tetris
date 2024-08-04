from typing import NoReturn
from JackTokenizer import Token, Tokens


class CompilationEngine:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.code: list[str] = []
        self.point = 0
        self.now = self.tokens[0]
        self.gv: dict[str, tuple[str, int, str]] = {}
        self.lv: dict[str, tuple[str, int, str]] = {}
        self.varCount: dict[str, int] = {"static": 0, "this": 0, "argument": 0, "local": 0}
        self.whileCount = 0
        self.ifCount = 0

    def error(self, des: str, line: int = -1) -> NoReturn:
        if line == -1:
            line = self.now.line
        print(des, f"[line: {line + 1}]")
        exit()

    def next(self) -> Token:
        self.point += 1
        if self.point > len(self.tokens):
            self.error("Wrong end of file", self.tokens[-1].line)
        self.now = self.tokens[self.point - 1]
        return self.now

    def main(self) -> list[str]:
        self.compileClass()
        return self.code

    def compileClass(self) -> None:
        if self.next() != Token("class", "keyword"):
            self.error("missing keyword 'class'")
        if self.next().type != "identifier":
            self.error(f"class name must be identifier, not {self.now.type}")
        self.class_name = self.now.content
        if self.next() != Token("{", "symbol"):
            self.error("missing symbol '{'")
        while self.next() == Tokens(["static", "field"], "keyword"):
            self.compileClassVarDec()
        while self.next() == Tokens(["constructor", "function", "method"], "keyword"):
            self.compileSubroutine()
        if self.now != Token("}", "symbol"):
            self.error("bracket '}' is not closed")

    def compileClassVarDec(self) -> None:
        scope_type = self.now.content
        if scope_type == "field":
            scope_type = "this"
        if self.next().type != "identifier" and self.now != Tokens(["int", "boolean", "char"], "keyword"):
            self.error("variable type must be int, boolean, char or identifier")
        var_type = self.now.content
        if self.next().type != "identifier":
            self.error(f"variable name must be identifier, not {self.now.type} '{self.now.content}'")
        self.gv[self.now.content] = (scope_type, self.varCount[scope_type], var_type)
        self.varCount[scope_type] += 1
        while self.next() != Token(";", "symbol"):
            if self.now != Token(",", "symbol"):
                self.error("missing symbol ','")
            if self.next().type != "identifier":
                self.error(f"variable name must be identifier, not {self.now.type} '{self.now.content}'")
            self.gv[self.now.content] = (scope_type, self.varCount[scope_type], var_type)
            self.varCount[scope_type] += 1

    def compileSubroutine(self) -> None:
        subroutine_type = self.now.content
        if subroutine_type == "constructor":
            self.code.append(f"push constant {self.varCount["this"]}")
            self.code.append("call Memory.alloc 1")
            self.code.append("pop pointer 0")
        elif subroutine_type == "method":
            self.code.append("push argument 0")
            self.code.append("pop pointer 0")
        if self.next().type != "identifier" and self.now != Tokens(["int", "boolean", "char", "void"], "keyword"):
            self.error(f"subroutine {subroutine_type} return type must be int, boolean, char, void or identifier")
        return_type = self.now.content
        if self.next().type != "identifier":
            self.error(f"subroutine {subroutine_type} name must be identifier, not {self.now.type} '{self.now.content}'")
        subroutine_name = self.now.content
        self.subroutine_info = (subroutine_type, return_type, subroutine_name)
        if self.next() != Token("(", "symbol"):
            self.error("missing symbol '('")
        self.compileArgumentList()
        if self.now != Token(")", "symbol"):
            self.error("missing symbol ')'")
        if self.next() != Token("{", "symbol"):
            self.error("missing symbol '{'")
        while self.next() == Token("var", "keyword"):
            self.compileVarDec()
        self.compileStatements()
        if self.now != Token("}", "symbol"):
            self.error("Brackets { are not closed")

    def compileArgumentList(self) -> None:
        if self.next().type != "identifier" and self.now != Tokens(["int", "boolean", "char"], "keyword"):
            self.error("argument type must be int, boolean, char or identifier")
        var_type = self.now.content
        if self.next().type != "identifier":
            self.error("argument name must be identifier")
        self.lv[self.now.content] = ("argument", self.varCount["argument"], var_type)
        self.varCount["argument"] += 1
        while self.next() == Token(",", "symbol"):
            if self.next().type != "identifier" and self.now != Tokens(["int", "boolean", "char"], "keyword"):
                self.error("argument type must be int, boolean, char or identifier")
            var_type = self.now.content
            if self.next().type != "identifier":
                self.error("argument name must be identifier")
            self.lv[self.now.content] = ("argument", self.varCount["argument"], var_type)
            self.varCount["argument"] += 1

    def compileVarDec(self) -> None:
        if self.next().type != "identifier" and self.now != Tokens(["int", "boolean", "char"], "keyword"):
            self.error("variable type must be int, boolean, char or identifier")
        var_type = self.now.content
        if self.next().type != "identifier":
            self.error("variable name must be identifier")
        self.lv[self.now.content] = ("local", self.varCount["local"], var_type)
        self.varCount["local"] += 1
        while self.next() == Token(",", "symbol"):
            if self.next().type != "identifier":
                self.error("variable name must be identifier")
            self.lv[self.now.content] = ("local", self.varCount["local"], var_type)
            self.varCount["local"] += 1
        if self.now != Token(";", "symbol"):
            self.error("missing symbol ';'")

    def compileStatements(self) -> None:
        while self.next() != Token("}", "symbol"):
            if self.now == Token("do", "keyword"):
                self.compileDo()
            elif self.now == Token("let", "keyword"):
                self.compileLet()
            elif self.now == Token("while", "keyword"):
                self.compileWhile()
            elif self.now == Token("return", "keyword"):
                self.compileReturn()
            elif self.now == Token("if", "keyword"):
                self.compileIf()
            else:
                self.error("statement must start with keyword 'do', 'let', 'while', 'return' or 'if'")

    def compileDo(self) -> None:
        if self.next().type != "identifier":
            self.error("keyword 'do' must be followed by identifier")
        if self.now.content in self.lv:
            t = self.lv[self.now.content]
        elif self.now.content in self.gv:
            t = self.lv[self.now.content]
        else:
            t = (self.now.content, -1, self.class_name)
        if self.next() == Token(".", "symbol"):
            if t[1] != -1:
                self.code.append(f"push {t[0]} {t[1]}")
            if self.next().type != "identifier":
                self.error("subroutine name must be identifier")
            t1 = self.now.content
            if self.next() != Token("(", "symbol"):
                self.error("missing symbol '('")
            n = self.compileExpressionList()
            if self.next() != Token(")", "symbol"):
                self.error("missing symbol ')'")
            if t[1] == -1:
                self.code.append(f"call {t[0]}.{t1} {n}")
            else:
                self.code.append(f"call {t[1]}.{t1} {n+1}")
        elif self.now == Token("(", "symbol"):
            if t[1] != -1:
                self.error(f"variable '{t[0]}' not callable")
            self.code.append("push pointer 0")
            n = self.compileExpressionList()
            if self.next() != Token(")", "symbol"):
                self.error("missing symbol ')'")
            self.code.append(f"call {t[1]}.{t[0]} {n+1}")
        else:
            self.error("identifier must be followed by symbol '(' or '.'")
        if self.next() != Token(";", "symbol"):
            self.error("missing symbol ';'")
        self.code.append("pop temp 0")

    def compileLet(self) -> None:
        if self.next().type != "identifier":
            self.error("keyword 'let' must be followed by identifier")
        if self.now.content in self.lv:
            t = self.lv[self.now.content]
        elif self.now.content in self.gv:
            t = self.gv[self.now.content]
        else:
            self.error(f"identifier '{self.now.content}' not found")
        if self.next() == Token("=", "symbol"):
            self.compileExpression()
            self.code.append(f"pop {t[0]} {t[1]}")
        elif self.now == Token("[", "symbol"):
            self.compileExpression()
            self.code.append(f"push {t[0]} {t[1]}")
            self.code.append("add")
            self.code.append("pop temp 0")
            if self.now != Token("]", "symbol"):
                self.error("missing symbol ']'")
            if self.next() != Token("=", "symbol"):
                self.error("missing symbol '='")
            self.compileExpression()
            self.code.append("push temp 0")
            self.code.append("pop pointer 1")
            self.code.append("pop that 0")
        if self.now != Token(";", "symbol"):
            self.error("missing symbol ';'")

    def compileWhile(self) -> None:
        nowCount = self.whileCount
        self.whileCount += 1
        if self.next() != Token("(", "symbol"):
            self.error("keyword 'while' must be followed by symbol '('")
        self.code.append(f"label while-{nowCount}-1")
        self.compileExpression()
        self.code.append(f"not")
        self.code.append(f"if-goto while-{nowCount}-2")
        if self.now != Token(")", "symbol"):
            self.error("missing symbol ')'")
        if self.next() != Token("{", "symbol"):
            self.error("missing symbol '{'")
        self.compileStatements()
        self.code.append(f"goto while-{nowCount}-1")
        self.code.append(f"label while-{nowCount}-2")
        if self.next() != Token("}", "symbol"):
            self.error("missing symbol '}'")

    def compileReturn(self) -> None:
        self.compileExpression()
        if self.now != Token(";", "symbol"):
            self.error("missing symbol ';'")

    def compileIf(self) -> None:
        pass

    def compileExpression(self) -> None:
        self.compileTerm()
        while self.now == Tokens(["+", "-", "*", "/", "<", ">", "=", "&", "|"], "symbol"):
            if self.now == Token("+", "symbol"):
                t = "add"
            elif self.now == Token("-", "symbol"):
                t = "sub"
            elif self.now == Token("*", "symbol"):
                t = "call Math.multiply 2"
            elif self.now == Token("/", "symbol"):
                t = "call Math.divide 2"
            elif self.now == Token("&", "symbol"):
                t = "and"
            elif self.now == Token("|", "symbol"):
                t = "or"
            elif self.now == Token(">", "symbol"):
                t = "gt"
            elif self.now == Token("<", "symbol"):
                t = "lt"
            elif self.now == Token("=", "symbol"):
                t = "eq"
            self.compileTerm()
            self.code.append(t)

    def compileTerm(self) -> None:
        if self.next().type == "integer":
            self.code.append(f"push constant {self.now.content}")
        elif self.now == Token("true", "keyword"):
            self.code.append("push constant 0")
            self.code.append("not")
        elif self.now == Token("false", "keyword"):
            self.code.append("push constant 0")
        elif self.now == Token("this", "keyword"):
            self.code.append("push constant 0")
        elif self.now == Token("null", "keyword"):
            self.code.append("push pointer 0")
        elif self.now == Token("-", "symbol"):
            self.compileTerm()
            self.code.append("not")
        elif self.now == Token("~", "symbol"):
            self.compileTerm()
            self.code.append("neg")
        elif self.now == Token("(", "symbol"):
            self.compileExpression()
            if self.now != Token(")", "symbol"):
                self.error("missing symbol ')'")
        elif self.now.type == "string":
            self.code.append(f"push constant {len(self.now.content)}")
            self.code.append("call String.new 1")
            for i in self.now.content:
                self.code.append(f"push constant {ord(i)}")
                self.code.append("call String.appendChar 2")
        elif self.now.type == "identifier":
            if self.now.content in self.lv:
                t = self.lv[self.now.content]
            elif self.now.content in self.gv:
                t = self.lv[self.now.content]
            else:
                t = (self.now.content, -1, self.class_name)
            if self.next() == Token(".", "symbol"):
                if t[1] != -1:
                    self.code.append(f"push {t[0]} {t[1]}")
                if self.next().type != "identifier":
                    self.error("subroutine name must be identifier")
                t1 = self.now.content
                if self.next() != Token("(", "symbol"):
                    self.error("missing symbol '('")
                n = self.compileExpressionList()
                if self.next() != Token(")", "symbol"):
                    self.error("missing symbol ')'")
                if t[1] == -1:
                    self.code.append(f"call {t[0]}.{t1} {n}")
                else:
                    self.code.append(f"call {t[1]}.{t1} {n+1}")
            elif self.now == Token("(", "symbol"):
                if t[1] != -1:
                    self.error(f"variable '{t[0]}' not callable")
                self.code.append("push pointer 0")
                n = self.compileExpressionList()
                if self.next() != Token(")", "symbol"):
                    self.error("missing symbol ')'")
                self.code.append(f"call {t[1]}.{t[0]} {n+1}")
            elif self.now == Token("[", "symbol"):
                self.compileExpression()
                if self.now != Token("]", "symbol"):
                    self.error("missing symbol ']'")
                self.code.append(f"push {t[0]} {t[1]}")
                self.code.append("add")
                self.code.append("pop pointer 1")
                self.code.append("push that 0")
            else:
                if t[1] == -1:
                    self.error(f"identifier '{t[0]}' is not variable")
                self.code.append(f"push {t[0]} {t[1]}")

    def compileExpressionList(self) -> int:
        return 0
