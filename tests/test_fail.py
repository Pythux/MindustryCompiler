
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
    'set yo 4 3': "line 1, instruction 'set' require 1 arguments, 2 given",
}
intrOneArg = {
    'print': "line 1, instruction 'print' require 1 arguments, 0 given",
    'printflush': "line 1, instruction 'printflush' require 1 arguments, 0 given",
    'drawflush': "line 1, instruction 'drawflush' require 1 arguments, 0 given",
    'ubind': "line 1, instruction 'ubind' require 1 arguments, 0 given",
    'print 1 2 3': "line 1, instruction 'print' require 1 arguments, 3 given",
    'print 1 2': "line 1, instruction 'print' require 1 arguments, 2 given",
}
instrWrite = {
    'write': "line 1, instruction 'write' require 3 arguments, 0 given",
    'write 1': "line 1, instruction 'write' require 3 arguments, 1 given",
    'write add': "line 1, instruction 'write', 'add' is a reserved keyword, it could not be used as variable",
    'write set': "line 1, instruction 'write', 'set' is a reserved keyword, it could not be used as variable",
    'write 1 set 3': "line 1, instruction 'write', 'set' is a reserved keyword, it could not be used as variable",
    'write 1 2 set': "line 1, instruction 'write', 'set' is a reserved keyword, it could not be used as variable",
    'write @yo lo "da" ta': "line 1, instruction 'write' require 3 arguments, 4 given",
}
instrRead = {
    'read': "line 1, instruction 'read' require a variable to store result at position 2, no variable given",
    'read 4': "line 1, instruction 'read' require a variable to store result at position 2, '4' not valide",
    'read "res"': """line 1, instruction \'read\' require a variable to store result at position 2, \'"res"\' not valide""",
    'read res': "line 1, instruction 'read' require 2 arguments, 0 given",
    'read res cell': "line 1, instruction 'read' require 2 arguments, 1 given",
    'read res cell index 4': "line 1, instruction 'read' require 2 arguments, 3 given",
}
instrSensor = {
    'sensor': "line 1, instruction 'sensor' require a variable to store result at position 2, no variable given",
    'sensor 4': "line 1, instruction 'sensor' require a variable to store result at position 2, '4' not valide",
    'sensor "res"': """line 1, instruction \'sensor\' require a variable to store result at position 2, \'"res"\' not valide""",
    'sensor res': "line 1, instruction 'sensor' require 2 arguments, 0 given",
    'sensor res buildingX': "line 1, instruction 'sensor' require 2 arguments, 1 given",
    'sensor res buildingX @x tooMuch': "line 1, instruction 'sensor' require 2 arguments, 3 given",
}
instrGetlink = {
    'getlink': "line 1, instruction 'getlink' require a variable to store result at position 2, no variable given",
    'getlink 4': "line 1, instruction 'getlink' require a variable to store result at position 2, '4' not valide",
    'getlink "res"': """line 1, instruction \'getlink\' require a variable to store result at position 2, \'"res"\' not valide""",
    'getlink res': "line 1, instruction 'getlink' require 1 arguments, 0 given",
    'getlink res linkid yo': "line 1, instruction 'getlink' require 1 arguments, 2 given",
}
instrRadar = {
    'radar': "line 1, instruction 'radar' not enought arguments, the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss']",
    'radar x': "line 1, instruction 'radar' the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss'], 'x' given instead",
    'radar any 4': "line 1, instruction 'radar' the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss'], '4' given instead",
    'radar any ally': "line 1, instruction 'radar' not enought arguments, the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss']",
    'radar any boss 2': "line 1, instruction 'radar' the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss'], '2' given instead",
    'radar any boss ally 2': "line 1, instruction 'radar' the 4th argument of this instruction must be one of: ['distance', 'health', 'shield', 'armor', 'maxHealth'], '2' given instead",
    'radar any boss ally': "line 1, instruction 'radar' the 4th argument of this instruction must be one of: ['distance', 'health', 'shield', 'armor', 'maxHealth'], only 3 arguments provided",
    'radar any boss ally distance': "line 1, instruction 'radar' not enought arguments",
    'radar any boss ally distance shield': "line 1, instruction 'radar', 'shield' is a reserved keyword, it could not be used as variable",
    'radar any boss ally distance yo': "line 1, instruction 'radar' not enought arguments",
    'radar any boss ally distance yo set': "line 1, instruction 'radar', 'set' is a reserved keyword, it could not be used as variable",
    'radar any boss ally distance yo 4': "line 1, instruction 'radar' require a variable to store result at position 8, no variable given",
    'radar any boss ally distance yo 4 6': "line 1, instruction 'radar' require a variable to store result at position 8, '6' not valide",
    'radar any boss ally distance yo 4 result 2': "line 1, instruction 'radar' too many arguments",
}
instrUradar = {
    'uradar': "line 1, instruction 'uradar' not enought arguments, the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss']",
    'uradar x': "line 1, instruction 'uradar' the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss'], 'x' given instead",
    'uradar any 4': "line 1, instruction 'uradar' the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss'], '4' given instead",
    'uradar any ally': "line 1, instruction 'uradar' not enought arguments, the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss']",
    'uradar any boss 2': "line 1, instruction 'uradar' the first three arguments of this instruction must be one of: ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss'], '2' given instead",
    'uradar any boss ally 2': "line 1, instruction 'uradar' the 4th argument of this instruction must be one of: ['distance', 'health', 'shield', 'armor', 'maxHealth'], '2' given instead",
    'uradar any boss ally': "line 1, instruction 'uradar' the 4th argument of this instruction must be one of: ['distance', 'health', 'shield', 'armor', 'maxHealth'], only 3 arguments provided",
    'uradar any boss ally distance': "line 1, instruction 'uradar' not enought arguments",
    'uradar any boss ally distance shield': "line 1, instruction 'uradar', 'shield' is a reserved keyword, it could not be used as variable",
    'uradar any boss ally distance yo': "line 1, instruction 'uradar' not enought arguments",
    'uradar any boss ally distance yo set': "line 1, instruction 'uradar', 'set' is a reserved keyword, it could not be used as variable",
    'uradar any boss ally distance yo 4': "line 1, instruction 'uradar' require a variable to store result at position 8, no variable given",
    'uradar any boss ally distance yo 4 6': "line 1, instruction 'uradar' require a variable to store result at position 8, '6' not valide",
    'uradar any boss ally distance yo 4 result 2': "line 1, instruction 'uradar' too many arguments",
}
instrDraw = {
    'draw': "line 1, instruction 'draw', require keyword, must be on of: ['stroke', 'clear', 'color', 'line', 'rect', 'lineRect', 'image', 'poly', 'linePoly', 'triangle']",
    'draw line': "line 1, instruction 'draw' require 6 arguments, 0 given",
    'draw yo': "line 1, instruction 'draw', 'yo' is not a valide keyword, must be on of:",
    'draw set': "line 1, instruction 'draw', 'set' is not a valide keyword, must be on of",
    'draw add': "line 1, instruction 'draw', 'add' is not a valide keyword, must be on of",
    'draw triangle x y': "line 1, instruction 'draw' require 6 arguments, 2 given",
    'draw triangle 1 2 3 4 5 6 7': "line 1, instruction 'draw' require 6 arguments, 7 given",
}
instrControl = {
    'control': "line 1, instruction 'control', require keyword, must be on of: ['enabled', 'configure', 'shootp', 'shoot', 'color']",
    'control 4': "line 1, instruction 'control', '4' is not a valide keyword, must be on of:",
    'control 4 5 6 7 8': "line 1, instruction 'control', '4' is not a valide keyword, must be on of:",
    'control shootp block1 0 0 0 0 6': "line 1, instruction 'control' require 5 arguments, 6 given",
}
instrUcontrol = {
    'ucontrol': "line 1, instruction 'ucontrol', require keyword, must be on of: ['idle', 'stop', 'move', 'approach', 'pathfind', 'target', 'targetp', 'itemDrop', 'itemTake', 'payDrop', 'payTake', 'flag', 'mine', 'build', 'getBlock', 'within', 'boost']",
    'ucontrol 4': "line 1, instruction 'ucontrol', '4' is not a valide keyword, must be on of:",
    'ucontrol move 0 0 0 0 0 6': "line 1, instruction 'ucontrol' require 5 arguments, 6 given",
}
instUlocate = {
    'ulocate': "line 1, instruction 'ulocate', require keyword, must be on of: ['ore', 'damaged', 'spawn', 'building']",
    'ulocate a': "line 1, instruction 'ulocate', 'a' is not a valide keyword, must be on of:",
    'ulocate 4': "line 1, instruction 'ulocate', '4' is not a valide keyword, must be on of:",
    'ulocate building': "line 1, instruction 'ulocate', require keyword, must be on of: ['core', 'storage', 'generator', 'factory', 'repair', 'rally', 'battery', 'resupply', 'reactor', 'turret']",
    'ulocate building x': "line 1, instruction 'ulocate', 'x' is not a valide keyword, must be on of: ['core', 'storage', 'generator', 'factory', 'repair', 'rally', 'battery', 'resupply', 'reactor', 'turret']",
    'ulocate building x y z': "line 1, instruction 'ulocate', 'x' is not a valide keyword, must be on of:",
    'ulocate building rally x': "line 1, instruction 'ulocate' require 6 arguments, 1 given",
    'ulocate building rally x y z': "line 1, instruction 'ulocate' require 6 arguments, 3 given",
    'ulocate building rally x y z 1 2': "line 1, instruction 'ulocate' require 6 arguments, 5 given",
    'ulocate spawn building x': "line 1, instruction 'ulocate', 'building' is a reserved keyword, it could not be used as variable",
    'ulocate ore null true @copper outx outy found': "line 1, instruction 'ulocate' require 7 arguments, 6 given",
    'ulocate spawn a x': "line 1, instruction 'ulocate' require 7 arguments, 2 given",
    'ulocate spawn null true null outx outy found buildingResult tooMuch': "line 1, instruction 'ulocate' require 7 arguments, 8 given",
    'ulocate spawn 0 outx outy found': "line 1, instruction 'ulocate' require 7 arguments, 4 given",
}


