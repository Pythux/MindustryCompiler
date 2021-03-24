#!/usr/bin/env python

# Yacc

from ply import yacc
from ply.yacc import YaccProduction

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


# def p_expression_plus(p):
#     '''expression : expression Plus expression

#     '''
#     #   ^            ^        ^    ^
#     #  p[0]         p[1]     p[2] p[3]

#     p[0] = p[1] + p[3]


def p_jump(p: YaccProduction):
    '''jump : Jump Variable condition Indent'''
    breakpoint()


def p_condition(p):
    '''condition : True'''
    p[0] = True


def p_asmLine(p: YaccProduction):
    '''asmLine : (asmFollowInstru)+ Indent
    '''


def p_asmFollowInstru(p: YaccProduction):
    '''asmFollowInstru : Variable
                       | Number
                       | ArobasedInfo
    '''


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
def buildParser():
    parser = yacc.yacc()
    return parser


# read file given
def runYacc(fileContent: str):
    pass


def runInteractiveYacc():
    parser = yacc.yacc()
    content = ''
    while True:
        try:
            s = input('Yacc >> ')
        except EOFError:
            break
        if s:
            content += s + '\n'
            continue
        result = parser.parse(content)
        print(result)
        content = ''
