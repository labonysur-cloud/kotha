import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lexer.lexer import tokenize

code = open("examples/hello_world.kotha").read()
tokens = tokenize(code)
for t in tokens:
    print(t)
