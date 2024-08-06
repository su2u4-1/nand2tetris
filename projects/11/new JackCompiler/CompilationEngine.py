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
        # for i in self.code:
        #     print(i)
        print("error:", des, "\nnow:", self.now)
        exit()

    def next(self) -> Token:
        if self.point >= len(self.tokens):
            self.error("Wrong end of file", self.tokens[-1].line)
        self.now = self.tokens[self.point]
        self.point += 1
        # print(self.now)
        return self.now

    def main(self) -> list[str]:
        self.compileClass()
        for i in range(len(self.code)):
            if self.code[i].startswith("#"):
                self.code[i] = ""
        while "" in self.code:
            self.code.remove("")
        return self.code

    def compileClass(self) -> None:
        # self.code.append("#Class_S")
        # print("Class_S")
        if self.next() != Token("class", "keyword"):
            self.error("missing keyword 'class'")
        if self.next().type != "identifier":
            self.error(f"class name must be identifier, not {self.now.type}")
        self.class_name = self.now.content
        if self.next() != Token("{", "symbol"):
            self.error("missing symbol '{'")
        while self.next() == Tokens(["static", "field"], "keyword"):
            self.compileClassVarDec()
        while self.now == Tokens(["constructor", "function", "method"], "keyword"):
            self.compileSubroutine()
        if self.now != Token("}", "symbol"):
            self.error("bracket '}' is not closed")
        # self.code.append("#Class_E")
        # print("Class_E")

    def compileClassVarDec(self) -> None:
        # self.code.append("#ClassVarDec_S")
        # print("ClassVarDec_S")
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
        # self.code.append("#ClassVarDec_E")
        # print("ClassVarDec_E")

    def compileSubroutine(self) -> None:
        # self.code.append("#Subroutine_S")
        # print("Subroutine_S")
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
        self.code.append(f"function {self.class_name}.{subroutine_name} {self.varCount['local']}")
        self.compileStatements()
        if self.now != Token("}", "symbol"):
            self.error("Brackets { are not closed")
        # self.code.append("#Subroutine_E")
        # print("Subroutine_E")

    def compileArgumentList(self) -> None:
        # self.code.append("#ArgumentList_S")
        # print("ArgumentList_S")
        self.next()
        while self.now != Token(")", "symbol"):
            if self.now.type != "identifier" and self.now != Tokens(["int", "boolean", "char"], "keyword"):
                self.error("argument type must be int, boolean, char or identifier")
            var_type = self.now.content
            if self.next().type != "identifier":
                self.error("argument name must be identifier")
            self.lv[self.now.content] = ("argument", self.varCount["argument"], var_type)
            self.varCount["argument"] += 1
            if self.next() != Tokens([",", ")"], "symbol"):
                self.error("must be symbol ',' or ')'")
        # self.code.append("#ArgumentList_E")
        # print("ArgumentList_E")

    def compileVarDec(self) -> None:
        # self.code.append("#VarDec_S")
        # print("VarDec_S")
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
        # print("VarDec_E")
        # self.code.append("#VarDec_E")

    def compileStatements(self) -> None:
        # self.code.append("#Statements_S")
        # print("Statements_S")
        while self.now != Token("}", "symbol"):
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
            self.next()
        # print("Statements_E")
        # self.code.append("#Statements_E")

    def compileDo(self) -> None:
        # self.code.append("#Do_S")
        # print("Do_S")
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
            if self.now != Token(")", "symbol"):
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
            if self.now != Token(")", "symbol"):
                self.error("missing symbol ')'")
            self.code.append(f"call {t[1]}.{t[0]} {n+1}")
        else:
            self.error("identifier must be followed by symbol '(' or '.'")
        if self.next() != Token(";", "symbol"):
            self.error("missing symbol ';'")
        self.code.append("pop temp 0")
        # print("Do_E")
        # self.code.append("#Do_E")

    def compileLet(self) -> None:
        # self.code.append("#Let_S")
        # print("Let_S")
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
        else:
            self.error("missing symbol '='")
        if self.now != Token(";", "symbol"):
            self.error("missing symbol ';'")
        # print("Let_E")
        # self.code.append("#Let_E")

    def compileWhile(self) -> None:
        # self.code.append("#While_S")
        # print("While_S")
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
        self.next()
        self.compileStatements()
        self.code.append(f"goto while-{nowCount}-1")
        self.code.append(f"label while-{nowCount}-2")
        if self.now != Token("}", "symbol"):
            self.error("missing symbol '}'")
        # print("While_E")
        # self.code.append("#While_E")

    def compileReturn(self) -> None:
        # self.code.append("#Return_S")
        # print("Return_S")
        if self.tokens[self.point] == Token(";", "symbol"):
            self.code.append("push constant 0")
            self.next()
        else:
            self.compileExpression()
            if self.now != Token(";", "symbol"):
                self.error("missing symbol ';'")
        self.code.append("return")
        # print("Return_E")
        # self.code.append("#Return_E")

    def compileIf(self) -> None:
        # self.code.append("#If_S")
        # print("If_S")
        nowCount = self.ifCount
        self.ifCount += 1
        if self.next() != Token("(", "symbol"):
            self.error("missing symbol '('")
        self.compileExpression()
        self.code.append("not")
        self.code.append(f"if-goto if-{nowCount}-1")
        if self.now != Token(")", "symbol"):
            self.error("missing symbol ')'")
        if self.next() != Token("{", "symbol"):
            self.error("missing symbol '{'")
        self.next()
        self.compileStatements()
        if self.now != Token("}", "symbol"):
            self.error("missing symbol '}'")
        if self.next() == Token("else", "keyword"):
            if self.next() != Token("{", "symbol"):
                self.error("missing symbol '{'")
            self.code.append(f"goto if-{nowCount}-2")
            self.code.append(f"label if-{nowCount}-1")
            self.next()
            self.compileStatements()
            self.code.append(f"label if-{nowCount}-2")
            if self.now != Token("}", "symbol"):
                self.error("missing symbol '}'")
        else:
            self.code.append(f"label if-{nowCount}-1")
        # print("If_E")
        # self.code.append("#If_E")

    def compileExpression(self) -> None:
        # self.code.append("#Expression_S")
        # print("Expression_S")
        if self.now == Tokens(["}", "]", ")", ";", ","], "symbol"):
            # print("Expression_E")
            # self.code.append("#Expression_E")
            return
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
        # print("Expression_E")
        # self.code.append("#Expression_E")

    def compileTerm(self) -> None:
        # self.code.append("#Term_S")
        # print("Term_S")
        m = True
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
                if self.now != Token(")", "symbol"):
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
                if self.now != Token(")", "symbol"):
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
                m = False
                if t[1] == -1:
                    self.error(f"identifier '{t[0]}' is not variable")
                self.code.append(f"push {t[0]} {t[1]}")
        if m:
            self.next()
        # print("Term_E")
        # self.code.append("#Term_E")

    def compileExpressionList(self) -> int:
        # self.code.append("#ExpressionList_S")
        # print("ExpressionList_S")
        n = 0
        while self.now != Token(")", "symbol"):
            self.compileExpression()
            n += 1
            if self.now != Tokens([",", ")"], "symbol"):
                self.error("missing symbol ','")
        # print("ExpressionList_E")
        # self.code.append("#ExpressionList_E")
        return n
