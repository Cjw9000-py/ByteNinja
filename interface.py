from byte_ninja.branch import *
from byte_ninja.structure import *

def variable(value=None):
    return value


@struct(branch=True)
class X:
    x: int = field()

    @IF(FIELD(x) == 2)
    class N:
        y: int = field()

    d: int = field()

    @IF(FIELD(x) == 2)
    class N:
        e: int = field()

class SB:
    def struct(self, fn):
        ...

    def program(self, fn):
        ...


# structs
# enums
# unions
builder = SB()

@builder.struct
class Thing:
    x: int
    y: int


@SB().program
class StreamProcessor:
    x: int = field()
    variable = variable()

    @IF(variable(x) == 2)
    class BODY:
        ...



builder.compile()
