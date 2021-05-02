'''instr 0+ args'''

from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord


@grammar
def endResult(p: YaccProduction):
    '''ligne : end instrArgs EndLine'''
    args = p[2]
    nbArgs = 0
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]))


@grammar
def end_errorTooMuch(p: YaccProduction):
    '''ligne : end instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=0)


@grammar
def instrOneArgResult(p: YaccProduction):
    '''ligne : instrOneArg instrArgs EndLine'''
    args = p[2]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args), line=p[1].lineno)

    p[0] = AsmInst(p[1], args)


@grammar
def instrOneArg_MaybeArgsNotEnought(p: YaccProduction):
    '''ligne : instrOneArg instrArgs error'''
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
    '''ligne : write instrArgs EndLine'''
    args = p[2]
    nbArgs = 3
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(p[1], p[2])


@grammar
def write_MaybeArgsNotEnought(p: YaccProduction):
    '''ligne : write instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=3)
