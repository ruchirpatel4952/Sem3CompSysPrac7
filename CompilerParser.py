from ParseTree import ParseTree  # Ensure ParseTree is imported
from Token import Token  # Ensure Token is imported

class CompilerParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def next(self):
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
        return self.current()

    def current(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def have(self, type, value=None):
        token = self.current()
        if token:
            if token.type == type and (value is None or token.value == value):
                return True
        return False

    def mustbe(self, type, value=None):
        if not self.have(type, value):
            raise ParseException(f"Expected {type} {value}, but found {self.current()}")
        token = self.current()
        self.next()
        return token

    def compileProgram(self):
        return self.compileClass()

    def compileClass(self):
        class_tree = ParseTree('class')
        class_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'class').value))
        class_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
        class_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '{').value))

        while self.have('keyword', 'static') or self.have('keyword', 'field'):
            class_tree.addChild(self.compileClassVarDec())

        while self.have('keyword', 'constructor') or self.have('keyword', 'function') or self.have('keyword', 'method'):
            class_tree.addChild(self.compileSubroutine())

        class_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '}').value))
        return class_tree

    def compileClassVarDec(self):
        var_dec_tree = ParseTree('classVarDec')
        var_dec_tree.addChild(ParseTree('keyword', self.mustbe('keyword').value))
        var_dec_tree.addChild(ParseTree('type', self.mustbeType().value))
        var_dec_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))

        while self.have('symbol', ','):
            var_dec_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ',').value))
            var_dec_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))

        var_dec_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ';').value))
        return var_dec_tree

    def compileSubroutine(self):
        subroutine_tree = ParseTree('subroutine')
        subroutine_tree.addChild(ParseTree('keyword', self.mustbe('keyword').value))
        subroutine_tree.addChild(ParseTree('type', self.mustbeType().value))
        subroutine_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
        subroutine_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))

        subroutine_tree.addChild(self.compileParameterList())

        subroutine_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
        subroutine_tree.addChild(self.compileSubroutineBody())

        return subroutine_tree

    def compileParameterList(self):
        parameter_list_tree = ParseTree('parameterList')
        if not self.have('symbol', ')'):
            parameter_list_tree.addChild(ParseTree('type', self.mustbeType().value))
            parameter_list_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))

            while self.have('symbol', ','):
                parameter_list_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ',').value))
                parameter_list_tree.addChild(ParseTree('type', self.mustbeType().value))
                parameter_list_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
        
        return parameter_list_tree

    def compileSubroutineBody(self):
        body_tree = ParseTree('subroutineBody')
        body_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '{').value))

        while self.have('keyword', 'var'):
            body_tree.addChild(self.compileVarDec())

        body_tree.addChild(self.compileStatements())
        body_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '}').value))

        return body_tree

    def compileVarDec(self):
        var_dec_tree = ParseTree('varDec')
        var_dec_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'var').value))
        var_dec_tree.addChild(ParseTree('type', self.mustbeType().value))
        var_dec_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))

        while self.have('symbol', ','):
            var_dec_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ',').value))
            var_dec_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))

        var_dec_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ';').value))
        return var_dec_tree

    def compileStatements(self):
        statements_tree = ParseTree('statements')
        while self.have('keyword'):
            if self.have('keyword', 'let'):
                statements_tree.addChild(self.compileLet())
            elif self.have('keyword', 'if'):
                statements_tree.addChild(self.compileIf())
            elif self.have('keyword', 'while'):
                statements_tree.addChild(self.compileWhile())
            elif self.have('keyword', 'do'):
                statements_tree.addChild(self.compileDo())
            elif self.have('keyword', 'return'):
                statements_tree.addChild(self.compileReturn())
        return statements_tree

    def compileLet(self):
        let_tree = ParseTree('letStatement')
        let_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'let').value))
        let_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))

        if self.have('symbol', '['):
            let_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '[').value))
            let_tree.addChild(self.compileExpression())
            let_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ']').value))

        let_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '=').value))
        let_tree.addChild(self.compileExpression())
        let_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ';').value))

        return let_tree

    def compileIf(self):
        if_tree = ParseTree('ifStatement')
        if_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'if').value))
        if_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))
        if_tree.addChild(self.compileExpression())
        if_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
        if_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '{').value))
        if_tree.addChild(self.compileStatements())
        if_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '}').value))

        if self.have('keyword', 'else'):
            if_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'else').value))
            if_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '{').value))
            if_tree.addChild(self.compileStatements())
            if_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '}').value))

        return if_tree

    def compileWhile(self):
        while_tree = ParseTree('whileStatement')
        while_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'while').value))
        while_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))
        while_tree.addChild(self.compileExpression())
        while_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
        while_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '{').value))
        while_tree.addChild(self.compileStatements())
        while_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '}').value))
        return while_tree

    def compileDo(self):
        do_tree = ParseTree('doStatement')
        do_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'do').value))
        do_tree.addChild(self.compileSubroutineCall())
        do_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ';').value))
        return do_tree

    def compileReturn(self):
        return_tree = ParseTree('returnStatement')
        return_tree.addChild(ParseTree('keyword', self.mustbe('keyword', 'return').value))
        if not self.have('symbol', ';'):
            return_tree.addChild(self.compileExpression())
        return_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ';').value))
        return return_tree

    def compileExpression(self):
        expression_tree = ParseTree('expression')
        expression_tree.addChild(self.compileTerm())
        while self.have('symbol'):
            op = self.current().value
            if op in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
                expression_tree.addChild(ParseTree('symbol', self.mustbe('symbol').value))
                expression_tree.addChild(self.compileTerm())
            else:
                break
        return expression_tree

    def compileTerm(self):
        term_tree = ParseTree('term')
        if self.have('integerConstant'):
            term_tree.addChild(ParseTree('integerConstant', self.mustbe('integerConstant').value))
        elif self.have('stringConstant'):
            term_tree.addChild(ParseTree('stringConstant', self.mustbe('stringConstant').value))
        elif self.have('keyword'):
            term_tree.addChild(ParseTree('keyword', self.mustbe('keyword').value))
        elif self.have('identifier'):
            term_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
            if self.have('symbol', '['):
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '[').value))
                term_tree.addChild(self.compileExpression())
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ']').value))
            elif self.have('symbol', '('):
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))
                term_tree.addChild(self.compileExpressionList())
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
            elif self.have('symbol', '.'):
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '.').value))
                term_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))
                term_tree.addChild(self.compileExpressionList())
                term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
        elif self.have('symbol', '('):
            term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))
            term_tree.addChild(self.compileExpression())
            term_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
        elif self.have('symbol'):
            term_tree.addChild(ParseTree('symbol', self.mustbe('symbol').value))
            term_tree.addChild(self.compileTerm())
        else:
            raise ParseException("Unexpected token: " + str(self.current()))
        return term_tree

    def compileExpressionList(self):
        expression_list_tree = ParseTree('expressionList')
        if not self.have('symbol', ')'):
            expression_list_tree.addChild(self.compileExpression())
            while self.have('symbol', ','):
                expression_list_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ',').value))
                expression_list_tree.addChild(self.compileExpression())
        return expression_list_tree

    def compileSubroutineCall(self):
        subroutine_call_tree = ParseTree('subroutineCall')
        subroutine_call_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
        if self.have('symbol', '.'):
            subroutine_call_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '.').value))
            subroutine_call_tree.addChild(ParseTree('identifier', self.mustbe('identifier').value))
        subroutine_call_tree.addChild(ParseTree('symbol', self.mustbe('symbol', '(').value))
        subroutine_call_tree.addChild(self.compileExpressionList())
        subroutine_call_tree.addChild(ParseTree('symbol', self.mustbe('symbol', ')').value))
        return subroutine_call_tree

    def mustbeType(self):
        if self.have('keyword', 'int') or self.have('keyword', 'char') or self.have('keyword', 'boolean'):
            return self.mustbe('keyword')
        else:
            return self.mustbe('identifier')

class ParseException(Exception):
    pass
