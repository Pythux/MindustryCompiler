
from .ValVarKey import Variable, KeyWord


class AsmInst:
    def __init__(self, instruction: KeyWord, liValVar=None) -> None:
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

    def applyToVariables(self, fun):
        for el in self.liValVar:
            if isinstance(el, Variable):
                fun(el)

    def toStr(self):
        if not len(self.liValVar):
            return "{}".format(self.instruction)

        return "{instr} {liValVar}".format(
            instr=self.instruction, liValVar=' '.join(map(str, self.liValVar)))

    def copy(self):
        return self.__class__(self.instruction, list(map(lambda el: el.copy(), self.liValVar)))

    def __repr__(self) -> str:
        return '<AsmInstr {}>'.format(self.toStr())
