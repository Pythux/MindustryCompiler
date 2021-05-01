
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord


@grammar
def endResult(p: YaccProduction):
    '''line : end EndLine'''
    p[0] = AsmInst(KeyWord(p[1]))


@grammar
def end_errorTooMuch(p: YaccProduction):
    '''line : end error'''
    raise err.tooManyArgs(p, 0)


@grammar
def instrOneArgResult(p: YaccProduction):
    '''line : instrOneArg info EndLine'''
    p[0] = AsmInst(p[1], [p[2]])


@grammar
def instrOneArg_tooMuchArgs(p: YaccProduction):
    '''line : instrOneArg info error'''
    raise err.tooManyArgs(p, 1, line=p[1].lineno)


@grammar
def instrOneArg_MaybeArgsNotEnought(p: YaccProduction):
    '''line : instrOneArg error'''
    raise err.maybeNotEnoughtArgs(p, 1, 0, line=p[1].lineno)


@grammar
def instrOneArg(p: YaccProduction):
    '''instrOneArg : print
                   | printflush
                   | drawflush
                   | ubind'''
    k = KeyWord(p[1])
    k.lineno = p.lineno(1)
    p[0] = k


@grammar
def writeResult(p: YaccProduction):
    '''line : write instrArgs EndLine'''
    if len(p[2]) != 3:
        raise err.tooManyArgs(p, 3, len(p[2]))
    p[0] = AsmInst(p[1], p[2])


@grammar
def write_MaybeArgsNotEnought(p: YaccProduction):
    '''line : write instrArgs error'''
    raise err.maybeNotEnoughtOrTooMuchArgs(p, nbArgsReq=3)


@grammar
def instrArgs(p: YaccProduction):
    '''instrArgs :
                 | info
                 | instrArgs info'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# read result cell1 index
# sensor result block1 @copper
# getlink result linkId
