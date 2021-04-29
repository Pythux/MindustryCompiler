
from compiler import CompilationException


class Value:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return o.value == self.value
        return False

    def __repr__(self) -> str:
        return '<Value {}>'.format(self.value)

    def copy(self):
        return self.__class__(self.value)


class Variable:
    def __init__(self, variable: str) -> None:
        if not isinstance(variable, str):
            raise CompilationException("not a string !")
        self.variable = variable

    def __str__(self) -> str:
        return self.variable

    def __repr__(self) -> str:
        return '<Variable {}>'.format(self.variable)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return o.variable == self.variable
        return False

    def __hash__(self) -> int:
        return hash(self.variable)

    def copy(self):
        return self.__class__(self.variable)
