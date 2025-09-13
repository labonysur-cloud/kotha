from lexer.lexer import tokenize

code = open("examples/hello_world.kotha").read()
tokens = tokenize(code)
for t in tokens:
    print(t)
