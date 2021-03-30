

class Context:
    # when read a Ref -> get ASM lineNumber
    AsmLineNumber = 0

    # will be used to store: ref -> code line
    refDict = {}

    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.refDict = {}
        self.refCount = 0

    def addRef(self, ref, index):
        if ref.id in self.refDict:
            raise Exception('ref {} already declared'.format(ref.id))
        self.refDict[ref.id] = index

    def genRef(self):
        self.refCount += 1
        return Ref(self.refCount)


context = Context()


class Ref:
    def __init__(self, ref: str) -> None:
        self.id = ref


class Jump:
    def __init__(self, line, ref: Ref, condition=None) -> None:
        self.line = line
        self.ref = ref
        self.asmCondition = condition if condition is not None else 'always true true'

    def toLine(self):
        if self.ref.id not in context.refDict:
            print("for jump at line: {}".format(self.line))
            print("ref {} not exist, existing ref: {}".format(self.ref.id, context.refDict))
            raise SystemExit()
        return 'jump {ref} {condition}'.format(
            ref=context.refDict[self.ref.id], condition=self.asmCondition)
