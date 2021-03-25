
# Yacc

from typing import List
from ply import yacc
from ply.yacc import YaccProduction

# Get the token map from the lexer.  This is required.
from compiler.lex import tokens  # noqa
from compiler.lex.mainLex import LexToken


lineNumber = 0


# trac lineNumber to #ref it
def p_lines_one(p: YaccProduction):
    '''lines : line'''
    line = p[1]
    if line is None:
        p[0] = []
    else:
        p[0] = [p[1]]
        global lineNumber
        lineNumber += 1


# add a line to lines
def p_lines_many(p: YaccProduction):
    '''lines : lines line'''
    line = p[2]
    if line is None:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]
        global lineNumber
        lineNumber += 1


# a line is ether a jump instruction or an asmInstr
def p_line(p: YaccProduction):
    '''line : jump
            | asmInstr
    '''
    p[0] = p[1]


# no p[0] =, we don't bubble it, just dircarded
def p_lines_empty(p: YaccProduction):
    '''line : noLine'''


# will be used to store: ref -> code line
refDict = {}


# discard empty lines
def p_noLine(p):
    '''noLine : Indent'''


# handle a ref instruction, we store info in refDict and discard information
def p_ref(p: YaccProduction):
    '''noLine : RefJump Indent'''
    ref = p[1]
    if ref in refDict:
        raise Exception('ref {} already declared'.format(ref))
    refDict[ref] = lineNumber


class Jump:
    def __init__(self, ref, condition=None) -> None:
        self.ref = ref
        self.asmCondition = condition

    def toLine(self, refDict):
        if self.ref not in refDict:
            raise Exception("ref {} not exist, refDict: {}".format(self.ref, refDict))
        return 'jump {ref} {condition}'.format(
            ref=refDict[self.ref], condition=self.singleCondition)


def p_jump(p: YaccProduction):
    '''jump : Jump ID asmCondition Indent
    '''
    jump = Jump(p[2], p[3])
    p[0] = jump


def p_jump_always(p):
    '''jump : Jump ID Indent'''
    p[0] = Jump(p[2])


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
    '''asmInstr : asmValideInstructions Indent'''
    p[0] = AsmInstr(p[1])


def p_asmFollowInstructions_one(p: YaccProduction):
    '''asmValideInstructions : value'''
    p[0] = str(p[1])


def p_asmFollowInstructions_many(p: YaccProduction):
    '''asmValideInstructions : asmValideInstructions value'''
    p[0] = p[1] + ' ' + str(p[2])


def p_asmFollowInstru(p: YaccProduction):
    '''value : ID
             | Number
             | String
             | ArobasedInfo
    '''
    p[0] = p[1]


# Error rule for syntax errors
def p_error(t: LexToken):
    print("Syntax error in input!")
    print("at line: {}, wasn't expecting: {}".format(t.lineno, t.type))
    print("for more information, it's value is: {}".format(t.value))
    raise SystemExit()


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


def runInteractiveYacc():
    content = ''
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if s:
            content += s + '\n'
            continue
        if content == '':
            continue
        print(runYacc(content))
        content = ''
        # cleanData()


def cleanData():
    global refDict
    refDict = {}
