

from compiler import CompilationException
from .ValVarKey import Value, Variable, KeyWord


class AsmInst:
    def __init__(self, instruction: KeyWord, liValVar=None) -> None:
        # validateAsmInstr(instruction, liValVar)
        self.instruction = instruction
        self.liValVar = liValVar if liValVar is not None else []

    # return list of ID
    def getVars(self):
        return [el.variable for el in self.liValVar if isinstance(el, Variable)]

    # replace an ID by another (ID or info)
    def replace(self, toReplace, toReplaceBy):
        for index, el in enumerate(self.liValVar):
            if isinstance(el, Variable) and el == toReplace:
                self.liValVar[index] = toReplaceBy

    def toStr(self):
        if not len(self.liValVar):
            return "{}".format(self.instruction)

        return "{instr} {liValVar}".format(
            instr=self.instruction, liValVar=' '.join(map(str, self.liValVar)))

    def copy(self):
        return self.__class__(self.instruction, list(map(lambda el: el.copy(), self.liValVar)))

    def __repr__(self) -> str:
        return '<AsmInstr {}>'.format(self.toStr())


def draw(liValVar):
    pass


def radar(liValVar):
    if len(liValVar) < 7:
        raise CompilationException("instruction 'radar' must have 7 arguments, {} given".format(len(liValVar)))
    valideRadarTarget = ['any', 'enemy', 'ally', 'player', 'attacker', 'flying', 'ground', 'boss']
    for i in range(3):
        if liValVar[i] not in valideRadarTarget:
            raise CompilationException("at instruction 'radar', the {} argument is not on of: {}"
                                       .format(i+1, valideRadarTarget))
    valideSort = ['distance', 'health', 'shield', 'armor', 'maxHealth']
    if liValVar[3] not in valideSort:
        raise CompilationException("at instruction 'radar', the 4 arguments is not on of: {}".format(valideSort))


def uradar(liValVar):
    lenArgs = len(liValVar)
    if lenArgs == 7:
        radar(liValVar)
    elif lenArgs == 6:
        liValVar = liValVar[:4] + [Value('null')] + liValVar[4:]
        radar(liValVar)
    else:
        raise CompilationException("uradar recev {} arguments, 6 required".format(lenArgs))


def ucontrol(liValVar):
    op, *args = liValVar


instr = {
    'read': 3,
    'write': 3,
    'print': 1,
    'printflush': 1,
    'draw': draw,
    'drawflush': 1,
    'getlink': 2,
    'sensor': 3,
    'set': 2,
    # 'op': operation,
    'ubind': 1,
    'radar': radar,
    'uradar': uradar,
    'ucontrol': ucontrol,
    'end': 0,
}


def validateAsmInstr(instruction, liValVar):
    if instruction not in instr:
        raise CompilationException("instruction '{}' is not a valide mindustry instruction".format(instruction))
    i = instr[instruction]
    if isinstance(i, int):
        if len(liValVar) != i:
            raise CompilationException("not enought arguments for instruction '{}', {} given, required {}"
                                       .format(instruction, len(liValVar), i))
    else:
        i(liValVar)


'''
draw stroke 0 0 0 255 0 0
draw clear 0 0 0 0 0 0
draw color 0 0 0 255 0 0
draw line 0 0 0 255 0 0
draw rect 0 0 0 255 0 0
draw lineRect 0 0 0 255 0 0
draw image 0 0 @copper 32 0 0
draw poly 0 0 0 255 0 0
draw linePoly 0 0 0 255 0 0
draw triangle 0 0 0 255 0 0

control enabled block1 0 0 0 0
control configure block1 0 0 0 0
control shootp block1 0 0 0 0
control shoot block1 0 0 0 0
control color block1 0 0 0 0

ucontrol move 0 0 0 0 0

ulocate ore core true @copper outx outy found building
ulocate spawn core true @copper outx outy found building
ulocate damaged core true @copper outx outy found building
ulocate building core true @copper outx outy found building
ulocate building reactor true @copper outx outy found building

'''
