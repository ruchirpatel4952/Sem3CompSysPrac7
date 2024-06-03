from CompilerParser import CompilerParser
from ParseTree import ParseTree
from Token import Token

tokens = [
    Token('keyword', 'class'),
    Token('identifier', 'Main'),
    Token('symbol', '{'),
    Token('keyword', 'static'),
    Token('keyword', 'int'),
    Token('identifier', 'a'),
    Token('symbol', ';'),
    Token('symbol', '}')
]

parser = CompilerParser(tokens)
parse_tree = parser.compileProgram()
print(parse_tree)
