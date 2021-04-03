

from ._start import grammar, LexToken


# Error rule for syntax errors
@grammar
def error(t: LexToken):
    print("Syntax error in input!")
    if t is not None:
        print("at line: {}, wasn't expecting: {}".format(t.lineno, t.type))
        print("for more information, it's value is: {}".format(t.value))
        raise SystemExit()
    raise SystemExit("end of line reached")
