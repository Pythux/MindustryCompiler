#!/usr/bin/env python

# Yacc

from ply import yacc

# Get the token map from the lexer.  This is required.
from compiler.lex import tokens  # noqa


# Dealing With Ambiguous Grammars
precedence = (
    ('left', 'Plus', 'Minus'),  # left associative because must choose one
    ('left', 'Multiply', 'Divide'),
)
# will give:
# Plus      : level = 1,  assoc = 'left'
# Minus     : level = 1,  assoc = 'left'
# Multiply  : level = 2,  assoc = 'left'
# Divide    : level = 2,  assoc = 'left'

'''
expression : expression PLUS expression
           | expression MINUS expression
           | expression TIMES expression
           | expression DIVIDE expression
           | LPAREN expression RPAREN
           | NUMBER
'''

# def p_expression(p):
#     '''expression : expression PLUS expression
#                   | expression MINUS expression'''
#     if p[2] == '+':
#         p[0] = p[1] + p[3]
#     elif p[2] == '-':
#         p[0] = p[1] - p[3]


def p_expression_plus(p):
    '''expression : expression Plus expression

    '''
    #   ^            ^        ^    ^
    #  p[0]         p[1]     p[2] p[3]

    p[0] = p[1] + p[3]


def p_expression_minus(p):
    'expression : expression Minus term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_multiply(p):
    'term : term Multiply factor'
    p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term Divide factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : Number'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
def buildParser():
    parser = yacc.yacc()
    return parser


def runInteractiveYacc():
    # parser = yacc.yacc(write_tables=False)
    parser = yacc.yacc()
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
