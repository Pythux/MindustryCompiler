
import pkgutil


# import all submodule of grammar in alphabetical order
__all__ = []
import importlib


def importSubModules(package, recursive=False):
    package = importlib.import_module(package)
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        importlib.import_module(full_name)
        __all__.append(name)

        if recursive and is_pkg:
            importSubModules(full_name)


importSubModules(__package__)
