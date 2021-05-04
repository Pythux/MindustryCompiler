
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


def invalideSubInstr(p, line=None, valideKeys=None, indexErr=2):
    valideKeys = valideKeys if valideKeys else subInstr[toStrToken(p[1])]
    if p[indexErr].type == 'EndLine':
        return CompilationException(
            getStartMsg(p, line=line, end=', ') +
            "require keyword, must be on of: {}".format(valideKeys))
    return CompilationException(
        getStartMsg(p, line=line, end=', ') +
        "'{}' is not a valide keyword, must be on of: {}".format(toStrToken(p[indexErr]), valideKeys))


def maybeNotEnoughtArgs(p, nbArgsReq, line=None):
    tokenErr = p[len(p) - 1]
    instrArgs = p[len(p) - 2]
    nbArgsGiven = len(instrArgs)
    if tokenErr.type in reserved:
        return reservedKeword(p, tokenErr, line=line)
    elif tokenErr.type == 'EndLine':
        return notEnoughtArgs(p, nbArgsReq, nbArgsGiven, line=line)
    elif tokenErr.type == 'OpenParenthesis':
        return CompilationException(
            getStartMsg(p, line) +
            "is a reserved keyword, it can't be use to function name"
        )
    raise CompilationException(getStartMsg(p, line) + "error found")


def reservedKeword(p, tokenErr, line=None):
    return CompilationException(
        getStartMsg(p, line=line, end=', ') +
        "'{}' is a reserved keyword, it could not be used as variable".format(toStrToken(tokenErr)))


def notEnoughtArgs(p, nbArgsReq, nbArgsGiven, line=None):
    return CompilationException(
        getStartMsg(p, line) + "require {} arguments, {} given".format(nbArgsReq, nbArgsGiven)
    )


def tooManyArgs(p, nbArgsReq, nbArgsGiven, line=None):
    return CompilationException(
        getStartMsg(p, line) + "require {} arguments, {} given".format(nbArgsReq, nbArgsGiven)
    )


def tooManyArgsNameIt(p, tokenErr, line=None):
    return CompilationException(
        getStartMsg(p, line) + "too many arguments, '{}' is exeeding".format(tokenErr.value)
    )


def mustBeVar(p, index, line=None):
    error = p[index]
    strErr = toStrToken(error)
    endMsg = "'{}' not valide".format(strErr)
    if error.type in reserved:
        endMsg = "'{}' is a reserved keyword".format(strErr)
    if error.type == 'EndLine':
        endMsg = "no variable given"
    return CompilationException(
        getStartMsg(p, line) + "require a variable to store result at position {}, {}"
        .format(index, endMsg))
