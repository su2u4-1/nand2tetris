class CompileError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def m(self):
        return f"CompileError[ErrorCode {self.code}]: {self.message}"


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
                            raise CompileError(0, "unmatched ')'")
                    case "[":
                        self.level[1] += 1
                    case "]":
                        self.level[1] -= 1
                        if self.level[1] < 0:
                            raise CompileError(1, "unmatched ']'")
                    case "{":
                        self.level[2] += 1
                    case "}":
                        self.level[2] -= 1
                        if self.level[2] < 0:
                            raise CompileError(2, "unmatched '}'")
            return t
        else:
            raise CompileError(3, "incomplete code file")

    def peek(self) -> tuple[str]:
        if self.point < self.len:
            return self.token[self.point]
        else:
            raise CompileError(3, "incomplete code file")

    def main(self) -> list[str]:
        now = self.get()
        if now[1] == "keyword" and now[0] == "class":
            self.compileClass()
        else:
            raise CompileError(4, "file must start with 'class' declaration")
        return self.code

    def compileClass(self):
        now = self.get()
        if now[1] == "identifier":
            self.className = now[0]
        else:
            raise CompileError(5, f"'{now[0]}' is not a valid class name")

        now = self.get()
        if now[1] == "symbol" and now[0] == "{":
            while True:
                next = self.peek()
                if next[1] == "keyword" and next[0] in ["field", "static"]:
                    self.compileClassVarDec()
                elif next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                    break
                else:
                    raise CompileError(6, "invalid class member, expected 'field', 'static', or subroutine declaration")
        else:
            raise CompileError(7, "missing '{' after class declaration")

        while True:
            next = self.peek()
            if next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                self.lv = {}
                self.lvCount = {"argument": 0, "local": 0}
                self.compileSubroutine()
            else:
                break

    def compileClassVarDec(self):
        now = self.get()
        if now[1] == "keyword" and now[0] in ["static", "field"]:
            kind = now[0]

            now = self.get()
            if now[1] == "identifier" or (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]):
                type = now[0]
            else:
                raise CompileError(8, f"invalid type '{now[0]}'")

            while True:
                now = self.get()
                if now[1] == "identifier":
                    self.gv[now[0]] = [type, kind, self.gvCount[kind]]
                    self.gvCount[kind] += 1
                else:
                    raise CompileError(9, f"'{now[0]}' is not a valid variable name")

                now = self.get()
                if now[1] == "symbol" and now[0] == ";":
                    break
                elif now[1] != "symbol" or now[0] != ",":
                    raise CompileError(10, f"unexpected token '{now[0]}'")

    def compileSubroutine(self):
        now = self.get()
        kind = now[0]
        t = len(self.code)
        if now[1] == "keyword" and now[0] == "constructor":
            self.code.append(f"push constant {self.gvCount['field']}")
            self.code.append("call Memory.alloc 1")
            self.code.append("pop pointer 0")
        elif now[1] == "keyword" and now[0] == "method":
            self.code.append("push argument 0")
            self.code.append("pop pointer 0")

        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char", "void"]) or now[1] == "identifier":
            type = now[0]
        else:
            raise CompileError(11, f"'{now[0]}' is not a valid return type")

        now = self.get()
        if now[1] == "identifier":
            self.gv[now[0]] = [type, kind, self.gvCount[kind]]
            self.gvCount[kind] += 1
            self.functionName = now[0]
        else:
            raise CompileError(12, f"'{now[0]}' is not a valid subroutine name")

        now = self.get()
        if now[1] != "symbol" or now[0] != "(":
            raise CompileError(13, "missing '(' after subroutine name")

        next = self.peek()
        if next[1] != "symbol" or next[0] != ")":
            self.compileParameterList()
        else:
            self.get()

        now = self.get()
        if now[1] != "symbol" or now[0] != "{":
            raise CompileError(14, "missing '{' before subroutine body")
        while True:
            next = self.peek()
            if next[1] == "keyword" and next[0] == "var":
                self.compileVarDec()
            else:
                break
        self.code.insert(t, f"function {self.className}.{self.functionName} {self.lvCount['argument'] + self.lvCount['local']}")
        self.compileStatement()

        now = self.get()
        if now[1] != "symbol" or now[0] != "}":
            raise CompileError(15, "missing '}' after subroutine body")

    def compileParameterList(self):
        while True:
            now = self.get()
            if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
                type = now[0]
            else:
                raise CompileError(16, f"'{now[0]}' is not a valid type")
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "argument", self.lvCount["argument"]]
                self.lvCount["argument"] += 1
            else:
                raise CompileError(17, f"'{now[0]}' is not a valid variable name")
            now = self.get()
            if now[1] == "symbol" and now[0] == ")":
                break
            elif now[1] != "symbol" or now[0] != ",":
                raise CompileError(18, "expected ',' or ')'")

    def compileVarDec(self):
        now = self.get()
        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
            type = now[0]
        else:
            raise CompileError(19, f"'{now[0]}' is not a valid type")
        while True:
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "local", self.lvCount["local"]]
                self.lvCount["local"] += 1
            else:
                raise CompileError(20, f"'{now[0]}' is not a valid variable name")

            now = self.get()
            if now[1] == "symbol" and now[0] == ";":
                break
            elif now[1] != "symbol" or now[0] != ",":
                raise CompileError(21, "expected ',' or ';'")

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
                    raise CompileError(22, f"unknown keyword '{now[0]}'")
            else:
                raise CompileError(23, f"expected a keyword, got '{now[0]}'")

            next = self.peek()
            if next[1] == "symbol" and next[0] == "}":
                break
            elif next[1] != "keyword" or next[0] not in ["do", "let", "while", "return", "if"]:
                raise CompileError(24, f"invalid statement '{next[0]}'")

    def compileDo(self):
        pass

    def compileLet(self):
        now = self.get()
        if now[1] != "identifier":
            raise CompileError(25, f"expected identifier, got '{now[0]}'")
        if now[0] in self.lv:
            t = f"{self.lv[now[0]][1]} {self.lv[now[0]][2]}"
        elif now[0] in self.gv:
            if self.gv[now[0]][1] == "field":
                t = f"this {self.gv[now[0]][2]}"
            else:
                t = f"{self.gv[now[0]][1]} {self.gv[now[0]][2]}"
        else:
            raise CompileError(26, f"identifier '{now[0]}' not found")

        now = self.get()
        if now[1] == "symbol" and now[0] == "=":
            self.compileExpression()
            self.code.append("pop " + t)
        elif now[1] == "symbol" and now[0] == "[":
            self.compileExpression()
            self.code.append("push " + t)
            self.code.append("add")

            now = self.get()
            if now[1] != "symbol" or now[0] != "]":
                raise CompileError(27, "unmatched '['")

            now = self.get()
            if now[1] != "symbol" or now[0] != "=":
                raise CompileError(28, "missing '=' after ']'")
            self.compileExpression()
            self.code.append("pop temp 0")
            self.code.append("pop pointer 1")
            self.code.append("push temp 0")
            self.code.append("pop that 0")
        else:
            raise CompileError(29, "expected '=' or '['")

        now = self.get()
        if now[1] != "symbol" or now[0] != ";":
            raise CompileError(30, "missing ';' after statement")

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass
