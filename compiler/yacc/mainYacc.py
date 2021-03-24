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
expression : expression Plus expression
           | expression Minus expression
           | expression Multiply expression
           | expression Divide expression
           | LeftParentheses expression RightParentheses
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


def p_lines_one(p: YaccProduction):
    '''lines : line'''
    p[0] = p[1]


def p_lines_many(p: YaccProduction):
    '''lines : lines line'''
    p[0] = p[1] + p[2]


def p_line(p: YaccProduction):
    '''line : jump
            | asmLine
    '''
    p[0] = p[1]


def p_lines_empty(p: YaccProduction):
    '''line : noLine'''
    p[0] = ''


def p_ref(p: YaccProduction):
    '''noLine : RefJump Indent'''


def p_jump(p: YaccProduction):
    '''jump : Jump Variable condition Indent'''
    p[0] = p[1] + ' ' + p[2] + ' ' + str(p[3])


def p_condition(p):
    '''condition : True'''
    p[0] = True


def p_asmLine(p: YaccProduction):
    '''asmLine : asmFollowInstructions Indent'''
    p[0] = p[1] + '\n' + (' '*4 * p[2])


def p_asmFollowInstructions_one(p: YaccProduction):
    '''asmFollowInstructions : asmFollowInstru'''
    p[0] = p[1]


def p_asmFollowInstructions_many(p: YaccProduction):
    '''asmFollowInstructions : asmFollowInstructions asmFollowInstru
    '''
    p[0] = str(p[1]) + ' ' + str(p[2])


def p_asmFollowInstru(p: YaccProduction):
    '''asmFollowInstru : Variable
                       | Number
                       | ArobasedInfo
    '''
    p[0] = p[1]


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
