

class Imports:
    def __init__(self) -> None:
        self.imported = {None: {}}  # None is main file
        self.toImports = []
        self.currentFile = None
        self.linesFunDef = []

    def clear(self):
        self.imported = {None: {}}  # None is main file
        self.toImports = []
        self.currentFile = None
        self.linesFunDef = []

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
            raise Exception("function {} already defined".format(funDef.name))
        self.imported[self.currentFile][funDef.name] = funDef

    # called at the verry end, once everything is imported
    def getModule(self, fileLib):
        if fileLib not in self.imported:
            raise Exception("module {} is used but not imported".format(fileLib))
        return self.imported[fileLib]

    # once parsing over, all funDef are registered in module
    def getFunCalled(self, moduleName, name, lineCall):
        module = self.getModule(moduleName)
        if name not in module:
            raise Exception("function '{}' does not exist, module {}, at line {}"
                            .format(name, moduleName, lineCall))
        fun = module[name]
        if not fun.defined:
            self.linesFunDef += fun.generateDefinition(moduleName)
        return fun

    # return lines of function definition
    def getFunctionsDefinition(self):
        lines = self.linesFunDef
        self.linesFunDef = []
        return lines


imports = Imports()
