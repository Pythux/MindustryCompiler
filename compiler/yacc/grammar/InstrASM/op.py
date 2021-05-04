
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def opResultTwoArgs(p: YaccProduction):
    '''ligne : op opTwoArgs ID instrArgs EndLine'''
    args = p[4]
    if len(args) != 2:
        raise err.tooManyArgs(p, 2, len(args))
    p[0] = AsmInst(KeyWord(p[1]), [p[2], Variable(p[3]), *args])


@grammar
def opResultOneArgs(p: YaccProduction):
    '''ligne : op opOneArgs ID instrArgs EndLine'''
    args = p[4]
    if len(args) != 1:
        raise err.tooManyArgs(p, 1, len(args))
    p[0] = AsmInst(KeyWord(p[1]), [p[2], Variable(p[3]), *args])


@grammar
def opKeyword_error(p: YaccProduction):
    '''ligne : op error'''
    raise err.invalideSubInstr(p)


@grammar
def opTwoArgsResult_error(p: YaccProduction):
    '''ligne : op opTwoArgs error
            | op opOneArgs error'''
    raise err.mustBeVar(p, 3)


@grammar
def opTwoArgsArgs_error(p: YaccProduction):
    '''ligne : op opTwoArgs ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 2)


@grammar
def opOneArgsArgs_error(p: YaccProduction):
    '''ligne : op opOneArgs ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, 1)


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
