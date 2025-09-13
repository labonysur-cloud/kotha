from parser.parser import parse
from interpreter.interpreter import Interpreter

def main():
    with open("examples/hello_world.kotha") as f:
        code = f.read()

    ast = parse(code)
    interpreter = Interpreter()
    interpreter.eval(ast)

if __name__ == "__main__":
    main()
