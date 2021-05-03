
from compiler import CompilationException
from .ValVarKey import Value, Variable


class Ref:
    def __init__(self, ref: str) -> None:
        if not isinstance(ref, str):
            if not isinstance(ref, int):
                raise CompilationException("error")
        self.id = ref

    def __repr__(self) -> str:
        return "<Ref: {}>".format(self.id)

    def copy(self):
        return self.__class__(self.id)

    def replace(self, toReplace, toReplaceBy):
        pass

    def applyToVariables(self, fun):
        pass

    def changeRef(self, newRef):
        self.id = newRef.id

    def applyToRef(self, fun):
        fun(self)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return o.id == self.id
        return False

    def __hash__(self) -> int:
        return hash(self.id)


class Jump:
    def __init__(self, line, ref: Ref, asmCondition=None) -> None:
        self.line = line
        self.ref = ref
        if asmCondition is None:
            self.asmCondition = Comparison(Value('true'), 'always', Value('true'))
        else:
            self.asmCondition = asmCondition

    def refToLine(self, refDict):
        if self.ref.id not in refDict:
            raise CompilationException("for jump at line: {}, ref {} does not exist".format(self.line, self.ref.id))
        self.refLine = refDict[self.ref.id]

    def toStr(self):
        return 'jump {refLine} {condition}'.format(
            refLine=self.refLine, condition=self.asmCondition)

    def __repr__(self):
        return '<Jump: {} {}>'.format(self.ref, self.asmCondition)

    def replace(self, toReplace, toReplaceBy):
        self.asmCondition.replace(toReplace, toReplaceBy)

    def applyToVariables(self, fun):
        self.asmCondition.applyToVariables(fun)

    def changeRef(self, newRef):
        self.ref = newRef

    def applyToRef(self, fun):
        fun(self.ref)

    def copy(self):
        return self.__class__(self.line, self.ref.copy(), self.asmCondition.copy())


class Comparison:
    def __init__(self, a, comp, b) -> None:
        self.ab = [a, b]
        self.comp = comp

    def __str__(self) -> str:
        return '{} {} {}'.format(self.comp, self.ab[0], self.ab[1])

    def replace(self, toReplace, toReplaceBy):
        for index, el in enumerate(self.ab):
            if el == toReplace:
                self.ab[index] = toReplaceBy

    def applyToVariables(self, fun):
        for el in self.ab:
            if isinstance(el, Variable):
                fun(el)

    def copy(self):
        return self.__class__(self.ab[0].copy(), self.comp, self.ab[1].copy())

    def __repr__(self) -> str:
        return "<Comparison: {}>".format(str(self))
