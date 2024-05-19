class CompileError(Exception):
    def __init__(self, number, message, code=None):
        self.code = number
        self.message = message
        self.location = code

    def m(self):
        if self.location is None:
            return f"CompileError[ErrorCode {self.code}]: {self.message}"
        else:
            return f"CompileError[ErrorCode {self.code}]: {self.message}\nError location: {self.location}"


symbolList = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
keyWordList = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "Int", "Char", "Boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
identifier = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def tokenizer(text: list[str]):
    # 處理前後空白與單行註釋
    for i in range(len(text)):
        text[i] = text[i].strip()
        text[i] = text[i].split("//")[0]
    text = " ".join(text)
    # 處理多行註釋
    while "/*" in text and "*/" in text:
        t = text.split("/*", 1)
        t[1] = t[1].split("*/", 1)[1]
        text = " ".join(t)
    # 註釋未關閉
    if "/*" in text and "*/" not in text:
        raise CompileError(0, "Comment is not closed")
    elif "/*" not in text and "*/" in text:
        raise CompileError(0, "Comment is not closed")
    # 主要分解區
    code = []
    t = ""
    s = ""
    f = False
    for i in text:
        # 處理字串
        if i == '"':
            if f:
                code.append(s + '"')
                s = ""
                f = False
            else:
                f = True
        if f:
            s += i
        # 處理其他
        elif i == " ":
            code.append(t)
            t = ""
        elif i in symbolList:
            code.append(t)
            code.append(i)
            t = ""
        elif not f:
            t += i
    # 清除多餘空字串
    while "" in code:
        code.remove("")
    # 附上類型
    for i in range(len(code)):
        if code[i] in symbolList:
            code[i] = (code[i], "symbol", i)
        elif code[i] in keyWordList:
            code[i] = (code[i], "keyword", i)
        elif code[i].isdigit() and int(i) < 32768:
            code[i] = (code[i], "integerConstant", i)
        elif code[i][0] == '"' and code[i][-1] == '"':
            code[i] = (code[i][1:-1], "stringConstant", i)
        elif code[i][0] in identifier:
            code[i] = (code[i], "identifier", i)
        else:
            raise CompileError(1, f"error: The identifier cannot start with {code[i][0]}", code[i])
    return code
