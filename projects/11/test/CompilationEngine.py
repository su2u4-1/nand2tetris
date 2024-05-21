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
        self.ifCount = 0
        self.whileCount = 0

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
                            raise CompileError(2, None, self.peek(), self.point)
                    case "[":
                        self.level[1] += 1
                    case "]":
                        self.level[1] -= 1
                        if self.level[1] < 0:
                            raise CompileError(3, None, self.peek(), self.point)
                    case "{":
                        self.level[2] += 1
                    case "}":
                        self.level[2] -= 1
                        if self.level[2] < 0:
                            raise CompileError(4, None, self.peek(), self.point)
            return t
        else:
            raise CompileError(5, None, self.peek(-1), self.point)

    def peek(self, n=None) -> tuple[str]:
        if n == None:
            n = self.point
        else:
            n = self.point + n
        if n < self.len:
            return self.token[n]
        else:
            raise CompileError(5, None, self.peek(-1), self.point)

    def main(self) -> list[str]:
        if self.get() == ("class", "keyword"):
            self.compileClass()
        else:
            raise CompileError(6, None, self.peek(), self.point)
        return self.code

    def compileClass(self):
        now = self.get()
        if now[1] == "identifier":
            self.className = now[0]
        else:
            raise CompileError(7, now[0], self.peek(), self.point)
        if self.get() == ("{", "symbol"):
            while True:
                next = self.peek()
                if next[1] == "keyword" and next[0] in ["field", "static"]:
                    self.compileClassVarDec()
                elif next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                    break
                else:
                    raise CompileError(8, None, self.peek(), self.point)
        else:
            raise CompileError(9, None, self.peek(), self.point)
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
            raise CompileError(10, now[0], self.peek(), self.point)
        while True:
            now = self.get()
            if now[1] == "identifier":
                self.gv[now[0]] = [type, kind, self.gvCount[kind]]
                self.gvCount[kind] += 1
            else:
                raise CompileError(11, now[0], self.peek(), self.point)
            now = self.get()
            if now == (";", "symbol"):
                break
            elif now != (",", "symbol"):
                raise CompileError(12, now[0], self.peek(), self.point)

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
            raise CompileError(13, now[0], self.peek(), self.point)
        now = self.get()
        if now[1] == "identifier":
            self.gv[now[0]] = [type, kind, self.gvCount[kind]]
            self.gvCount[kind] += 1
            self.functionName = now[0]
        else:
            raise CompileError(14, now[0], self.peek(), self.point)
        if self.get() != ("(", "symbol"):
            raise CompileError(15, None, self.peek(), self.point)
        if self.peek() != (")", "symbol"):
            self.compileParameterList()
        else:
            self.get()
        if self.get() != ("{", "symbol"):
            raise CompileError(16, None, self.peek(), self.point)
        while True:
            if self.peek() != ("var", "keyword"):
                break
            self.get()
            self.compileVarDec()
        self.code.insert(t, f"function {self.className}.{self.functionName} {self.lvCount['argument'] + self.lvCount['local']}")
        self.compileStatement()
        if self.get() != ("}", "symbol"):
            raise CompileError(17, None, self.peek(), self.point)

    def compileParameterList(self):
        while True:
            now = self.get()
            if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
                type = now[0]
            else:
                raise CompileError(18, now[0], self.peek(), self.point)
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "argument", self.lvCount["argument"]]
                self.lvCount["argument"] += 1
            else:
                raise CompileError(19, now[0], self.peek(), self.point)
            now = self.get()
            if now != (")", "symbol"):
                break
            elif now != (",", "symbol"):
                raise CompileError(20, None, self.peek(), self.point)

    def compileVarDec(self):
        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
            type = now[0]
        else:
            raise CompileError(21, now[0], self.peek(), self.point)
        while True:
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "local", self.lvCount["local"]]
                self.lvCount["local"] += 1
            else:
                raise CompileError(22, now[0], self.peek(), self.point)
            now = self.get()
            if now != (";", "symbol"):
                break
            elif now != (",", "symbol"):
                raise CompileError(23, None, self.peek(), self.point)

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
                    raise CompileError(24, now[0], self.peek(), self.point)
            else:
                raise CompileError(25, now[0], self.peek(), self.point)
            if self.peek() == ("}", "symbol"):
                break

    def compileDo(self):
        self.compileSubroutineCall()
        if self.get() != (";", "symbol"):
            raise CompileError(26, None, self.peek(), self.point)
        self.code.append("pop temp 0")

    def compileLet(self):
        now = self.get()
        if now[1] != "identifier":
            raise CompileError(27, now[0], self.peek(), self.point)
        if now[0] in self.lv:
            t = f"{self.lv[now[0]][1]} {self.lv[now[0]][2]}"
        elif now[0] in self.gv:
            if self.gv[now[0]][1] == "field":
                t = f"this {self.gv[now[0]][2]}"
            else:
                t = f"{self.gv[now[0]][1]} {self.gv[now[0]][2]}"
        else:
            raise CompileError(28, now[0], self.peek(), self.point)
        now = self.get()
        if now == ("=", "symbol"):
            self.compileExpression()
            self.code.append("pop " + t)
        elif now == ("[", "symbol"):
            self.compileExpression()
            self.code.append("push " + t)
            self.code.append("add")
            if self.get() != ("]", "symbol"):
                raise CompileError(29, None, self.peek(), self.point)
            if self.get() != ("=", "symbol"):
                raise CompileError(30, None, self.peek(), self.point)
            self.compileExpression()
            self.code.append("pop temp 0")
            self.code.append("pop pointer 1")
            self.code.append("push temp 0")
            self.code.append("pop that 0")
        else:
            raise CompileError(31, None, self.peek(), self.point)
        if self.get() != (";", "symbol"):
            raise CompileError(32, None, self.peek(), self.point)

    def compileWhile(self):
        if self.get() != ("(", "symbol"):
            raise CompileError(33, None, self.peek(), self.point)
        if self.peek() == (")", "symbol"):
            raise CompileError(34, None, self.peek(), self.point)
        self.code.append(f"label while-{self.whileCount}-1")
        self.compileExpression()
        self.code.append(f"not")
        self.code.append(f"if-goto while-{self.whileCount}-2")
        if self.get() != (")", "symbol"):
            raise CompileError(35, None, self.peek(), self.point)
        if self.get() != ("{", "symbol"):
            raise CompileError(36, None, self.peek(), self.point)
        self.compileStatement()
        self.code.append(f"goto while-{self.whileCount}-1")
        self.code.append(f"label while-{self.whileCount}-2")
        if self.get() != ("}", "symbol"):
            raise CompileError(37, None, self.peek(), self.point)
        self.whileCount += 1

    def compileReturn(self):
        if self.peek() == (";", "symbol"):
            self.get()
            self.code.append("push constant 0")
        else:
            self.compileExpression()
        self.code.append("return")

    def compileIf(self):
        if self.get() != ("(", "symbol"):
            raise CompileError(38, None, self.peek(), self.point)
        if self.peek() == (")", "symbol"):
            raise CompileError(39, None, self.peek(), self.point)
        self.compileExpression()
        self.code.append("not")
        self.code.append(f"if-goto if-{self.ifCount}-1")
        if self.get() != (")", "symbol"):
            raise CompileError(40, None, self.peek(), self.point)
        if self.get() != ("{", "symbol"):
            raise CompileError(41, None, self.peek(), self.point)
        self.compileStatement()
        if self.get() != ("}", "symbol"):
            raise CompileError(42, None, self.peek(), self.point)
        if self.peek() != ("else", "keyword"):
            self.code.append(f"label if-{self.ifCount}-1")
            return
        self.code.append(f"goto if-{self.ifCount}-2")
        self.code.append(f"label if-{self.ifCount}-1")
        if self.get() != ("{", "symbol"):
            raise CompileError(43, None, self.peek(), self.point)
        self.compileStatement()
        self.code.append(f"label if-{self.ifCount}-2")
        if self.get() != ("}", "symbol"):
            raise CompileError(44, None, self.peek(), self.point)

    def compileExpression(self):
        t = sum(self.level)
        while True:
            self.compileTerm()
            now = self.get()
            if t > sum(self.level):
                self.point -= 1
                break
            if now != (",", "symbol"):
                raise CompileError(45, None, self.peek(), self.point)

    def compileTerm(self):
        now = self.get()
        if now[1] == "stringContent":
            self.code.append(f"push constant {len(now[0])}")
            self.code.append("call String.new 1")
            for i in now[0]:
                self.code.append(f"push constant {ord(i)}")
                self.code.append("call String.appendChar 2")
        elif now[1] == "keyword" and now[0] in ["true", "false", "null", "this"]:
            if now[0] == "true":
                self.code.append("push constant 0")
                self.code.append("not")
            elif now[0] == "false":
                self.code.append("push constant 0")
            elif now[0] == "null":
                self.code.append("push constant 0")
            elif now[0] == "this":
                self.code.append("push pointer 0")
        elif now[1] == "integerConstant":
            self.code.append(f"push constant {now[0]}")
        elif now[1] == "symbol" and now[0] in ["-", "~", "("]:
            if now[0] == "-":
                self.code.append("neg")
                self.compileTerm()
            elif now[0] == "~":
                self.code.append("not")
                self.compileTerm()
            elif now[0] == "(":
                self.compileExpression()
                if self.get() != (")", "symbol"):
                    raise CompileError(46, None, self.peek(), self.point)
        elif now[1] == "identifier":
            next = self.peek()
            if next == ("[", "symbol"):
                if now[0] in self.lv:
                    self.code.append(f"pop {self.lv[now[0]][1]} {self.lv[now[0]][2]}")
                elif now[0] in self.gv:
                    if self.gv[now[0]][1] == "field":
                        self.code.append(f"pop this {self.gv[now[0]][2]}")
                    else:
                        self.code.append(f"pop {self.gv[now[0]][1]} {self.gv[now[0]][2]}")
                else:
                    raise CompileError(47, now[0], self.peek(), self.point)
                self.compileExpression()
                if self.get() != ("]", "symbol"):
                    raise CompileError(48, None, self.peek(), self.point)
                self.code.append("add")
                self.code.append("pop pointer 1")
                self.code.append("push that 0")
            elif next == (".", "symbol") or next == ("(", "symbol"):
                self.point -= 1
                self.compileSubroutineCall()
            else:
                if now[0] in self.lv:
                    self.code.append(f"push {self.lv[now[0]][1]} {self.lv[now[0]][2]}")
                elif now[0] in self.gv:
                    if self.gv[now[0]][1] == "field":
                        self.code.append(f"push this {self.gv[now[0]][2]}")
                    else:
                        self.code.append(f"push {self.gv[now[0]][1]} {self.gv[now[0]][2]}")
                else:
                    raise CompileError(49, now[0], self.peek(), self.point)
        else:
            raise CompileError(50, None, self.peek(), self.point)

    def compileSubroutineCall(self):
        pass

    def compileExpressionList(self):
        pass
