
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, Value, KeyWord


@grammar
def opResultTwoArgs(p: YaccProduction):
    '''line : op opTwoArgs ID info info EndLine'''
    p[0] = AsmInst(KeyWord(p[1]), [p[2], Variable(p[3]), p[4], p[5]])


@grammar
def opKeyword_error(p: YaccProduction):
    '''line : op error'''
    raise err.invalideSubInstr(p)


@grammar
def opTwoArgsResult_error(p: YaccProduction):
    '''line : op opTwoArgs error'''
    raise err.mustBeVar(p, 3)


@grammar
def opTwoArgsArgs_error(p: YaccProduction):
    '''line : op opTwoArgs ID error
            | op opTwoArgs ID info error'''
    givenArgs = len(p) - 5
    raise err.maybeNotEnoughtArgs(p, 2, givenArgs)


@grammar
def opTwoArgsArgsTooMuch_error(p: YaccProduction):
    '''line : op opTwoArgs ID info info error'''
    raise err.tooManyArgs(p, 2)


@grammar
def opTwoArgs(p: YaccProduction):
    '''opTwoArgs : add'''
    p[0] = KeyWord(p[1])
