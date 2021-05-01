
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord


@grammar
def endResult(p: YaccProduction):
    '''line : end instrArgs EndLine'''
    args = p[2]
    nbArgs = 0
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]))


@grammar
def end_errorTooMuch(p: YaccProduction):
    '''line : end instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=0)


@grammar
def instrOneArgResult(p: YaccProduction):
    '''line : instrOneArg instrArgs EndLine'''
    args = p[2]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(p[1], args)


@grammar
def instrOneArg_MaybeArgsNotEnought(p: YaccProduction):
    '''line : instrOneArg instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1, line=p[1].lineno)


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
    args = p[2]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(p[1], p[2])


@grammar
def write_MaybeArgsNotEnought(p: YaccProduction):
    '''line : write instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=3)


# read result cell1 index
# sensor result block1 @copper
# getlink result linkId
