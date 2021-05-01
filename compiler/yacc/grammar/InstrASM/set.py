
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def setResult(p: YaccProduction):
    '''line : set ID info EndLine'''
    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), p[3]])


@grammar
def set_tooMuchArgs(p: YaccProduction):
    '''line : set ID info error'''
    raise err.tooManyArgs(p, 1)


@grammar
def set_mustBeID(p: YaccProduction):
    '''line : set error'''
    raise err.mustBeVar(p, 2, p[2])


@grammar
def set_MaybeArgsNotEnought(p: YaccProduction):
    '''line : set ID error'''
    raise err.maybeNotEnoughtOrTooMuchArgs(p, 1)
