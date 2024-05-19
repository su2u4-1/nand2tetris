from JackTokenizer import CompileError


class CompilationEngine:
    def __init__(self, token: list[tuple[str]]):
        self.token = token
        self.point = 0
        self.len = len(token)
        self.gv = {}  # global variables
        self.lv = {}  # local variables
        self.gvCount = {"static": 0, "field": 0, "function": 0, "constructor": 0, "method": 0}
        self.lvCount = {"argument": 0, "local": 0}
        self.code = []
        self.level = [0, 0, 0]

    def get(self) -> tuple[str]:
        if self.point < self.len:
            t = self.token[self.point]
            self.point += 1
            if t[1] == "symbol":
                match t[0]:
                    case "(":
                        self.level[0] += 1
                    case ")":
                        self.level[0] -= 1
                        if self.level[0] < 0:
                            raise CompileError(2, "unmatched ')'", self.peek(), self.point)
                    case "[":
                        self.level[1] += 1
                    case "]":
                        self.level[1] -= 1
                        if self.level[1] < 0:
                            raise CompileError(3, "unmatched ']'", self.peek(), self.point)
                    case "{":
                        self.level[2] += 1
                    case "}":
                        self.level[2] -= 1
                        if self.level[2] < 0:
                            raise CompileError(44, "unmatched '}'", self.peek(), self.point)
            return t
        else:
            raise CompileError(5, "incomplete code file", self.peek(-1), self.point)

    def peek(self, n=None) -> tuple[str]:
        if n == None:
            n = self.point
        else:
            n = self.point + n
        if n < self.len:
            return self.token[n]
        else:
            raise CompileError(5, "incomplete code file", self.peek(-1), self.point)

    def main(self) -> list[str]:
        if self.get() == ("class", "keyword"):
            self.compileClass()
        else:
            raise CompileError(6, "file must start with 'class' declaration", self.peek(), self.point)
        return self.code

    def compileClass(self):
        now = self.get()
        if now[1] == "identifier":
            self.className = now[0]
        else:
            raise CompileError(7, f"'{now[0]}' is not a valid class name", self.peek(), self.point)

        if self.get() == ("{", "symbol"):
            while True:
                next = self.peek()
                if next[1] == "keyword" and next[0] in ["field", "static"]:
                    self.compileClassVarDec()
                elif next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                    break
                else:
                    raise CompileError(8, "invalid class member, expected 'field', 'static', or subroutine declaration", self.peek(), self.point)
        else:
            raise CompileError(9, "missing '{' after class declaration", self.peek(), self.point)

        while True:
            next = self.peek()
            if next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                self.lv = {}
                self.lvCount = {"argument": 0, "local": 0}
                self.compileSubroutine()
            else:
                break

    def compileClassVarDec(self):
        kind = self.get()[0]

        now = self.get()
        if now[1] == "identifier" or (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]):
            type = now[0]
        else:
            raise CompileError(10, f"invalid type '{now[0]}'", self.peek(), self.point)

        while True:
            now = self.get()
            if now[1] == "identifier":
                self.gv[now[0]] = [type, kind, self.gvCount[kind]]
                self.gvCount[kind] += 1
            else:
                raise CompileError(11, f"'{now[0]}' is not a valid variable name", self.peek(), self.point)

            now = self.get()
            if now == (";", "symbol"):
                break
            elif now != (",", "symbol"):
                raise CompileError(12, f"unexpected token '{now[0]}'", self.peek(), self.point)

    def compileSubroutine(self):
        now = self.get()
        kind = now[0]
        t = len(self.code)
        if now == ("constructor", "keyword"):
            self.code.append(f"push constant {self.gvCount['field']}")
            self.code.append("call Memory.alloc 1")
            self.code.append("pop pointer 0")
        elif now == ("method", "keyword"):
            self.code.append("push argument 0")
            self.code.append("pop pointer 0")

        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char", "void"]) or now[1] == "identifier":
            type = now[0]
        else:
            raise CompileError(13, f"'{now[0]}' is not a valid return type", self.peek(), self.point)

        now = self.get()
        if now[1] == "identifier":
            self.gv[now[0]] = [type, kind, self.gvCount[kind]]
            self.gvCount[kind] += 1
            self.functionName = now[0]
        else:
            raise CompileError(14, f"'{now[0]}' is not a valid subroutine name", self.peek(), self.point)

        if self.get() != ("(", "symbol"):
            raise CompileError(15, "missing '(' after subroutine name", self.peek(), self.point)

        if self.peek() != (")", "symbol"):
            self.compileParameterList()
        else:
            self.get()

        if self.get() != ("{", "symbol"):
            raise CompileError(16, "missing '{' before subroutine body", self.peek(), self.point)
        while True:
            if self.peek() != ("var", "keyword"):
                break
            self.get()
            self.compileVarDec()
        self.code.insert(t, f"function {self.className}.{self.functionName} {self.lvCount['argument'] + self.lvCount['local']}")
        self.compileStatement()

        if self.get() != ("}", "symbol"):
            raise CompileError(17, "missing '}' after subroutine body", self.peek(), self.point)

    def compileParameterList(self):
        while True:
            now = self.get()
            if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
                type = now[0]
            else:
                raise CompileError(18, f"'{now[0]}' is not a valid type", self.peek(), self.point)
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "argument", self.lvCount["argument"]]
                self.lvCount["argument"] += 1
            else:
                raise CompileError(19, f"'{now[0]}' is not a valid variable name", self.peek(), self.point)
            now = self.get()
            if now != (")", "symbol"):
                break
            elif now != (",", "symbol"):
                raise CompileError(20, "expected ',' or ')'", self.peek(), self.point)

    def compileVarDec(self):
        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
            type = now[0]
        else:
            raise CompileError(21, f"'{now[0]}' is not a valid type", self.peek(), self.point)
        while True:
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "local", self.lvCount["local"]]
                self.lvCount["local"] += 1
            else:
                raise CompileError(22, f"'{now[0]}' is not a valid variable name", self.peek(), self.point)

            now = self.get()
            if now != (";", "symbol"):
                break
            elif now != (",", "symbol"):
                raise CompileError(23, "expected ',' or ';'", self.peek(), self.point)

    def compileStatement(self):
        while True:
            now = self.get()
            if now[1] == "keyword":
                if now[0] == "do":
                    self.compileDo()
                elif now[0] == "let":
                    self.compileLet()
                elif now[0] == "while":
                    self.compileWhile()
                elif now[0] == "return":
                    self.compileReturn()
                elif now[0] == "if":
                    self.compileIf()
                else:
                    raise CompileError(24, f"unknown keyword '{now[0]}'", self.peek(), self.point)
            else:
                raise CompileError(25, f"expected a keyword, got '{now[0]}'", self.peek(), self.point)

            if self.peek() == ("}", "symbol"):
                break

    def compileDo(self):
        self.compileSubroutineCall()
        if self.get() != (";", "symbol"):
            raise CompileError(27, "missing ';' after statement", self.peek(), self.point)
        self.code.append("pop temp 0")

    def compileLet(self):
        now = self.get()
        if now[1] != "identifier":
            raise CompileError(27, f"expected identifier, got '{now[0]}'", self.peek(), self.point)
        if now[0] in self.lv:
            t = f"{self.lv[now[0]][1]} {self.lv[now[0]][2]}"
        elif now[0] in self.gv:
            if self.gv[now[0]][1] == "field":
                t = f"this {self.gv[now[0]][2]}"
            else:
                t = f"{self.gv[now[0]][1]} {self.gv[now[0]][2]}"
        else:
            raise CompileError(28, f"identifier '{now[0]}' not found", self.peek(), self.point)

        now = self.get()
        if now == ("=", "symbol"):
            self.compileExpression()
            self.code.append("pop " + t)
        elif now == ("[", "symbol"):
            self.compileExpression()
            self.code.append("push " + t)
            self.code.append("add")

            if self.get() != ("]", "symbol"):
                raise CompileError(29, "unmatched '['", self.peek(), self.point)

            if self.get() != ("=", "symbol"):
                raise CompileError(30, "missing '=' after ']'", self.peek(), self.point)
            self.compileExpression()
            self.code.append("pop temp 0")
            self.code.append("pop pointer 1")
            self.code.append("push temp 0")
            self.code.append("pop that 0")
        else:
            raise CompileError(31, "expected '=' or '['", self.peek(), self.point)

        if self.get() != (";", "symbol"):
            raise CompileError(32, "missing ';' after statement", self.peek(), self.point)

    def compileWhile(self):
        pass

    def compileReturn(self):
        if self.peek() == (";", "symbol"):
            self.get()
            self.code.append("push constant 0")
        else:
            self.compileExpression()
        self.code.append("return")

    def compileIf(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileSubroutineCall(self):
        pass

    def compileExpressionList(self):
        pass
