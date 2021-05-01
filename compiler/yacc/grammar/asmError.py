
from ply.lex import LexToken
from compiler import CompilationException
from compiler.lex.keywords import instr, subInstr, reserved


def toStrToken(t):
    if isinstance(t, LexToken):
        return t.value
    return t


def getStartMsg(p, line=None, end=None):
    lineNb, instr = p.lineno(1), p[1]
    lineNb = lineNb if line is None else line
    return "line {}, instruction '{}'{}".format(lineNb, instr, ' ' if end is None else end)


def invalideInstr(p, line=None):
    return CompilationException(
        getStartMsg(p, line) + "is not valide, valides instuctions are: {}".format(instr)
    )


def invalideSubInstr(p):
    valideKeys = subInstr[toStrToken(p[1])]
    return CompilationException(
        getStartMsg(p, end=', ') +
        "'{}' is not a valide keyword, must be on of: {}".format(toStrToken(p[2]), valideKeys))


def maybeNotEnoughtArgs(p, nbArgsReq, nbArgsGiven):
    tokenErr = p[len(p) - 1]
    if tokenErr.type == 'EndLine':
        return notEnoughtArgs(p, nbArgsReq, nbArgsGiven)
    return reservedKeword(p, tokenErr)


def reservedKeword(p, tokenErr):
    return CompilationException(
        getStartMsg(p) + "'{}' is a reserved keyword, it could not be used as variable".format(toStrToken(tokenErr)))


def notEnoughtArgs(p, nbArgsReq, nbArgsGiven):
    return CompilationException(
        getStartMsg(p) + "require {} arguments, {} given".format(nbArgsReq, nbArgsGiven)
    )


def tooManyArgs(p, nbArgsReq):
    return CompilationException(
        getStartMsg(p) + "require {} arguments, too much is given".format(nbArgsReq)
    )


def mustBeVar(p, index, error):
    endMsg = "not valide"
    if error.type in reserved:
        endMsg = "is a reserved keyword"
    return CompilationException(
        getStartMsg(p) + "require a variable to store result at position {}, '{}' {}"
        .format(index, toStrToken(p[index]), endMsg))
