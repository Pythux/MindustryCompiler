

class Ref:
    def __init__(self, ref: str) -> None:
        self.id = ref

    def __str__(self) -> str:
        return "<Ref: {}>".format(self.id)

    def __repr__(self) -> str:
        return self.__str__()


class Jump:
    def __init__(self, line, ref: Ref, condition=None) -> None:
        self.line = line
        self.ref = ref
        self.asmCondition = condition if condition is not None else 'always true true'

    def refToLine(self, refDict):
        if self.ref.id not in refDict:
            print("for jump at line: {}".format(self.line))
            print("ref {} not exist, existing ref: {}".format(self.ref.id, self.context.refDict))
            raise SystemExit()
        self.refLine = refDict[self.ref.id]

    def toStr(self):
        return 'jump {refLine} {condition}'.format(
            refLine=self.refLine, condition=self.asmCondition)

    def __str__(self):
        return '<Jump: {} {}>'.format(self.ref, self.asmCondition)

    def __repr__(self) -> str:
        return self.__str__()

    def replace(self, toReplace, toReplaceBy):
        for index, el in enumerate(self.ab):
            if el == toReplace:
                self.ab[index] = toReplaceBy


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
