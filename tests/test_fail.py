
import pytest

from compiler import CompilationException
from compiler.yacc.mainYacc import runYacc


def assertCompilationException(code, exceptionSubStr):
    with pytest.raises(CompilationException) as e:
        runYacc(code, clearContext=True)
    assert exceptionSubStr in str(e.value)


instrNotValide = {
    'x': "line 1, instruction 'x' is not valide",
    '4': "line 1, instruction '4' is not valide",
    '@yo': "line 1, instruction '@yo' is not valide",
    '"x"': "line 1, instruction '\"x\"' is not valide",
    'x y z': "line 1, instruction 'x' is not valide",
    '4 y z': "line 1, instruction '4' is not valide",
    '@yo y z': "line 1, instruction '@yo' is not valide",
    'op y': "line 1, instruction 'op', 'y' is not a valide keyword",
}


subInstrNotValide = {
    'op x': "line 1, instruction 'op', 'x' is not a valide keyword, must be on of:",
    'op 4': "line 1, instruction 'op', '4' is not a valide keyword",
    'op @yo': "line 1, instruction 'op', '@yo' is not a valide keyword",
    'op "hi"': "line 1, instruction 'op', '\"hi\"' is not a valide keyword",
}


instrOp = {
    'op add 4 1': "line 1, instruction 'op' require a variable to store result at position 3, '4' not valide",
    'op add yo': "line 1, instruction 'op' require 2 arguments, 0 given",
    'op add yo 1': "line 1, instruction 'op' require 2 arguments, 1 given",
    'op add yo 1 2 3': "line 1, instruction 'op' require 2 arguments, too much is given",
    'op add yo 1 2 3 4 5 6': "line 1, instruction 'op' require 2 arguments, too much is given",
}


def test_asm():
    for dico in [instrNotValide, subInstrNotValide, instrOp]:
        for k, v in dico.items():
            assertCompilationException(k, v)