errorList = [
    instrNotValide, subInstrNotValide, instrOp, instrSimple, instrSet, intrOneArg, instrWrite, instrRead,
    instrSensor, instrGetlink, instrRadar, instrUradar, instrDraw,
    instrControl, instrUcontrol, instUlocate
]


def identical(instr):
    return runYacc(instr) == instr + '\n'


def test_asm():
    for dico in errorList:
        for k, v in dico.items():
            assertCompilationException(k, v)

    assert identical('op add yo 1 2')
    assert identical('op mul yo 1 2')
    assert identical('op abs res arg1')
    assert identical('end')
    assert identical('set yo 4')
    assert identical('ubind @flare')
    assert identical('read res cell 1')
    assert identical('sensor result block1 @copper')
    assert identical('getlink result linkId')
    assert identical('radar enemy any flying distance turret1 sortOrder result')
    assert identical('uradar enemy any flying distance null sortOrder result')
    assert identical('uradar enemy any flying distance null sortOrder result')
    assert identical('draw triangle 1 2 3 4 5 6')
    assert identical('control shootp block1 0 0 0 0')
    assert identical('control shootp 0 0 0 0 0')
    assert identical('ulocate building reactor true null outx outy found buildingResult')
    assert identical('ulocate spawn null true null outx outy found buildingResult')
    assert identical('ulocate ore null true @copper outx outy found buildingResult')
