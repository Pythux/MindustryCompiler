
import copy


class Value:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, o: object) -> bool:
        return o.variable == self.variable

    def __repr__(self) -> str:
        return '<Value {}>'.format(self.value)


class Variable:
    def __init__(self, variable: str) -> None:
        if not isinstance(variable, str):
            raise Exception("not a string !")
        self.variable = variable

    def __str__(self) -> str:
        return self.variable

    def __repr__(self) -> str:
        return '<Variable {}>'.format(self.variable)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return o == self.variable
        return o.variable == self.variable

    def __hash__(self) -> int:
        return hash(self.variable)


class AsmInst:
    def __init__(self, instruction: str, liValVar) -> None:
        self.instruction = instruction
        self.liValVar = liValVar

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
            return self.instruction

        return "{instr} {liValVar}".format(
            instr=self.instruction, liValVar=' '.join(map(str, self.liValVar)))
