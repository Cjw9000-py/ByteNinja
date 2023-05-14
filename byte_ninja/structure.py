from __future__ import annotations

from warnings import warn
from typing import Generator
from threading import current_thread, main_thread

from byte_ninja.backends.pythonic.code_object import BaseCodeObject
from .branch import TreeContext, Branch
from .base import ListBased


def _check_thread(caller_name: str):
    """
    Check if we are executed in the main thread,
    and if not raise a warning.
    """

    current = current_thread()
    main = main_thread()

    if current.ident != main.ident:
        warn(
            f'{caller_name} should only be used in the main thread',
            UserWarning,
        )


class Field:
    __slots__ = 'dependencies', 'name', 'type', 'default'

    def __init__(self, default: object = None):
        self.dependencies = list()
        self.name = None
        self.type = None
        self.default = default

        TreeContext.stack[0].append(self)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'name={self.name}, '
            f'type={self.type}, '
            f'default={self.default}'
            f')'
        )

field = Field

class StructureNodeTree(ListBased):
    ...


class Node:
    ...


class FieldNode(Node):
    __slots__ = 'field'

    def __init__(self, field: Field):  # noqa
        self.field = field


class IfBranch(ListBased, Node):
    ...

class ElifBranch(ListBased, Node):
    ...

class ElseBranch(ListBased, Node):
    ...


class BranchCompoundNode(Node):
    __slots__ = 'if_branch', 'elif_branches', 'else_branch'

    def __init__(self, if_: IfBranch, elif_list: list[ElifBranch], else_: ElseBranch | None):
        self.if_branch = if_
        self.elif_branches = elif_list
        self.else_branch = else_





class Structure:
    __branched__: bool
    __fields__: dict
    __tree__: list
    __read_code__: BaseCodeObject
    __write_code__: BaseCodeObject


class StructureFactory:
    def __init__(self, cls: type):
        self.cls = cls

    def build(self) -> type:
        fields = list()

        for name, typ in self.cls.__annotations__:
            default = None
            if hasattr(self.cls, name):
                default = getattr(self.cls, name)

            f = Field(default)
            f.name = name
            f.type = typ
            fields.append(f)

        return type(self.cls.__name__, (Structure, ), {
            '__branched__': False,
            '__fields__': fields,
            '__tree__': fields.copy(),
        })


# todo cleanup and define proper nodes
# todo build compilation into this class(not directly)
class BranchedStructureFactory:

    class BranchGroup(list):
        def add_branch(self, branch: Branch):
            assert (
                branch.type != Branch.BranchType.BRANCH_IF and
                len(self) >= 1
            )

            if branch.type == Branch.BranchType.BRANCH_ELIF:
                self.append(branch)
            elif branch.type == Branch.BranchType.BRANCH_ELSE:
                if len(self) == 0 or self[-1].type == Branch.BranchType.BRANCH_ELSE:
                    raise SyntaxError('unmatched else')  # todo more info
                self.append(branch)
            else:
                assert False

    def __init__(self, tree: list, cls: type):
        self.tree = tree
        self.cls = cls

    def group_branches(self, branch: Branch | list) -> Branch | list:
        group: list | None = None

        res = branch.copy()
        res.clear()

        for f in branch:
            if isinstance(f, Field):
                res.append(f)

            elif isinstance(f, Branch):
                if f.type == Branch.BranchType.BRANCH_IF:
                    # open a new group
                    group = list()
                    group.append(self.group_branches(f))

                elif f.type == Branch.BranchType.BRANCH_ELIF:
                    # check if we expect an elif
                    if group is None:
                        raise SyntaxError('unmatched elif')  # todo

                    # append the elif to the group
                    group.append(self.group_branches(f))

                elif f.type == Branch.BranchType.BRANCH_ELSE:
                    # check if we expect an else
                    if group is None:
                        raise SyntaxError('unmatched else')  # todo

                    group.append(self.group_branches(f))
                    res.append(group)
                    group = None

                else:
                    assert False

            if group is not None:
                res.append(group)

            return res

    def inject_field_info(self, branch: Branch | list, cls: type, conditions: list):
        fields_stack = list(cls.__annotations__.items())
        fields_stack.reverse()

        for f in branch:
            if isinstance(f, Field):
                f.name, f.type = fields_stack.pop()
                # remove None values (from else branches, which don't have a condition)
                f.dependencies = list(filter(bool, (*conditions, branch.condition)))
            elif isinstance(f, list):
                # branch group
                for b in f:
                    self.inject_field_info(b, b.cls, [*conditions, branch.condition])

    def flatten_fields(self, branch: Branch | list) -> Generator[Field]:
        for f in branch:
            if isinstance(f, Field):
                yield f
            elif isinstance(f, list):
                # branch group
                for b in f:
                    yield from self.flatten_fields(b)
            else:
                assert False

    def build(self) -> type:
        self.tree = self.group_branches(self.tree)
        self.inject_field_info(self.tree, self.cls, list())
        flat = list(self.flatten_fields(self.tree))

        return type(self.cls.__name__, (Structure,), {
            '__branched__': True,
            '__fields__': flat,
            '__tree__': self.tree,
        })


def struct(cls: type = None, *,
           branch: bool = False):

    if branch:
        # push the global level
        TreeContext.start()

    def inner(cls: type):  # noqa
        if branch:
            # pop the global level
            tree = TreeContext.finish()
            return BranchedStructureFactory(tree, cls)
        return StructureFactory(cls)

    if cls is None:
        return inner
    return inner(cls)
