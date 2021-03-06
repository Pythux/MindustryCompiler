

from compiler import CompilationException
from typing import Callable
from pathlib import PurePath
import os


class Context:
    p_fun = {}
    p_imports = {}
    precedence = None


context = Context()


# a decorator to get grammar function (ak: p_fun)
# use it to declare a p_function
def grammar(p_fun: Callable):
    p_name = p_fun.__name__
    if p_name in context.p_fun:
        raise CompilationException("function {} is defined more than once".format(p_name))
    context.p_fun[p_name] = p_fun
    p_import = p_fun.__module__
    if p_import not in context.p_imports:
        context.p_imports[p_import] = True
    return p_fun


def precedence(precedence):
    context.precedence = precedence


fileInfo = '''
# This file is automatically generated. Do not edit.'''


lexTokenImport = '''
from ply import yacc

# Required to build parser
from compiler.lex import tokens  # noqa
'''


def getGeneratedContent():
    c = []
    c.append(fileInfo)
    c.append('')
    c.append(lexTokenImport)
    c.append('')

    for p_import in list(context.p_imports.keys()):
        c.append('import {}'.format(p_import))

    c.append('\n')

    if context.precedence is not None:
        c.append('precedence = ' + str(context.precedence))

    c.append('\n')

    for p_fun in list(context.p_fun.values()):
        fun_name = p_fun.__name__
        fun_doc = p_fun.__doc__
        fun_module = p_fun.__module__
        c.append('def p_{fun_name}(p):'.format(fun_name=fun_name))
        c.append("    '''{fun_doc}'''".format(fun_doc=fun_doc))
        c.append('    {fun_module}.{fun_name}(p)'.format(fun_module=fun_module, fun_name=fun_name))
        c.append('\n')

    c.append('parser = yacc.yacc()')

    strContent = '\n'.join(c) + '\n'
    return strContent


# confused with open mode w, w+ ? here the link:
# https://stackoverflow.com/questions/1466000/difference-between-modes-a-a-w-w-and-r-in-built-in-open-function/30566011#30566011
def generateYaccFunctions():
    generatedContent = getGeneratedContent()
    generatedFile = PurePath(os.path.dirname(__file__), 'p_functionYacc.py')
    changed = True
    if os.path.isfile(generatedFile):
        with open(generatedFile, 'r') as fd:
            changed = generatedContent != fd.read()

    if changed:
        print('grammar functions have changed, rewriting module p_functionYacc')
        with open(generatedFile, 'w') as fd:
            fd.write(generatedContent)
