from byte_ninja.enums import ByteOrder
from byte_ninja.backends.base.code_object import BaseCodeObject

from abc import ABC, abstractmethod


class DataType(ABC):
    @abstractmethod
    def read(self, vm) -> object:
        ...

    @abstractmethod
    def write(self, vm, value: object):
        ...


class PrimitiveType(DataType, ABC):
    ...


class ComplexType(DataType, ABC):
    __slots__ = 'read_code', 'write_code'
    __read_code__: BaseCodeObject
    __write_code__: BaseCodeObject


    def read(self, vm) -> dict:
        ...

    def write(self, vm, value: dict):
        ...
