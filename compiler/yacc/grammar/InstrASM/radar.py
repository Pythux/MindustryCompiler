
from .._start import grammar, YaccProduction
from .. import asmError as err
from ...classes import AsmInst, KeyWord
from compiler import CompilationException
from compiler.lex import keywords


# uradar enemy any any distance 0 order result
# radar enemy any flying distance turret1 sortOrder result
@grammar
def radarResult(p: YaccProduction):
    '''ligne : radar radarTarget radarTarget radarTarget radarSort info info variable EndLine
             | uradar radarTarget radarTarget radarTarget radarSort info info variable EndLine'''
    p[0] = AsmInst(KeyWord(p[1]), p[2:len(p)-1])


@grammar
def radarTooManyArgs(p: YaccProduction):
    '''ligne : radar radarTarget radarTarget radarTarget radarSort info info variable error
             | uradar radarTarget radarTarget radarTarget radarSort info info variable error'''
    raise CompilationException(err.getStartMsg(p) + "too many arguments")


@grammar
def radarNotAnID(p: YaccProduction):
    '''ligne : radar radarTarget radarTarget radarTarget radarSort info info error
             | uradar radarTarget radarTarget radarTarget radarSort info info error'''
    raise err.mustBeVar(p, 8)


@grammar
def radarMaybeNotEnought(p: YaccProduction):
    '''ligne : radar radarTarget radarTarget radarTarget radarSort error
             | uradar radarTarget radarTarget radarTarget radarSort error'''
    tokenErr = p[len(p)-1]
    startMsg = err.getStartMsg(p)
    if tokenErr.type == 'EndLine':
        raise CompilationException(
            startMsg + "not enought arguments"
        )

    raise err.reservedKeword(p, tokenErr)


@grammar
def radarMaybeNotEnought2(p: YaccProduction):
    '''ligne : radar radarTarget radarTarget radarTarget error
             | uradar radarTarget radarTarget radarTarget error'''
    tokenErr = p[len(p)-1]
    startMsg = err.getStartMsg(p)
    endmsg = 'only 3 arguments provided'
    if tokenErr.type != 'EndLine':
        endmsg = "'{}' given instead".format(tokenErr.value)

    raise CompilationException(
        startMsg + "the 4th argument of this instruction must be one of: {}, ".format(keywords.radarSort) + endmsg)


@grammar
def radarMaybeNotEnought3(p: YaccProduction):
    '''ligne : radar error
             | uradar error'''
    tokenErr = p[len(p)-1]
    startMsg = err.getStartMsg(p)
    if tokenErr.type != 'EndLine':
        raise CompilationException(
            startMsg + "the first three arguments of this instruction must be one of: {}".format(keywords.radarTarget) +
            ", '{}' given instead".format(tokenErr.value))

    raise CompilationException(
        startMsg + "not enought arguments, the first three arguments of this instruction must be one of: {}"
        .format(keywords.radarTarget))


@grammar
def radarTarget(p: YaccProduction):
    '''radarTarget : any
                   | enemy
                   | ally
                   | player
                   | attacker
                   | flying
                   | ground
                   | boss'''
    p[0] = KeyWord(p[1])


@grammar
def radarSort(p: YaccProduction):
    '''radarSort : distance
                 | health
                 | shield
                 | armor
                 | maxHealth'''
    p[0] = KeyWord(p[1])
