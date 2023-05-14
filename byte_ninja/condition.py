from __future__ import annotations

from abc import ABC
from typing import Union, SupportsBytes
from .bytecode.codes import OperationCode


NativeType = Union[float, int, str, SupportsBytes]


class Operand(ABC):
    ...


class NativeOperand(Operand):
    __slots__ = 'value'

    def __init__(self, value: Union[float, int, str, SupportsBytes]):
        self.value = value


class FieldOperand(Operand):
    __slots__ = 'value'

    def __init__(self, field):
        self.value = field


class Condition:
    __slots__ = 'type', 'left', 'right'

    def __init__(self, left: Operand):
        self.type = None
        self.left = left
        self.right = None

    def _set_op(self, typ: OperationCode, value: object):
        if isinstance(value, (float, int, str, bytes, bytearray)):
            self.right = NativeOperand(value)
        elif isinstance(value, FieldOperand):
            self.right = value
        else:
            raise TypeError('cannot use this value to create a condition', value)

        self.type = typ
        return self

    def __eq__(self, other: Union[Operand, NativeType]):
        return self._set_op(OperationCode.EQ, other)

    def __ne__(self, other: Union[Operand, NativeType]):
        return self._set_op(OperationCode.NE, other)

    def __lt__(self, other: Union[Operand, NativeType]):
        return self._set_op(OperationCode.LT, other)

    def __gt__(self, other: Union[Operand, NativeType]):
        return self._set_op(OperationCode.GT, other)

    def __le__(self, other: Union[Operand, NativeType]):
        return self._set_op(OperationCode.LE, other)

    def __ge__(self, other: Union[Operand, NativeType]):
        return self._set_op(OperationCode.GE, other)
