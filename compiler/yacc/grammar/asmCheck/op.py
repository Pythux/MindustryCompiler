
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def opResultTwoArgs(p: YaccProduction):
    '''line : op opTwoArgs ID info info EndLine'''
    p[0] = AsmInst(KeyWord(p[1]), [p[2], Variable(p[3]), p[4], p[5]])


@grammar
def opResultOneArgs(p: YaccProduction):
    '''line : op opOneArgs ID info EndLine'''
    p[0] = AsmInst(KeyWord(p[1]), [p[2], Variable(p[3]), p[4]])


@grammar
def opKeyword_error(p: YaccProduction):
    '''line : op error'''
    raise err.invalideSubInstr(p)


@grammar
def opTwoArgsResult_error(p: YaccProduction):
    '''line : op opTwoArgs error
            | op opOneArgs error'''
    raise err.mustBeVar(p, 3, p[3])


@grammar
def opTwoArgsArgs_error(p: YaccProduction):
    '''line : op opTwoArgs ID error
            | op opTwoArgs ID info error'''
    givenArgs = len(p) - 5
    raise err.maybeNotEnoughtArgs(p, 2, givenArgs)


@grammar
def opOneArgsArgs_error(p: YaccProduction):
    '''line : op opOneArgs ID error'''
    givenArgs = len(p) - 5
    raise err.maybeNotEnoughtArgs(p, 1, givenArgs)


@grammar
def opTwoArgsArgsTooMuch_error(p: YaccProduction):
    '''line : op opTwoArgs ID info info error'''
    raise err.tooManyArgs(p, 2)


@grammar
def opOneArgsArgsTooMuch_error(p: YaccProduction):
    '''line : op opOneArgs ID info error'''
    raise err.tooManyArgs(p, 1)


@grammar
def opTwoArgs(p: YaccProduction):
    '''opTwoArgs : add
                 | sub
                 | mul
                 | div
                 | idiv
                 | mod
                 | pow

                 | equal
                 | notEqual
                 | land
                 | lessThan
                 | lessThanEq
                 | greaterThan
                 | strictEqual

                 | shl
                 | shr
                 | or
                 | and
                 | xor
                 | not

                 | max
                 | min
                 | angle
                 | len
                 | noise'''
    p[0] = KeyWord(p[1])


@grammar
def opOneArgs(p: YaccProduction):
    '''opOneArgs : abs
                 | log
                 | log10
                 | sin
                 | cos
                 | tan
                 | floor
                 | ceil
                 | sqrt
                 | rand
        '''
    p[0] = KeyWord(p[1])
