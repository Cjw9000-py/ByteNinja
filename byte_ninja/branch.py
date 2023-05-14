from __future__ import annotations
from enum import IntEnum

from .condition import (
    Condition,
    Operand,
    NativeOperand,
    FieldOperand,
)


class TreeContext:
    enabled: bool = False
    stack: list[list] = list()

    @classmethod
    def start(cls):
        """ Start a new struct. """
        cls.stack.append(list())
        cls.enabled = True

    @classmethod
    def finish(cls) -> list:
        """ Finish up the current struct. """
        assert len(cls.stack) == 1
        cls.enabled = False
        return cls.stack.pop()

    @classmethod
    def new_level(cls, level: list):
        """ Create a new stack level. """
        cls.stack.append(level)

    @classmethod
    def finish_level(cls):
        """ Move the top stack level into the lower level. """
        assert len(cls.stack) >= 2

        top = cls.stack.pop()
        cls.stack[-1].append(top)


class Branch(list):
    class BranchType(IntEnum):
        BRANCH_IF = 0
        BRANCH_ELIF = 1
        BRANCH_ELSE = 2

    def __init__(self, typ: BranchType, condition: Condition = None, cls: type = None):
        super().__init__()
        self.type = typ
        self.condition = condition
        self.cls = cls

    def copy(self) -> Branch:
        obj = self.__class__(self.type, self.condition)
        obj.extend(self)
        return obj


def _check_branching():
    if not TreeContext.enabled:
        raise RuntimeError('branching can only be used with '
                           'the branching option enabled.')


def FIELD(field) -> Condition:  # noqa
    return Condition(FieldOperand(field))


def _branch(condition, typ):
    _check_branching()
    branch = Branch(
        typ,
        condition,
    )

    TreeContext.new_level(branch)

    def inner(cls: type):
        TreeContext.finish_level()
        branch.cls = cls
        return cls

    return inner


def IF(condition):  # noqa
    return _branch(condition, Branch.BranchType.BRANCH_IF)

def ELIF(condition):  # noqa
    return _branch(condition, Branch.BranchType.BRANCH_ELIF)

def ELSE():  # noqa
    return _branch(None, Branch.BranchType.BRANCH_ELSE)