from lexer.lexer import tokenize
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser.parser import parse

code = open("examples/hello_world.kotha").read()
tokens_list = tokenize(code)
ast = parse(code)

print(ast)
