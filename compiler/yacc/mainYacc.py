
# Yacc

from typing import List
from ply import yacc
from ply.yacc import YaccProduction

# Get the token map from the lexer.  This is required.
from compiler.lex import tokens  # noqa


# Dealing With Ambiguous Grammars
# precedence = (
#     ('left', 'Plus', 'Minus'),  # left associative because must choose one
#     ('left', 'Multiply', 'Divide'),
# )
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
           | Number
'''

# def p_expression_plus(p):
#     '''expression : expression Plus expression

#     '''
#     #   ^            ^        ^    ^
#     #  p[0]         p[1]     p[2] p[3]

#     p[0] = p[1] + p[3]


lineNumber = 0


def p_lines_one(p: YaccProduction):
    '''lines : line'''
    line = p[1]
    if line is None:
        p[0] = []
    else:
        p[0] = [p[1]]
        global lineNumber
        lineNumber += 1


def p_lines_many(p: YaccProduction):
    '''lines : lines line'''
    line = p[2]
    if line is None:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]
        global lineNumber
        lineNumber += 1


def p_line(p: YaccProduction):
    '''line : jump
            | asmInstr
    '''
    p[0] = p[1]


def p_lines_empty(p: YaccProduction):
    '''line : noLine'''


refDict = {}


def p_ref(p: YaccProduction):
    '''noLine : RefJump Indent'''
    ref = p[1]
    if ref in refDict:
        raise Exception('ref {} already declared'.format(ref))
    refDict[ref] = lineNumber


class Jump:
    def __init__(self, ref, condition) -> None:
        self.ref = ref
        self.singleCondition = toAsmSingleCondition(condition)

    def toLine(self, refDict):
        if self.ref not in refDict:
            raise Exception("ref {} not exist, refDict: {}".format(self.ref, refDict))
        return 'jump {ref} {condition}'.format(
            ref=refDict[self.ref], condition=self.singleCondition)


def toAsmSingleCondition(singleCondition):
    if isinstance(singleCondition, AsmCondition):
        return singleCondition
    return singleCondition


def p_jump(p: YaccProduction):
    '''jump : Jump ID condition Indent
            | Jump ID asmCondition Indent
    '''
    jump = Jump(p[2], p[3])
    p[0] = jump


def p_condition(p):
    '''condition : True
                 | False
    '''
    p[0] = p[1]


class AsmCondition:
    def __init__(self, operation, infoA, infoB) -> None:
        self.string = operation + ' ' + str(infoA) + ' ' + str(infoB)


def p_asmCondition(p):
    '''asmCondition : ID info info'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + str(p[3])


def p_info(p):
    '''info : ID
            | Number
            | ArobasedInfo
    '''
    p[0] = p[1]


class AsmInstr:
    def __init__(self, string) -> None:
        self.string = string

    def toLine(self):
        return self.string


# catch all ASM as it, no processing them
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
    '''asmFollowInstru : ID
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
def runYacc(content: str):
    parser = yacc.yacc()
    lines = parser.parse(content)
    stringCode = changeRefToLineNumber(lines)
    return stringCode


# we only have at this moment AsmInstr or Jump Objects in lines
def changeRefToLineNumber(li: List[any]):
    lines = []
    for el in li:
        if isinstance(el, AsmInstr):
            lines.append(el.toLine())
        elif isinstance(el, Jump):
            lines.append(el.toLine(refDict))
        else:
            raise Exception('wtf')
    return '\n'.join(lines)


# python -m pdb -c continue compiler/__main__.py -i --yacc
def runInteractiveYacc():
    content = ''
    while True:
        try:
            s = input('Yacc >> ')
        except EOFError:
            break
        if s:
            content += s + '\n'
            continue
        if content == '':
            continue
        print(runYacc(content))
        content = ''
        cleanData()


def cleanData():
    global refDict
    refDict = {}
