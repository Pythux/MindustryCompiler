'''instr ID xArgs'''

from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, Variable, KeyWord


@grammar
def setResult(p: YaccProduction):
    '''ligne : set ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def set_tooMuchArgs(p: YaccProduction):
    '''ligne : set ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def set_mustBeID(p: YaccProduction):
    '''ligne : set error'''
    raise err.mustBeVar(p, 2)


# read result cell1 index
@grammar
def readResult(p: YaccProduction):
    '''ligne : read ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 2
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def read_tooMuchArgs(p: YaccProduction):
    '''ligne : read ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def read_mustBeID(p: YaccProduction):
    '''ligne : read error'''
    raise err.mustBeVar(p, 2)


# sensor result block1 @copper
@grammar
def sensorResult(p: YaccProduction):
    '''ligne : sensor ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 2
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def sensor_tooMuchArgs(p: YaccProduction):
    '''ligne : sensor ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def sensor_mustBeID(p: YaccProduction):
    '''ligne : sensor error'''
    raise err.mustBeVar(p, 2)


# getlink result linkId
@grammar
def getlinkResult(p: YaccProduction):
    '''ligne : getlink ID instrArgs EndLine'''
    args = p[3]
    nbArgs = 1
    if len(args) != nbArgs:
        raise err.tooManyArgs(p, nbArgs, len(args))

    p[0] = AsmInst(KeyWord(p[1]), [Variable(p[2]), *args])


@grammar
def getlink_tooMuchArgs(p: YaccProduction):
    '''ligne : getlink ID instrArgs error'''
    raise err.maybeNotEnoughtArgs(p, nbArgsReq=1)


@grammar
def getlink_mustBeID(p: YaccProduction):
    '''ligne : getlink error'''
    raise err.mustBeVar(p, 2)
