from ply import lex


tokens = [
    'VAR',
    'NUM',

    'PLUS',
    'MINUS',
    'TIMES',

    'LE',
    'LT',
    'EQ',
    'NE',
    'GE',
    'GT',

    'LPAREN',
    'RPAREN',

    'COMMA',

    'ASSIGN',

    'SEMICOL',

    'IFELSE',
    'COLON',

    'LBRACK',
    'RBRACK',
    'LBRACE',
    'RBRACE',

    'PRINT',
    'RANDOM',
]

t_ignore = ' \t\v\n\f'

t_VAR = r'[a-zA-Z_][a-zA-Z_0-9]*'


def t_NUM(t):
    r'[-+]?\d+'
    t.value = int(t.value)
    return t


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'

t_LE = r'<='
t_LT = r'<'
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_GT = r'>'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_COMMA = r'\.'

t_ASSIGN = r'='

t_SEMICOL = r';'

t_IFELSE = r'\?'
t_COLON = r':'

t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_PRINT = r'!'
t_RANDOM = r'~'


def t_error(t):
    print("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)


lexer = lex.lex()
