

from typing import Callable


class GenerateContext:
    p_fun = {}


context = GenerateContext()


def grammar(p_fun: Callable):
    p_name = p_fun.__name__
    if p_name in context.p_fun:
        raise Exception("function {} is defined more than once".format(p_name))
    context.p_fun[p_name] = p_fun
    return p_fun


def generateYaccFunctions():
    breakpoint()
