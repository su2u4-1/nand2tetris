[
    ["class", "startLabel", 0],
    ["class", "keyword", 1],
    ["Main", "identifier", 1],
    ["{", "symbol", 1],
    ["subroutineDec", "startLabel", 1],
    ["function", "keyword", 2],
    ["void", "keyword", 2],
    ["main", "identifier", 2],
    ["(", "symbol", 2],
    ["parameterList", "startLabel", 2],
    ["parameterList", "endLabel", 2],
    [")", "symbol", 2],
    ["subroutineBody", "startLabel", 2],
    ["{", "symbol", 3],
    ["varDec", "startLabel", 3],
    ["var", "keyword", 4],
    ["SquareGame", "identifier", 4],
    ["game", "identifier", 4],
    [";", "symbol", 4],
    ["varDec", "endLabel", 3],
    ["statements", "startLabel", 3],
    ["letStatement", "startLabel", 4],
    ["let", "keyword", 5],
    ["game", "identifier", 5],
    ["=", "symbol", 5],
    ["expression", "startLabel", 5],
    ["term", "startLabel", 6],
    ["SquareGame", "identifier", 7],
    [".", "symbol", 7],
    ["new", "identifier", 7],
    ["(", "symbol", 7],
    ["expressionList", "startLabel", 7],
    ["expressionList", "endLabel", 7],
    [")", "symbol", 7],
    ["term", "endLabel", 6],
    ["expression", "endLabel", 5],
    [";", "symbol", 5],
    ["letStatement", "endLabel", 4],
    ["doStatement", "startLabel", 4],
    ["do", "keyword", 5],
    ["game", "identifier", 5],
    [".", "symbol", 5],
    ["run", "identifier", 5],
    ["(", "symbol", 5],
    ["expressionList", "startLabel", 5],
    ["expressionList", "endLabel", 5],
    [")", "symbol", 5],
    [";", "symbol", 5],
    ["doStatement", "endLabel", 4],
    ["doStatement", "startLabel", 4],
    ["do", "keyword", 5],
    ["game", "identifier", 5],
    [".", "symbol", 5],
    ["dispose", "identifier", 5],
    ["(", "symbol", 5],
    ["expressionList", "startLabel", 5],
    ["expressionList", "endLabel", 5],
    [")", "symbol", 5],
    [";", "symbol", 5],
    ["doStatement", "endLabel", 4],
    ["returnStatement", "startLabel", 4],
    ["return", "keyword", 5],
    [";", "symbol", 5],
    ["returnStatement", "endLabel", 4],
    ["statements", "endLabel", 3],
    ["}", "symbol", 3],
    ["subroutineBody", "endLabel", 2],
    ["subroutineDec", "endLabel", 1],
    ["}", "symbol", 1],
    ["class", "endLabel", 0],
]

{
    0: [
        "dict_class",
        {
            0: ["str_keyword", "class"],
            1: ["str_identifier", "Main"],
            2: ["str_symbol", "{"],
            3: [
                "dict_subroutineDec",
                {
                    0: ["str_keyword", "function"],
                    1: ["str_keyword", "void"],
                    2: ["str_identifier", "main"],
                    3: ["str_symbol", "("],
                    4: ["dict_parameterList", {}],
                    5: ["str_symbol", ")"],
                    6: [
                        "dict_subroutineBody",
                        {
                            0: ["str_symbol", "{"],
                            1: [
                                "dict_varDec",
                                {
                                    0: ["str_keyword", "var"],
                                    1: ["str_identifier", "SquareGame"],
                                    2: ["str_identifier", "game"],
                                    3: ["str_symbol", ";"],
                                },
                            ],
                            2: [
                                "dict_statements",
                                {
                                    0: [
                                        "dict_letStatement",
                                        {
                                            0: ["str_keyword", "let"],
                                            1: ["str_identifier", "game"],
                                            2: ["str_symbol", "="],
                                            3: [
                                                "dict_expression",
                                                {
                                                    0: [
                                                        "dict_term",
                                                        {
                                                            0: ["str_identifier", "SquareGame"],
                                                            1: ["str_symbol", "."],
                                                            2: ["str_identifier", "new"],
                                                            3: ["str_symbol", "("],
                                                            4: ["dict_expressionList", {}],
                                                            5: ["str_symbol", ")"],
                                                        },
                                                    ]
                                                },
                                            ],
                                            4: ["str_symbol", ";"],
                                        },
                                    ],
                                    1: [
                                        "dict_doStatement",
                                        {
                                            0: ["str_keyword", "do"],
                                            1: ["str_identifier", "game"],
                                            2: ["str_symbol", "."],
                                            3: ["str_identifier", "run"],
                                            4: ["str_symbol", "("],
                                            5: ["dict_expressionList", {}],
                                            6: ["str_symbol", ")"],
                                            7: ["str_symbol", ";"],
                                        },
                                    ],
                                    2: [
                                        "dict_doStatement",
                                        {
                                            0: ["str_keyword", "do"],
                                            1: ["str_identifier", "game"],
                                            2: ["str_symbol", "."],
                                            3: ["str_identifier", "dispose"],
                                            4: ["str_symbol", "("],
                                            5: ["dict_expressionList", {}],
                                            6: ["str_symbol", ")"],
                                            7: ["str_symbol", ";"],
                                        },
                                    ],
                                    3: ["dict_returnStatement", {0: ["str_keyword", "return"], 1: ["str_symbol", ";"]}],
                                },
                            ],
                            3: ["str_symbol", "}"],
                        },
                    ],
                },
            ],
            4: ["str_symbol", "}"],
        },
    ]
}
