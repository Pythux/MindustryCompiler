
from compiler import CompilationException
from ._start import grammar, LexToken


# Error rule for syntax errors
@grammar
def error(t: LexToken):
    print("Syntax error in input!")
    if t is not None:
        raise CompilationException("at line: {}, wasn't expecting: {}".format(t.lineno, t.type))
    raise CompilationException("end of line reached")
