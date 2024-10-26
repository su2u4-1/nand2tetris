symbolList = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
keyWordList = [
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "Int",
    "Char",
    "Boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
]
identifier = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
message_list = {
    0: "Comment is not closed",
    1: "error: The identifier cannot start with {}",
    2: "Unmatched closing parenthesis ')'",
    3: "Unmatched closing bracket ']'",
    4: "Unmatched closing brace '}'",
    5: "Incomplete code file",
    6: "File must start with a 'class' declaration",
    7: "'{}' is not a valid class name",
    8: "Invalid class member, expected 'field', 'static', or a subroutine declaration",
    9: "Missing '{' after class declaration",
    10: "Invalid type '{}'",
    11: "'{}' is not a valid variable name",
    12: "Unexpected token '{}'",
    13: "'{}' is not a valid return type",
    14: "'{}' is not a valid subroutine name",
    15: "Missing '(' after subroutine name",
    16: "Missing '{' before subroutine body",
    17: "Missing '}' after subroutine body",
    18: "'{}' is not a valid type",
    19: "'{}' is not a valid variable name",
    20: "Expected ',' or ')'",
    21: "'{}' is not a valid type",
    22: "'{}' is not a valid variable name",
    23: "Expected ',' or ';'",
    24: "Unknown keyword '{}'",
    25: "Expected a keyword, got '{}'",
    26: "Missing ';' after statement",
    27: "Expected identifier, got '{}'",
    28: "Identifier '{}' not found",
    29: "Unmatched opening bracket '['",
    30: "Missing '=' after ']'",
    31: "Expected '=' or '['",
    32: "Missing ';' after statement 'let'",
    33: "Missing '(' after keyword 'while'",
    34: "Missing conditional expression",
    35: "Unmatched closing parenthesis ')'",
    36: "Missing '{'",
    37: "Unmatched closing brace '}'",
    38: "",
    39: "Missing '(' after keyword 'if'",
    40: "Missing conditional expression",
    41: "Unmatched closing parenthesis ')'",
    42: "Missing '{'",
    43: "Unmatched closing brace '}'",
    44: "Missing '{'",
    45: "Unmatched closing brace '}'",
    46: "Missing ','",
    47: "Missing closing parenthesis ')'",
    48: "Identifier '{}' not found",
    49: "Unmatched opening bracket '['",
    50: "Identifier '{}' not found",
    51: "An unspecified compile error occurred",
    52: "",
    53: "",
    54: "",
    55: "",
    56: "",
    57: "",
}


class CompileError(Exception):
    def __init__(self, code, now, next=None, n=None):
        self.code = code
        if now is None:
            self.message = message_list[code]
        else:
            self.message = message_list[code].format(now)
        self.location = next
        if next is not None and n is not None:
            self.code = f"{self.code}, Token:{n}"

    def m(self) -> str:
        t = f"CompileError[ErrorCode:{self.code}]: {self.message}"
        if self.location is not None:
            t += f"\nError location: {self.location}"
        return t


def tokenizer(text: list[str]) -> tuple[str]:
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
    while "\t" in text:
        text = "".join(text.split("\t"))
    # 註釋未關閉
    if "/*" in text and "*/" not in text:
        raise CompileError(0, None)
    elif "/*" not in text and "*/" in text:
        raise CompileError(0, None)
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
    while '"' in code:
        code.remove('"')
    # 附上類型
    for i in range(len(code)):
        if code[i] in symbolList:
            code[i] = (code[i], "symbol")
        elif code[i] in keyWordList:
            code[i] = (code[i], "keyword")
        elif code[i].isdigit() and int(i) < 32768:
            code[i] = (code[i], "integerConstant")
        elif code[i][0] == '"' and code[i][-1] == '"':
            code[i] = (code[i][1:-1], "stringContent")
        elif code[i][0] in identifier:
            code[i] = (code[i], "identifier")
        else:
            raise CompileError(1, code[i][0], code[i], i)
    return code
