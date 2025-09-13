from lexer.lexer import tokenize
from parser.parser import parse

code = open("examples/hello_world.kotha").read()
tokens_list = tokenize(code)
ast = parse(tokens_list)

print(ast)
