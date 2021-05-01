'''instr ID xArgs'''

from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def setResult(p: YaccProduction):
    '''line : set ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def set_tooMuchArgs(p: YaccProduction):
    '''line : set ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def set_mustBeID(p: YaccProduction):
    '''line : set error'''
    raise err.mustBeVar(p, 2)


# read result cell1 index
@grammar
def readResult(p: YaccProduction):
    '''line : read ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 2
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def read_tooMuchArgs(p: YaccProduction):
    '''line : read ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def read_mustBeID(p: YaccProduction):
    '''line : read error'''
    raise err.mustBeVar(p, 2)


# sensor result block1 @copper
@grammar
def sensorResult(p: YaccProduction):
    '''line : sensor ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 2
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def sensor_tooMuchArgs(p: YaccProduction):
    '''line : sensor ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def sensor_mustBeID(p: YaccProduction):
    '''line : sensor error'''
    raise err.mustBeVar(p, 2)


# getlink result linkId
@grammar
def getlinkResult(p: YaccProduction):
    '''line : getlink ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def getlink_tooMuchArgs(p: YaccProduction):
    '''line : getlink ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def getlink_mustBeID(p: YaccProduction):
    '''line : getlink error'''
    raise err.mustBeVar(p, 2)
