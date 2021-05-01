
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def endResult(p: YaccProduction):
    '''line : end EndLine'''
    p[0] = AsmInst(KeyWord(p[1]))


@grammar
def end_error(p: YaccProduction):
    '''line : end error'''
    raise err.tooManyArgs(p, 0)
