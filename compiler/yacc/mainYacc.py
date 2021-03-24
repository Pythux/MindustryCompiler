#!/usr/bin/env python

# Yacc

from typing import List
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


lineNumber = 0


def p_lines_one(p: YaccProduction):
    '''lines : line'''
    p[0] = [p[1]]
    global lineNumber
    lineNumber += 1


def p_lines_many(p: YaccProduction):
    '''lines : lines line'''
    p[0] = p[1] + p[2]
    global lineNumber
    lineNumber += 1


def p_line(p: YaccProduction):
    '''line : jump
            | asmInstr
    '''
    p[0] = p[1]


def p_lines_empty(p: YaccProduction):
    '''line : noLine'''
    p[0] = ''


refDict = {}


def p_ref(p: YaccProduction):
    '''noLine : RefJump Indent'''
    ref = p[1]
    if refDict[ref] is not None:
        raise Exception('ref {} already declared'.format(ref))
    refDict[ref] = lineNumber


class Jump:
    def __init__(self, ref, condition) -> None:
        self.ref = ref
        self.singleCondition = toAsmSingleCondition(condition)

    def toLine(self, refDict):
        return 'jump {ref} {condition}'.format(
            ref=refDict[self.ref], condition=self.singleCondition)


def toAsmSingleCondition(singleCondition):
    return singleCondition


def p_jump(p: YaccProduction):
    '''jump : Jump Variable condition Indent'''
    jump = Jump(p[2], p[3])
    p[0] = jump


def p_condition(p):
    '''condition : True'''
    p[0] = True


class AsmCondition:
    def __init__(self, operation, infoA, infoB) -> None:
        self.string = operation + ' ' + str(infoA) + ' ' + str(infoB)


def p_asmCondition(p):
    '''asmCondition : Variable info info'''
    p[0] = AsmCondition(p[1], p[2], p[3])


def p_info(p):
    '''info : Variable
            | Number
            | ArobasedInfo
    '''
    p[0] = p[1]


class AsmInstr:
    def __init__(self, string) -> None:
        self.string = string

    def toLine(self):
        return self.string


def p_asmLine(p: YaccProduction):
    '''asmInstr : asmFollowInstructions Indent'''
    p[0] = AsmInstr(p[1])


def p_asmFollowInstructions_one(p: YaccProduction):
    '''asmFollowInstructions : asmFollowInstru'''
    p[0] = str(p[1])


def p_asmFollowInstructions_many(p: YaccProduction):
    '''asmFollowInstructions : asmFollowInstructions asmFollowInstru
    '''
    p[0] = p[1] + ' ' + str(p[2])


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
        stringCode = toLinesOfCode(result)
        print(stringCode)
        content = ''


def toLinesOfCode(li: List[any]):
    lines = []
    for el in li:
        if isinstance(el, AsmInstr):
            lines.append(el.toLine())
        if isinstance(el, Jump):
            lines.append(el.toLine(refDict))
        else:
            raise Exception('wtf')
    return '\n'.join(lines)
