

class Imports:
    def __init__(self) -> None:
        self.imported = {None: {}}  # None is main file
        self.toImports = []
        self.currentFile = None

    def clear(self):
        self.imported = {None: {}}  # None is main file
        self.toImports = []
        self.currentFile = None

    # simple absolute import from lib/, one lvl
    def toImport(self, filesToImport):
        for fileLib in filesToImport:
            if fileLib not in self.imported and fileLib not in self.toImports:
                self.toImports.append(fileLib)

    # generator that give the next module that will be parsed
    def nextToImport(self):
        while len(self.toImports):
            module = self.toImports.pop()
            assert module not in self.imported
            self.currentFile = module  # will pe processed
            self.imported[module] = {}  # functions will be stored here
            yield module

    def addFunToModule(self, funDef):
        if funDef.name in self.imported[self.currentFile]:
            raise Exception("function/macro {} already defined".format(funDef.name))
        self.imported[self.currentFile][funDef.name] = funDef

    def addMacroToModule(self, macroDef):
        if macroDef.name in self.imported[self.currentFile]:
            raise Exception("function/macro {} already defined".format(macroDef.name))
        self.imported[self.currentFile][macroDef.name] = macroDef

    # called at the verry end, once everything is imported
    def getModule(self, fileLib):
        if fileLib not in self.imported:
            raise Exception("module {} is used but not imported".format(fileLib))
        return self.imported[fileLib]


imports = Imports()
