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
                            print("error_code:0, error_message: unmatched ')'")
                            exit()
                    case "[":
                        self.level[1] += 1
                    case "]":
                        self.level[1] -= 1
                        if self.level[1] < 0:
                            print("error_code:1, error_message: unmatched ']'")
                            exit()
                    case "{":
                        self.level[2] += 1
                    case "}":
                        self.level[2] -= 1
                        if self.level[2] < 0:
                            print("error_code:2, error_message: unmatched '}'")
                            exit()
            return t
        else:
            print("error_code:3, error_message: incomplete code file")
            exit()

    def main(self) -> list[str]:
        now = self.get()
        if now[1] == "keyword" and now[0] == "class":
            self.compileClass()
        else:
            print("error_code:4, error_message: file must start with 'class' declaration")
            exit()
        return self.code

    def compileClass(self):
        now = self.get()
        if now[1] == "identifier":
            self.className = now[0]
        else:
            print(f"error_code:5, error_message: '{now[0]}' is not a valid class name")
            exit()

        now = self.get()
        if now[1] == "symbol" and now[0] == "{":
            while True:
                next = self.token[self.point]
                if next[1] == "keyword" and next[0] in ["field", "static"]:
                    self.compileClassVarDec()
                elif next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                    break
                else:
                    print("error_code:6, error_message: invalid class member, expected 'field', 'static', or subroutine declaration")
                    exit()
        else:
            print("error_code:7, error_message: missing '{' after class declaration")
            exit()

        while True:
            next = self.token[self.point]
            if next[1] == "keyword" and next[0] in ["function", "method", "constructor"]:
                self.lv = {}
                self.lvCount = {"argument": 0, "local": 0}
                f = self.compileSubroutine()
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
                print(f"error_code:8, error_message: invalid type '{now[0]}'")
                exit()

            while True:
                now = self.get()
                if now[1] == "identifier":
                    self.gv[now[0]] = [type, kind, self.gvCount[kind]]
                    self.gvCount[kind] += 1
                else:
                    print(f"error_code:9, error_message: '{now[0]}' is not a valid variable name")
                    exit()

                now = self.get()
                if now[1] == "symbol" and now[0] == ";":
                    break
                elif now[1] != "symbol" or now[0] != ",":
                    print(f"error_code:10, error_message: unexpected token '{now[0]}'")
                    exit()

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
            print(f"error_code:11, error_message: '{now[0]}' is not a valid return type")
            exit()

        now = self.get()
        if now[1] == "identifier":
            self.gv[now[0]] = [type, kind, self.gvCount[kind]]
            self.gvCount[kind] += 1
            self.functionName = now[0]
        else:
            print(f"error_code:12, error_message: '{now[0]}' is not a valid subroutine name")
            exit()

        now = self.get()
        if now[1] != "symbol" or now[0] != "(":
            print("error_code:13, error_message: missing '(' after subroutine name")
            exit()

        next = self.token[self.point]
        if next[1] != "symbol" or next[0] != ")":
            self.compileParameterList()
        else:
            self.get()

        now = self.get()
        if now[1] != "symbol" or now[0] != "{":
            print("error_code:14, error_message: missing '{' before subroutine body")
            exit()
        while True:
            next = self.token[self.point]
            if next[1] == "keyword" and next[0] == "var":
                self.compileVarDec()
            else:
                break
        self.code.insert(t, f"function {self.className}.{self.functionName} {self.lvCount['argument'] + self.lvCount['local']}")
        self.compileStatement()

        now = self.get()
        if now[1] != "symbol" or now[0] != "}":
            print("error_code:15, error_message: missing '}' after subroutine body")
            exit()

    def compileParameterList(self):
        while True:
            now = self.get()
            if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
                type = now[0]
            else:
                print(f"error_code:16, error_message: '{now[0]}' is not a valid type")
                exit()
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "argument", self.lvCount["argument"]]
                self.lvCount["argument"] += 1
            else:
                print(f"error_code:17, error_message: '{now[0]}' is not a valid variable name")
                exit()
            now = self.get()
            if now[1] == "symbol" and now[0] == ")":
                break
            elif now[1] != "symbol" or now[0] != ",":
                print("error_code:18, error_message: expected ',' or ')'")
                exit()

    def compileVarDec(self):
        now = self.get()
        now = self.get()
        if (now[1] == "keyword" and now[0] in ["int", "boolean", "char", "Int", "Boolean", "Char"]) or now[1] == "identifier":
            type = now[0]
        else:
            print(f"error_code:19, error_message: '{now[0]}' is not a valid type")
            exit()
        while True:
            now = self.get()
            if now[1] == "identifier":
                self.lv[now[0]] = [type, "local", self.lvCount["local"]]
                self.lvCount["local"] += 1
            else:
                print(f"error_code:20, error_message: '{now[0]}' is not a valid variable name")
                exit()

            now = self.get()
            if now[1] == "symbol" and now[0] == ";":
                break
            elif now[1] != "symbol" or now[0] != ",":
                print(f"error_code:21, error_message: expected ',' or ';'")
                exit()

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
                    print(f"error_code:22, error_message: unknown keyword '{now[0]}'")
                    exit()
            else:
                print(f"error_code:23, error_message: expected a keyword, got '{now[0]}'")
                exit()

            next = self.token[self.point]
            if next[1] == "symbol" and next[0] == "}":
                break
            elif next[1] != "keyword" or next[0] not in ["do", "let", "while", "return", "if"]:
                print(f"error_code:24, error_message: invalid statement '{next[0]}'")
                exit()

    def compileDo(self):
        pass

    def compileLet(self):
        now = self.get()
        if now[1] != "identifier":
            print(f"error_code:25, error_message: expected identifier, got '{now[0]}'")
            exit()
        if now[0] in self.lv:
            t = f"{self.lv[now[0]][1]} {self.lv[now[0]][2]}"
        elif now[0] in self.gv:
            if self.gv[now[0]][1] == "field":
                t = f"this {self.gv[now[0]][2]}"
            else:
                t = f"{self.gv[now[0]][1]} {self.gv[now[0]][2]}"
        else:
            print(f"error_code:26, error_message: identifier '{now[0]}' not found")
            exit()

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
                print("error_code:27, error_message: unmatched '['")
                exit()

            now = self.get()
            if now[1] != "symbol" or now[0] != "=":
                print("error_code:28, error_message: missing '=' after ']'")
                exit()
            self.compileExpression()
            self.code.append("pop temp 0")
            self.code.append("pop pointer 1")
            self.code.append("push temp 0")
            self.code.append("pop that 0")
        else:
            print("error_code:29, error_message: expected '=' or '['")
            exit()

        now = self.get()
        if now[1] != "symbol" or now[0] != ";":
            print("error_code:30, error_message: missing ';' after statement")
            exit()

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
