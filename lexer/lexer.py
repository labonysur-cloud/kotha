import ply.lex as lex

# Reserved keywords
reserved = {
    'dekhaw': 'PRINT',
    'jodi': 'IF',
    'othoba': 'ELSE',
    'kaaj': 'FUNCTION',
    'ferot': 'RETURN',
    'user': 'INPUT',
    'array': 'ARRAY',
    'cholbe': 'WHILE',
    'jotokkhon': 'WHILE_CONDITION',
    'theke': 'FROM',
    'porjonto': 'TO',
    'jog': 'ADD',
    'koro': 'DO',
    'gun': 'MUL',
    'vag': 'DIV',
    'vagses': 'MOD',
    'biyog': 'SUB',
    'ebong': 'AND',
    'noy': 'NOT',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'banaw': 'DECLARE',
    'er': 'OF',
    'value': 'VALUE',
    'input': 'INPUT_KEYWORD',
    'new': 'NEW',
}

# Token list
tokens = [
    'ID', 'NUMBER', 'STRING', 'SEMI', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'ASSIGN', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COMMA', 'OR',
] + list(reserved.values())

# Operators/punctuation
t_SEMI = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ASSIGN = r'='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='

# String literal
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # remove quotes
    return t

# Number
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identifier
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignore spaces/tabs
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# Function to use in main.py
def tokenize(code):
    lexer.input(code)
    result = []
    for tok in lexer:
        result.append(tok)
    return result




