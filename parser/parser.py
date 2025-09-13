import ply.yacc as yacc
from lexer.lexer import tokens  # import tokens from your lexer

# AST nodes
class PrintNode:
    def __init__(self, value):
        self.value = value

class AssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class IfNode:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForNode:
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

class FunctionNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnNode:
    def __init__(self, value):
        self.value = value

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class InputNode:
    def __init__(self, var):
        self.var = var

class ArrayDeclareNode:
    def __init__(self, name, size):
        self.name = name
        self.size = size

class BreakNode:
    pass

class ContinueNode:
    pass

# Grammar rules
def p_program(p):
    'program : statements'
    p[0] = p[1]

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement_print(p):
    'statement : PRINT LPAREN expression RPAREN SEMI'
    p[0] = PrintNode(p[3])

def p_statement_assign(p):
    'statement : ID ASSIGN expression SEMI'
    p[0] = AssignNode(p[1], p[3])

def p_statement_if(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statements RBRACE
                 | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    if len(p) == 8:
        p[0] = IfNode(p[3], p[6])
    else:
        p[0] = IfNode(p[3], p[6], p[10])

def p_statement_while(p):
    'statement : WHILE WHILE_CONDITION expression LBRACE statements RBRACE'
    p[0] = WhileNode(p[3], p[5])

def p_statement_for(p):
    'statement : WHILE ID ASSIGN expression FROM expression TO expression LBRACE statements RBRACE'
    p[0] = ForNode(p[2], p[4], p[6], p[9])

def p_statement_function(p):
    'statement : FUNCTION ID LPAREN params RPAREN LBRACE statements RBRACE'
    p[0] = FunctionNode(p[2], p[4], p[7])

def p_statement_return(p):
    'statement : RETURN expression SEMI'
    p[0] = ReturnNode(p[2])

def p_statement_input(p):
    'statement : INPUT OF ID VALUE INPUT_KEYWORD NEW SEMI'
    p[0] = InputNode(p[3])

def p_statement_array(p):
    'statement : ARRAY DECLARE ID LBRACKET expression RBRACKET SEMI'
    p[0] = ArrayDeclareNode(p[3], p[5])

def p_statement_break(p):
    'statement : BREAK SEMI'
    p[0] = BreakNode()

def p_statement_continue(p):
    'statement : CONTINUE SEMI'
    p[0] = ContinueNode()

def p_params(p):
    '''params : params COMMA ID
              | ID
              | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression_unary(p):
    'expression : NOT expression'
    p[0] = BinOpNode(None, 'not', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = p[1]

def p_expression_call(p):
    'expression : ID LPAREN args RPAREN'
    p[0] = CallNode(p[1], p[3])

def p_args(p):
    '''args : args COMMA expression
            | expression
            | empty'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    pass

# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE'),
    ('left', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
)

# Build parser
parser = yacc.yacc()

# Function to parse code
def parse(code):
    return parser.parse(code)
