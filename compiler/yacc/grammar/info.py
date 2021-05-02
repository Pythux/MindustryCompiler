

from ._start import grammar, YaccProduction, context
from ..classes import Variable, Value


@grammar
def info_id(p: YaccProduction):
    '''info : ID'''
    info = Variable(p[1])
    if context.fun.inFunScope:
        p[0] = context.fun.scopeId(info)
        return

    p[0] = info


@grammar
def info(p: YaccProduction):
    '''info : Number
            | String
            | ArobasedInfo
            | True
            | False
    '''
    p[0] = Value(p[1])
