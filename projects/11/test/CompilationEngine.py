class CompilationEngine:
    def __init__(self, token: list[tuple[str]]):
        self.token = token
        self.point = 0
        self.len = len(token)
        self.gv = {}  # global variable
        self.lv = {}  # local variable
        self.gvCount = {"static": 0, "field": 0, "function": 0, "constructor": 0, "method": 0}
        self.lvCount = {"argument": 0, "local": 0}
        self.argument = 0
        self.local = 0
        self.code = []
        self.level = [0, 0, 0]

    def get(self) -> tuple[str]:
        if self.point < self.len:
            t = self.token[self.point]
            self.point += 1
            if t == ("(", "symbol"):
                self.level[0] += 1
            elif t == (")", "symbol"):
                self.level[0] -= 1
                if self.level[0] < 0:
                    print("error: ( not closed")
                    exit()
            elif t == ("[", "symbol"):
                self.level[1] += 1
            elif t == ("]", "symbol"):
                self.level[1] -= 1
                if self.level[1] < 0:
                    print("error: [ not closed")
                    exit()
            elif t == ("{", "symbol"):
                self.level[2] += 1
            elif t == ("}", "symbol"):
                self.level[2] -= 1
                if self.level[2] < 0:
                    print("error: { not closed")
                    exit()
            return t
        else:
            print("error: Code file is incomplete")
            exit()

    def main(self) -> list[str]:
        # start with class
        now = self.get()
        if now == ("class", "keyword"):
            self.compileClass()
        else:
            print("error: The beginning of the file is not class")
            exit()
        return self.code

    def compileClass(self):
        # className
        now = self.get()
        if now[1] == "identifier":
            self.className = now[0]
        else:
            print(f"error: {now[1]} {now[0]} cannot be used as the name of class")
            exit()

        # { after className
        now = self.get()
        if now == ("{", "symbol"):
            # field or static
            while True:
                next = self.token[self.point]
                if next == ("static", "keyword") or next == ("field", "keyword"):
                    self.compileClassVarDec()
                elif next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                    break
                else:
                    print("error: There are only field, static or subroutine in class")
                    exit()
        else:
            print("error: Class missing {")
            exit()

        # function, method or constructor
        while True:
            next = self.token[self.point]
            if next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                self.lv = {}
                self.lvCount = {"argument": 0, "local": 0}
                f = self.compileSubroutine()
            else:
                break

    def compileClassVarDec(self):
        # static or field
        now = self.get()
        if now[1] == "keyword" and now[0] in ["static", "field"]:
            # kind = static or field
            kind = now[0]

            # type = int, boolean, char or identifier
            now = self.get()
            if now[1] == "identifier" or (now[1] == "keyword" and now[0] in ["int", "boolean", "char"]):
                type = now[0]
            else:
                print(f"error: type cannot be {now[0]}")
                exit()

            # everything before the ;
            while True:
                # variable
                now = self.get()
                if now[1] == "identifier":
                    self.gv[now[0]] = [type, kind, self.gvCount[kind]]
                    self.gvCount[kind] += 1
                else:
                    print(f"error: {now[1]} {now[0]} cannot be used as a variable name")
                    exit()

                # ends with ;
                now = self.get()
                if now == (";", "symbol"):
                    break
                elif now != (",", "symbol"):
                    print(f"error: unknow {now[1]} {now[0]}")
                    exit()

    def compileSubroutine(self):
        # kind = function, method or constructor
        now = self.get()
        kind = now[0]

        # special treatment for method and constructor
        temp = []
        if now == ("constructor", "keyword"):
            temp.append(f"push constant {self.gvCount['field']}")
            temp.append("call Memory.alloc 1")
            temp.append("pop pointer 0")
        elif now == ("method", "keyword"):
            temp.append("push argument 0")
            temp.append("pop pointer 0")

        # type = int, boolean, char, void or identifier
        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "void"]) or now[1] == "identifier":
            type = now[0]
        else:
            print(f"error: {now[0]} is not a legal type")
            exit()

        # subroutine name
        now = self.get()
        if now[1] == "identifier":
            self.gv[now[0]] = [type, kind, self.gvCount[kind]]
            self.gvCount[kind] += 1
            self.functionName = now[0]
        else:
            print(f"error: {now[1]} {now[0]} cannot be used as a sbroutine name")
            exit()

        # argument list
        now = self.get()
        if now != ("(", "symbol"):
            print("error: Missing (")
            exit()
        next = self.token[self.point]
        argCount = 0
        if next != (")", "symbol"):
            argCount += self.compileParameterList()
        else:
            self.get()

        # subroutine body
        now = self.get()
        if now != ("{", "symbol"):
            print("error: Missing {")
            exit()
        varCount = 0
        while True:
            next = self.token[self.point]
            if next == ("var", "keyword"):
                varCount += self.compileVarDec()
            else:
                break

        # write code
        self.code.append(f"function {self.className}.{self.functionName} {argCount + varCount}")
        self.code.extend(temp)

        # processing statement
        self.compileStatement()
        now = self.get()
        if now != ("}", "symbol"):
            print("error: Missing }")
            exit()

    def compileParameterList(self) -> int:
        pass

    def compileVarDec(self) -> int:
        pass

    def compileStatement(self):
        pass

    def compileDo(self):
        pass

    def compileLet(self):
        pass

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
