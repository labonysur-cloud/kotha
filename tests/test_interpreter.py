import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lexer.lexer import tokenize
from parser.parser import parse
from interpreter.interpreter import Interpreter

code = open("examples/hello_world.kotha").read()
tokens_list = tokenize(code)
ast = parse(code)
interpreter = Interpreter()
interpreter.eval(ast)
