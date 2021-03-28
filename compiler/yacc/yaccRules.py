
from typing import Callable, List, T
from .yaccImport import yacc, YaccProduction

from compiler.lex.mainLex import LexToken

# Required to build parser
from compiler.lex import tokens  # noqa

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


# handle a ref instruction, we store info in refDict and discard information
def p_ref(p: YaccProduction):
    '''noLine : RefJump EndLine'''
    ref = p[1]
    if ref in refDict:
        raise Exception('ref {} already declared'.format(ref))
    refDict[ref] = lineNumber


class Jump:
    def __init__(self, line, ref, condition) -> None:
        self.line = line
        self.ref = ref
        self.asmCondition = condition

    def toLine(self, refDict):
        if self.ref not in refDict:
            print("for jump at line: {}".format(self.line))
            print("ref {} not exist, existing ref: {}".format(self.ref, refDict))
            raise SystemExit()
        return 'jump {ref} {condition}'.format(
            ref=refDict[self.ref], condition=self.asmCondition)


def p_jump_asmCondition(p: YaccProduction):
    '''jump : Jump ID asmCondition EndLine'''
    # get for error message line of jump instruction
    jump = Jump(p.lineno(1), p[2], p[3])
    p[0] = jump


def p_comparison(p: YaccProduction):
    '''asmCondition : info Comparison info'''
    p[0] = p[2][0] + ' ' + str(p[1]) + ' ' + str(p[3])


def p_jump_always(p: YaccProduction):
    '''jump : Jump ID EndLine'''
    p[0] = Jump(p.lineno(1), p[2], 'always true true')


def p_asmCondition(p: YaccProduction):
    '''asmCondition : ID info info'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + str(p[3])


# to keep the "valide ASM will pass"
def p_jump_asmNoRef(p: YaccProduction):
    '''asmInstr : Jump Number asmCondition EndLine'''
    p[0] = p[1] + ' ' + str(p[2]) + ' ' + p[3]


# catch all ASM as it, no processing them
def p_asmLine(p: YaccProduction):
    '''asmInstr : asmValideInstructions EndLine'''
    p[0] = p[1]


# from . import asmInstr


def decoParams(funToCall: Callable):
    def deco(emptyFun):
        def called(p):
            funToCall(p)
        called.__doc__ = funToCall.__doc__
        called.__name__ = funToCall.__name__
        return called
        return funToCall  # does not work, why ?
    return deco


# @decoParams(asmInstr.p_asmLine)
# def p_asmLine(p):
#     pass


# parser = yacc.yacc()

# current_module = __import__(__name__)

# current_module.p_yolo = asmInstr.p_asmLine
# setattr(current_module, 'p_yolo', asmInstr.p_asmLine)



def p_asmFollowInstructions_one(p: YaccProduction):
    '''asmValideInstructions : info'''
    p[0] = str(p[1])


def p_asmFollowInstructions_many(p: YaccProduction):
    '''asmValideInstructions : asmValideInstructions info'''
    p[0] = p[1] + ' ' + str(p[2])



# discard empty lines
def p_noLine(p):
    '''noLine : EndLine'''


def p_info(p: YaccProduction):
    '''info : ID
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


parser = yacc.yacc()
