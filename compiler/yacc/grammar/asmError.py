

from compiler import CompilationException


def getStartMsg(lineNb, instr):
    return "line {}, instruction '{}' ".format(lineNb, instr)


def notEnoughtArgs(lineNb, instr, nbArgsReq, nbArgsGiven):
    return CompilationException(
        getStartMsg(lineNb, instr) + "require {} arguments, {} given".format(nbArgsReq, nbArgsGiven)
    )


def tooManyArgs(lineNb, instr, nbArgsReq):
    return CompilationException(
        getStartMsg(lineNb, instr) + "require {} arguments, too much is given".format(nbArgsReq)
    )
