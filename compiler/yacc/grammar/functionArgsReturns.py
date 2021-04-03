

from ._start import grammar, YaccProduction, context


# x, y, z = fun()
@grammar
def returnedVars_one(p: YaccProduction):
    '''returnedVars : ID'''
    p[0] = [p[1]]


@grammar
def returnedVars_many(p: YaccProduction):
    '''returnedVars : returnedVars Comma ID'''
    p[0] = p[1] + [p[3]]


@grammar
def argumentsCall_one(p: YaccProduction):
    '''argumentsCall : info'''
    p[0] = [p[1]]


@grammar
def argumentsCall_many(p: YaccProduction):
    '''argumentsCall : argumentsCall Comma info'''
    p[0] = p[1] + [p[3]]


@grammar
def argumentsCall_empty(p: YaccProduction):
    '''argumentsCall : '''
    p[0] = []


# register function definition arguments
def addArgument(arg):
    if arg in context.fun.args:
        raise SystemExit('Duplicate parameter "{}"'.format(arg))
    context.fun.args.append(arg)
    context.fun.scopeId(arg)


@grammar
def args_one(p: YaccProduction):
    '''arguments : ID'''
    arg = p[1]
    addArgument(arg)


@grammar
def args_many(p: YaccProduction):
    '''arguments : arguments Comma ID'''
    arg = p[3]
    addArgument(arg)


@grammar
def args_empty(p: YaccProduction):
    '''arguments : '''


# return x, y, z
@grammar
def returnsVal_empty(p: YaccProduction):
    '''returnsVal : '''
    p[0] = []


@grammar
def returnsVal_one(p: YaccProduction):
    '''returnsVal : info'''
    p[0] = [p[1]]


@grammar
def returnsVal_many(p: YaccProduction):
    '''returnsVal : returnsVal Comma info'''
    p[0] = p[1] + [p[3]]
