from parser.parser import PrintNode, AssignNode, BinOpNode, IfNode, WhileNode, ForNode, FunctionNode, ReturnNode, CallNode, InputNode, ArrayDeclareNode, BreakNode, ContinueNode

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Variable '{name}' not defined")

    def set(self, name, value):
        self.vars[name] = value

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.functions = {}

    def eval(self, node, env=None):
        if env is None:
            env = self.global_env

        if isinstance(node, list):
            result = None
            for stmt in node:
                result = self.eval(stmt, env)
                if isinstance(result, ReturnValue):
                    return result
            return result

        if isinstance(node, PrintNode):
            value = self.eval(node.value, env)
            print(value)
            return None

        if isinstance(node, AssignNode):
            value = self.eval(node.value, env)
            env.set(node.name, value)
            return value

        if isinstance(node, BinOpNode):
            left = self.eval(node.left, env) if node.left is not None else None
            right = self.eval(node.right, env)
            op = node.op
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '%':
                return left % right
            elif op == '>':
                return left > right
            elif op == '<':
                return left < right
            elif op == '>=':
                return left >= right
            elif op == '<=':
                return left <= right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == 'and':
                return left and right
            elif op == 'or':
                return left or right
            elif op == 'not':
                return not right
            else:
                raise Exception(f"Unknown operator {op}")

        if isinstance(node, IfNode):
            cond = self.eval(node.condition, env)
            if cond:
                return self.eval(node.then_branch, env)
            elif node.else_branch:
                return self.eval(node.else_branch, env)
            return None

        if isinstance(node, WhileNode):
            while self.eval(node.condition, env):
                result = self.eval(node.body, env)
                if isinstance(result, BreakSignal):
                    break
                if isinstance(result, ContinueSignal):
                    continue
                if isinstance(result, ReturnValue):
                    return result
            return None

        if isinstance(node, ForNode):
            start = self.eval(node.start, env)
            end = self.eval(node.end, env)
            env.set(node.var, start)
            i = start
            while i <= end:
                env.set(node.var, i)
                result = self.eval(node.body, env)
                if isinstance(result, BreakSignal):
                    break
                if isinstance(result, ContinueSignal):
                    i += 1
                    continue
                if isinstance(result, ReturnValue):
                    return result
                i += 1
            return None

        if isinstance(node, FunctionNode):
            self.functions[node.name] = node
            return None

        if isinstance(node, ReturnNode):
            value = self.eval(node.value, env)
            return ReturnValue(value)

        if isinstance(node, CallNode):
            func = self.functions.get(node.name)
            if not func:
                raise Exception(f"Function {node.name} not defined")
            if len(func.params) != len(node.args):
                raise Exception(f"Function {node.name} expects {len(func.params)} arguments, got {len(node.args)}")
            new_env = Environment(self.global_env)
            for param, arg in zip(func.params, node.args):
                new_env.set(param, self.eval(arg, env))
            result = self.eval(func.body, new_env)
            if isinstance(result, ReturnValue):
                return result.value
            return None

        if isinstance(node, InputNode):
            value = input(f"Enter value for {node.var}: ")
            env.set(node.var, value)
            return value

        if isinstance(node, ArrayDeclareNode):
            size = self.eval(node.size, env)
            env.set(node.name, [None] * size)
            return None

        if isinstance(node, BreakNode):
            return BreakSignal()

        if isinstance(node, ContinueNode):
            return ContinueSignal()

        if isinstance(node, int) or isinstance(node, str):
            return node

        if isinstance(node, str):
            return env.get(node)

        raise Exception(f"Unknown node type: {type(node)}")

class ReturnValue:
    def __init__(self, value):
        self.value = value

class BreakSignal:
    pass

class ContinueSignal:
    pass
