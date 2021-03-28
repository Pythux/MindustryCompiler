
class Context:
    # when read a Ref -> get ASM lineNumber
    AsmLineNumber = 0

    # will be used to store: ref -> code line
    refDict = {}

    def __init__(self) -> None:
        self.clear()

    def clear(self):
        self.AsmLineNumber = 0
        self.refDict = {}
        self.refCount = 0

    def addRef(self, ref, lineDiff=0):
        if ref in context.refDict:
            raise Exception('ref {} already declared'.format(ref))
        context.refDict[ref] = context.AsmLineNumber + lineDiff

    def genRef(self):
        self.refCount += 1
        return self.refCount


context = Context()
