import re

symbolL = ["{", "}", "[", "]", "(", ")", ",", ";", "+", "-", "*", "/", "&", "|", "~", ">", "<", "=", "."]
keyList = [
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


# 將嵌套的列表展開為一個平面列表
def flattenNestedList(nested_list: list):
    def _flatten(nested, result):
        for item in nested:
            if isinstance(item, list):
                _flatten(item, result)
            else:
                result.append(item)
        return result

    return _flatten(nested_list, [])


# 移除列表裡的特定元素
def removeE(l: list, e):
    t = []
    if type(e) == list:
        e = set(e)
        for i in l:
            if i not in e:
                t.append(i)
    else:
        for i in l:
            if i != e:
                t.append(i)
    return t


# 處理文本元素,分割和重組字符串
def processTextElements(text: list):
    text = flattenNestedList(text)
    f = False
    for i in range(len(text)):
        if '"' in text[i]:
            t = text[i].split('"')
            if len(t) == 2:
                text[i] = [t[0], '"', t[1]]
            elif len(t) == 3:
                text[i] = [t[0], '"', t[1], '"', t[2]]
    text = flattenNestedList(text)
    for i in range(len(text)):
        if text[i] == '"':
            if f:
                f = False
                te += " " + text[i]
                text[i] = te
            else:
                f = True
                te = ""
        if f:
            te += " " + text[i]
            text[i] = ""
    text = removeE(text, "")
    for i in range(len(text)):
        if text[i].startswith(' "') and text[i].endswith('"'):
            text[i] = '"' + text[i][3:-2] + '"'
        elif (text[i][0:2] != ' "' and text[i][0] != '"') or text[i][-1] != '"':
            if text[i] in symbolL:
                continue
            else:
                for k in symbolL:
                    if k in text[i]:
                        t = text[i].split(k, 1)
                        t = [t[0], k, t[1]]
                        text[i] = processTextElements(t)
                        break
    return flattenNestedList(text)


# 預處理源代碼,清理註釋,空白和不必要的換行
def main(text: list):
    r = []
    f = False
    for i in range(len(text)):
        text[i] = text[i].strip()
        text[i] = re.sub(r"\s+", " ", text[i])
    for i in text:
        if i.startswith("/*"):
            f = True
        if f:
            r.append(i)
        if i.endswith("*/"):
            f = False
        if i.startswith("//"):
            r.append(i)
    text = removeE(text, r)
    for i in range(len(text)):
        if "//" in text[i]:
            text[i] = text[i].split("//")[0]
        text[i] = text[i].strip()
        text[i] = re.sub(r"\s+", " ", text[i])
    text = removeE(text, "")
    temp = []
    f = False
    for i in text:
        temp += processTextElements(i.split())
    text = removeE(flattenNestedList(temp), "")
    return Nxml(text)


def Nxml(text: list):
    temp = []
    err = False
    for i in text:
        if i in keyList:
            temp.append([i, "keyword"])
        elif i in symbolL:
            temp.append([i, "symbol"])
        elif i.isdigit() and int(i) < 32768:
            temp.append([int(i), "integerConstant"])
        elif i[0] == i[-1] == '"':
            temp.append([i[1:-1], "stringConstant"])
        elif not i[0].isdigit():
            temp.append([i, "identifier"])
        else:
            print("error:", i)
            err = True
    if err:
        exit()
    return temp
