from __future__ import annotations

from builder import FieldNode



def field(value: object | FieldNode = None):
    """
    Usage:

    @builder.struct
    class Thing:
        # for defining fields
        x: int = field(2)
        # you can omit the field and just write this:
        # x: int = 2
        # but if you do this you cannot use branching anymore.
        # to use branching you have to assign all fields with field()

        # usage of advanced features like
        # branching is allowed now

        # field() can also be used to check for values,
        # like this:
        @IF(field(x) == 2)
        class BODY:  # note the class must not be named 'BODY'
                     # it is also fine if branch classes overwrite each other

            y: int = field(42)

        @IF(field(x) == 42)
        class BODY:  # overwrite is fine
            z: int = field(44)


    """
    ...


def variable(value: object = None, ):
    ...


def checksum():
    ...


def const():
    ...


def assign(target: FieldNode, value: object):
    ...


def op(operation: ..., target: ...):
    ...


def read(data_type: ..., target: ...):
    ...


def write(data_type: ..., target: ...):
    ...


def seek(offset: int, mode: ... = ...):
    ...


def tell(target: ... = ...):
    ...



def IF(condition: ... = ...):  # noqa
    ...

def ELIF(condition: ... = ...):  # noqa
    ...

def ELSE():  # noqa
    ...


def WHILE(condition: ... = ...):  # noqa
    ...


def FOR(target: ...):  # noqa
    ...


def ITER():  # noqa
    ...


def BREAK():  # noqa
    ...


def CONTINUE():  # noqa
    ...




