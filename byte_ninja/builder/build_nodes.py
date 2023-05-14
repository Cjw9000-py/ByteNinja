from enum import IntEnum
from abc import ABC, abstractmethod


class NodeType(IntEnum):
    data_type = 0
    field = 1
    variable = 2
    branch = 3
    loop = 4

    ...



class Node(ABC):
    ...


########### DATA TYPES

class DataTypeNode(Node, ABC):
    __slots__ = 'name'

    def __init__(self, name: str):
        self.name = name


class StructureNode(DataTypeNode):
    __slots__ = 'name', 'body_cls'

    def __init__(self, name: str, body_cls: type):
        super().__init__(name)
        self.body_cls = body_cls


class EnumNode(Node):
    ...


class UnionNode(Node):
    ...


########### FIELDS

class FieldNode(Node):
    ...


class ConstantNode(Node):
    ...


class ChecksumNode:
    ...


########### VARIABLE

class VariableNode(Node):
    ...


########## BRANCH & LOOP

class BranchNode(Node):
    ...


######### OPERATIONS

class AssignNode(Node):
    ...



# not used atm

class ReadNode:
    ...


class WriteNode:
    ...


class OperationNode:
    ...


class BitFieldNode:
    ...
