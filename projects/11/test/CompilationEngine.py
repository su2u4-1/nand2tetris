class CompilationEngine:
    def __init__(self, token: list[tuple[str]]):
        self.token = token
        self.point = 0
        self.len = len(token)
        self.gv = {}  # global variable
        self.lv = {}  # local variable
        self.vardec = {"static": 0, "field": 0}
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
        now = self.get()
        if now == ("class", "keyword"):
            self.compileClass()
        else:
            print("error: The beginning of the file is not class")
            exit()
        return self.code

    def compileClass(self):
        now = self.get()
        if now[1] == "identifier":
            self.classname = now[0]
        else:
            print(f"error: {now[1]} {now[0]} cannot be used as the name of class")
            exit()
        now = self.get()
        if now == ("{", "symbol"):
            next = self.token[self.point]
            if next == ("static", "keyword") or next == ("field", "keyword"):
                self.compileClassVarDec()
            elif next[1] != "keyword" or next[0] not in ["function", "method", "constructor"]:
                print("error: The first one in class is not var or subroutine")
                exit()
        else:
            print("error: class messing {")
            exit()
        next = self.token[self.point]
        if next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
            f = True
            while f:
                f = self.compileSubroutine()

    def compileClassVarDec(self):
        now = self.get()
        if now[1] == "keyword" and now[0] in ["static", "field"]:
            kind = now[0]
            now = self.get()
            if now[1] == "identifier" or (now[1] == "keyword" and now[0] in ["int", "boolean", "char"]):
                type = now[0]
            else:
                print(f"error: type cannot be {now[0]}")
                exit()
            while now != (";", "symbol"):
                now = self.get()
                if now[1] == "identifier":
                    self.gv[now[0]] = [type, kind, self.vardec[kind]]
                    self.vardec[kind] += 1
                else:
                    print(f"error: {now[1]} {now[0]} cannot be used as a variable name")
                    exit()
                now = self.get()
                if now == (";", "symbol"):
                    break
                elif now != (",", "symbol"):
                    print(f"error: unknow {now[1]} {now[0]}")
                    exit()

    def compileSubroutine(self) -> bool:
        temp = []
        now = self.get()
        if now == ("constructor", "keyword"):
            temp.append(f"push constant {self.vardec["field"]}")
            temp.append("call Memory.alloc 1")
            temp.append("pop pointer 0")
        elif now == ("method", "keyword"):
            temp.append("push argument 0")
            temp.append("pop pointer 0")
        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "void"]) or now[1] == "identifier":
            pass
        else:
            print(f"error: {now[0]} is not a legal type")

    def compileParameterList(self):
        pass

    def compileVarDec(self):
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
