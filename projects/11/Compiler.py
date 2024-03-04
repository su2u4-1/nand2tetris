def compiler(text: list[str]):
    s = len(text[i]) - len(text[i].strip())
    text[i] = text[i].strip()

def compile(text):
    global symbol, symbolClass
    symbol = []
    symbolClass = {}
    variable(text)
    for i in symbol:
        print(i)
    print(symbolClass)
    return text


def variable(text: list):
    f0 = False
    t0 = []
    f1 = False
    t1 = []
    f2 = False
    t2 = []
    n0 = 0
    n1 = 0
    for i in range(len(text)):
        text[i] = text[i].strip()
    for i in text:
        if i == "<class>":
            s = -1
            n0 = 0
        if i == "<subroutineDec>":
            s += 1
            n1 = 0
            if len(symbol) < s + 1:
                symbol.append({})
        if i == "<classVarDec>":
            f0 = True
        if f0:
            t0.append(i)
        if i == "</classVarDec>":
            f0 = False
            n0 = classVar(t0, n0)
            t0 = []
        if i == "<varDec>":
            f1 = True
        if f1:
            t1.append(i)
        if i == "</varDec>":
            f1 = False
            n1 = var(t1, s, n1)
            t1 = []
        if i == "<parameterList>":
            f2 = True
        if f2:
            t2.append(i)
        if i == "</parameterList>":
            f2 = False
            n1 = parameterList(t2, s, n1)
            t2 = []
    for i in range(len(text)):
        if text[i] == "<keyword> class </keyword>":
            className = " ".join(text[i + 1].split()[1:-1])
        elif text[i] == "":
            pass


def var(text, s, n):
    for i in range(len(text)):
        if text[i] == "<keyword> var </keyword>":
            type = " ".join(text[i + 1].split()[1:-1])
            if text[i + 1].startswith("<identifier>") and text[i + 1].endswith("</identifier>"):
                pass
            if text[i + 2].startswith("<identifier>") and text[i + 2].endswith("</identifier>"):
                name = " ".join(text[i + 2].split()[1:-1])
                symbol[s][name] = [type, "local", n]
                n += 1
        elif text[i] == "<symbol> , </symbol>":
            if text[i + 1].startswith("<identifier>") and text[i + 1].endswith("</identifier>"):
                name = " ".join(text[i + 1].split()[1:-1])
                symbol[s][name] = [type, "local", n]
                n += 1
        elif text[i] == "<symbol> ; </symbol>":
            return n


def classVar(text, n):
    for i in range(len(text)):
        if text[i] in ["<keyword> field </keyword>", "<keyword> static </keyword>"]:
            cl = " ".join(text[i].split()[1:-1])
            type = " ".join(text[i + 1].split()[1:-1])
            if text[i + 1].startswith("<identifier>") and text[i + 1].endswith("</identifier>"):
                pass
            if text[i + 2].startswith("<identifier>") and text[i + 2].endswith("</identifier>"):
                name = " ".join(text[i + 2].split()[1:-1])
                symbolClass[name] = [type, cl, n]
                n += 1
        elif text[i] == "<symbol> , </symbol>":
            if text[i + 1].startswith("<identifier>") and text[i + 1].endswith("</identifier>"):
                name = " ".join(text[i + 1].split()[1:-1])
                symbolClass[name] = [type, cl, n]
                n += 1
        elif text[i] == "<symbol> ; </symbol>":
            return n


def parameterList(text, s, n):
    if len(text) > 2:
        type = " ".join(text[0].split()[1:-1])
        if text[0].startswith("<identifier>") and text[0].endswith("</identifier>"):
            pass
        if text[2].startswith("<identifier>") and text[2].endswith("</identifier>"):
            name = " ".join(text[2].split()[1:-1])
            symbol[s][name] = [type, "argument", n]
            n += 1
    if len(text) > 4:
        for i in range(len(text)):
            if text[i] == "<symbol> , </symbol>":
                type = " ".join(text[i + 1].split()[1:-1])
                if text[i + 1].startswith("<identifier>") and text[i + 1].endswith("</identifier>"):
                    pass
                if text[i + 2].startswith("<identifier>") and text[i + 2].endswith("</identifier>"):
                    name = " ".join(text[i + 2].split()[1:-1])
                    symbol[s][name] = [type, "argument", n]
                    n += 1
    return n
