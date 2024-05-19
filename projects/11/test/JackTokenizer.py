symbolList = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
keyWordList = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
identifier = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def tokenizer(text: list[str]):
    # 處理前後空白與單行註釋
    for i in range(len(text)):
        text[i] = text[i].strip()
        text[i] = text[i].split("//")[0]
    text = " ".join(text)
    # 處理多行註釋
    while "/*" in text and "*/" in text:
        t = text.split("/*")
        t[1] = t[1].split("*/")[1]
        text = " ".join(t)
    # 註釋未關閉
    if "/*" in text and "*/" not in text:
        print("error: Comment is not closed")
        exit()
    elif "/*" not in text and "*/" in text:
        print("error: Comment is not closed")
        exit()
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
            code[i] = (code[i], "symbol")
        elif code[i] in keyWordList:
            code[i] = (code[i], "keyword")
        elif code[i].isdigit() and int(i) < 32768:
            code[i] = (code[i], "integerConstant")
        elif code[i][0] == '"' and code[i][-1] == '"':
            code[i] = (code[i][1:-1], "sttringConstant")
        elif code[i][0] in identifier:
            code[i] = (code[i], "identifier")
        else:
            print(f"error: The identifier cannot start with {code[i][0]}")
    return code