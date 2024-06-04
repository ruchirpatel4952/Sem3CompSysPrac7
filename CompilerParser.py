from ParseTree import ParseTree, Token, ParseException

class CompilerParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def next(self):
        if self.current_index < len(self.tokens) - 1:
            self.current_index += 1

    def current(self):
        return self.tokens[self.current_index]

    def have(self, expected_type, expected_value=None):
        token = self.current()
        if expected_value is None:
            return token.getType() == expected_type
        return token.getType() == expected_type and token.getValue() == expected_value

    def mustBe(self, expected_type, expected_value=None):
        if not self.have(expected_type, expected_value):
            raise ParseException(f"Expected {expected_type} {expected_value}, got {self.current().getType()} {self.current().getValue()}")
        token = self.current()
        self.next()
        return token

    def compileProgram(self):
        return self.compileClass()

    def compileClass(self):
        tree = ParseTree("class", "class")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", "class"))
        tree.addChild(self.mustBe("identifier").getValue())  # Adding value of the identifier token
        tree.addChild(self.mustBe("symbol", "{"))

        while self.have("keyword", "static") or self.have("keyword", "field"):
            tree.addChild(self.compileClassVarDec())

        while self.have("keyword", "constructor") or self.have("keyword", "function") or self.have("keyword", "method"):
            tree.addChild(self.compileSubroutine())

        tree.addChild(self.mustBe("symbol", "}"))
        return tree

    def compileClassVarDec(self):
        tree = ParseTree("classVarDec", "classVarDec")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", ["static", "field"]))
        tree.addChild(self.mustBe("keyword", ["int", "char", "boolean"]) or self.mustBe("identifier"))
        tree.addChild(self.mustBe("identifier"))

        while self.have("symbol", ","):
            tree.addChild(self.mustBe("symbol", ","))
            tree.addChild(self.mustBe("identifier"))

        tree.addChild(self.mustBe("symbol", ";"))
        return tree

    def compileSubroutine(self):
        tree = ParseTree("subroutine", "subroutine")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", ["constructor", "function", "method"]))
        tree.addChild(self.mustBe("keyword", ["void", "int", "char", "boolean"]) or self.mustBe("identifier"))
        tree.addChild(self.mustBe("identifier"))
        tree.addChild(self.mustBe("symbol", "("))
        tree.addChild(self.compileParameterList())
        tree.addChild(self.mustBe("symbol", ")"))
        tree.addChild(self.compileSubroutineBody())
        return tree

    def compileParameterList(self):
        tree = ParseTree("parameterList", "parameterList")  # Update ParseTree constructor call
        if not self.have("symbol", ")"):
            tree.addChild(self.mustBe("keyword", ["int", "char", "boolean"]) or self.mustBe("identifier"))
            tree.addChild(self.mustBe("identifier"))

            while self.have("symbol", ","):
                tree.addChild(self.mustBe("symbol", ","))
                tree.addChild(self.mustBe("keyword", ["int", "char", "boolean"]) or self.mustBe("identifier"))
                tree.addChild(self.mustBe("identifier"))

        return tree

    def compileSubroutineBody(self):
        tree = ParseTree("subroutineBody", "subroutineBody")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("symbol", "{"))

        while self.have("keyword", "var"):
            tree.addChild(self.compileVarDec())

        tree.addChild(self.compileStatements())
        tree.addChild(self.mustBe("symbol", "}"))
        return tree

    def compileVarDec(self):
        tree = ParseTree("varDec", "varDec")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", "var"))
        tree.addChild(self.mustBe("keyword", ["int", "char", "boolean"]) or self.mustBe("identifier"))
        tree.addChild(self.mustBe("identifier"))

        while self.have("symbol", ","):
            tree.addChild(self.mustBe("symbol", ","))
            tree.addChild(self.mustBe("identifier"))

        tree.addChild(self.mustBe("symbol", ";"))
        return tree

    def compileStatements(self):
        tree = ParseTree("statements", "statements")  # Update ParseTree constructor call
        while self.have("keyword", ["let", "if", "while", "do", "return"]):
            if self.have("keyword", "let"):
                tree.addChild(self.compileLet())
            elif self.have("keyword", "if"):
                tree.addChild(self.compileIf())
            elif self.have("keyword", "while"):
                tree.addChild(self.compileWhile())
            elif self.have("keyword", "do"):
                tree.addChild(self.compileDo())
            elif self.have("keyword", "return"):
                tree.addChild(self.compileReturn())
        return tree

    def compileLet(self):
        tree = ParseTree("letStatement", "letStatement")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", "let"))
        tree.addChild(self.mustBe("identifier"))

        if self.have("symbol", "["):
            tree.addChild(self.mustBe("symbol", "["))
            tree.addChild(self.compileExpression())
            tree.addChild(self.mustBe("symbol", "]"))

        tree.addChild(self.mustBe("symbol", "="))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe("symbol", ";"))
        return tree

    def compileIf(self):
        tree = ParseTree("ifStatement", "ifStatement")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", "if"))
        tree.addChild(self.mustBe("symbol", "("))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe("symbol", ")"))
        tree.addChild(self.mustBe("symbol", "{"))
        tree.addChild(self.compileStatements())
        tree.addChild(self.mustBe("symbol", "}"))

        if self.have("keyword", "else"):
            tree.addChild(self.mustBe("keyword", "else"))
            tree.addChild(self.mustBe("symbol", "{"))
            tree.addChild(self.compileStatements())
            tree.addChild(self.mustBe("symbol", "}"))

        return tree

    def compileWhile(self):
        tree = ParseTree("whileStatement", "whileStatement")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", "while"))
        tree.addChild(self.mustBe("symbol", "("))
        tree.addChild(self.compileExpression())
        tree.addChild(self.mustBe("symbol", ")"))
        tree.addChild(self.mustBe("symbol", "{"))
        tree.addChild(self.compileStatements())
        tree.addChild(self.mustBe("symbol", "}"))
        return tree

    def compileDo(self):
        tree = ParseTree("doStatement", "doStatement")  # Update ParseTree constructor call
        tree.addChild(self.mustBe("keyword", "do"))
        tree.addChild(self.compileSubroutineCall())
        tree.addChild(self.mustBe("symbol", ";"))
        return tree
    
    def compileReturn(self):
        tree = ParseTree("returnStatement")
        tree.addChild(self.mustBe("keyword", "return"))

        if not self.have("symbol", ";"):
            tree.addChild(self.compileExpression())

        tree.addChild(self.mustBe("symbol", ";"))
        return tree

    def compileExpression(self):
        tree = ParseTree("expression")
        tree.addChild(self.compileTerm())

        while self.have("symbol", ["+", "-", "*", "/", "&", "|", "<", ">", "="]):
            tree.addChild(self.mustBe("symbol"))
            tree.addChild(self.compileTerm())

        return tree

    def compileTerm(self):
        tree = ParseTree("term")

        if self.have("integerConstant"):
            tree.addChild(self.mustBe("integerConstant"))
        elif self.have("stringConstant"):
            tree.addChild(self.mustBe("stringConstant"))
        elif self.have("keyword", ["true", "false", "null", "this"]):
            tree.addChild(self.mustBe("keyword"))
        elif self.have("identifier"):
            tree.addChild(self.mustBe("identifier"))
            if self.have("symbol", "["):
                tree.addChild(self.mustBe("symbol", "["))
                tree.addChild(self.compileExpression())
                tree.addChild(self.mustBe("symbol", "]"))
            elif self.have("symbol", "("):
                tree.addChild(self.mustBe("symbol", "("))
                tree.addChild(self.compileExpressionList())
                tree.addChild(self.mustBe("symbol", ")"))
            elif self.have("symbol", "."):
                tree.addChild(self.mustBe("symbol", "."))
                tree.addChild(self.mustBe("identifier"))
                tree.addChild(self.mustBe("symbol", "("))
                tree.addChild(self.compileExpressionList())
                tree.addChild(self.mustBe("symbol", ")"))
        elif self.have("symbol", "("):
            tree.addChild(self.mustBe("symbol", "("))
            tree.addChild(self.compileExpression())
            tree.addChild(self.mustBe("symbol", ")"))
        elif self.have("symbol", ["-", "~"]):
            tree.addChild(self.mustBe("symbol"))
            tree.addChild(self.compileTerm())
        else:
            raise ParseException(f"Unexpected token {self.current().getType()} {self.current().getValue()}")

        return tree

    def compileExpressionList(self):
        tree = ParseTree("expressionList")

        if not self.have("symbol", ")"):
            tree.addChild(self.compileExpression())
            while self.have("symbol", ","):
                tree.addChild(self.mustBe("symbol", ","))
                tree.addChild(self.compileExpression())

        return tree

    def compileSubroutineCall(self):
        tree = ParseTree("subroutineCall")
        tree.addChild(self.mustBe("identifier"))

        if self.have("symbol", "."):
            tree.addChild(self.mustBe("symbol", "."))
            tree.addChild(self.mustBe("identifier"))

        tree.addChild(self.mustBe("symbol", "("))
        tree.addChild(self.compileExpressionList())
        tree.addChild(self.mustBe("symbol", ")"))

        return tree

if __name__ == "__main__":
    tokens = [
        Token("keyword", "class"),
        Token("identifier", "MyClass"),
        Token("symbol", "{"),
        Token("symbol", "}")
    ]

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException as e:
        print(f"Error Parsing: {e}")
