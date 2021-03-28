
class Context:
    # when read a Ref -> get ASM lineNumber
    AsmLineNumber = 0

    # will be used to store: ref -> code line
    refDict = {}

    def clear(self):
        self.AsmLineNumber = 0
        self.refDict = {}


context = Context()
