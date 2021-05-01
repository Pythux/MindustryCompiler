
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
    'op add yo 1 2 3': "line 1, instruction 'op' require 2 arguments, 3 given",
    'op add yo 1 2 3 4 5 6': "line 1, instruction 'op' require 2 arguments, 6 given",
    'op abs': "line 1, instruction 'op' require a variable to store result at position 3",
    'op abs add': "line 1, instruction 'op' require a variable to store result at position 3, 'add' is a reserved keyword",
    'op abs res': "line 1, instruction 'op' require 1 arguments, 0 given",
    'op abs res arg1 arg2': "line 1, instruction 'op' require 1 arguments, 2 given",
}
instrSimple = {
    'end yo': "line 1, instruction 'end' require 0 arguments, 1 given",
}
instrSet = {
    'set': "line 1, instruction 'set' require a variable to store result at position 2, no variable given",
    'set 4': "line 1, instruction 'set' require a variable to store result at position 2, '4' not valide",
    'set @4 2': "line 1, instruction 'set' require a variable to store result at position 2, '@4' not valide",
    'set yo 4 3': "line 1, instruction 'set' require 1 arguments, too much is given",
}
intrOneArg = {
    'print': "line 1, instruction 'print' require 1 arguments, 0 given",
    'printflush': "line 1, instruction 'printflush' require 1 arguments, 0 given",
    'drawflush': "line 1, instruction 'drawflush' require 1 arguments, 0 given",
    'ubind': "line 1, instruction 'ubind' require 1 arguments, 0 given",
    'print 1 2 3': "line 1, instruction 'print' require 1 arguments, too much is given",
    'print 1 2': "line 1, instruction 'print' require 1 arguments, too much is given",
}
instrWrite = {
    'write': "line 1, instruction 'write' require 1 arguments, 0 given",
    'write 1': "6",
    'write add': "6",
    'write set': "6",
    'write 1 set 3': "6",
    'write 1 2 set': "6",
    'white @yo lo "da" ta': "6",
}


errorList = [instrNotValide, subInstrNotValide, instrOp, instrSimple, instrSet, intrOneArg, instrWrite]


def test_asm():
    for dico in errorList:
        for k, v in dico.items():
            assertCompilationException(k, v)

    assert runYacc('op add yo 1 2', clearContext=True) == 'op add yo 1 2\n'
    assert runYacc('op mul yo 1 2', clearContext=True) == 'op mul yo 1 2\n'
    assert runYacc('op abs res arg1', clearContext=True) == 'op abs res arg1\n'
    assert runYacc('end', clearContext=True) == 'end\n'
    assert runYacc('set yo 4', clearContext=True) == 'set yo 4\n'
    assert runYacc('ubind @flare', clearContext=True) == 'ubind @flare\n'