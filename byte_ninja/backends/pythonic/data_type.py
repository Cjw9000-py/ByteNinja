from byte_ninja.enums import ByteOrder
from .code_object import CodeObject

from struct import unpack, pack
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


class IntType(PrimitiveType):
    __slots__ = 'size', 'byteorder', 'signed'

    def __init__(self, size: int, byteorder: ByteOrder, signed: bool):
        self.size = size
        self.byteorder = byteorder
        self.signed = signed

    def read(self, vm) -> int:
        return int.from_bytes(
            bytes=vm.stream.read(self.size),
            byteorder=self.byteorder,  # noqa
            signed=self.signed,
        )

    def write(self, vm, value: int):
        vm.stream.write(
            int.to_bytes(
                self=value,
                length=self.size,
                byteorder=self.byteorder,  # noqa
                signed=self.signed,
            )
        )


class FloatType(PrimitiveType):
    __slots__ = 'size',

    def __init__(self, size: int):
        assert size in (4, 8)
        self.size = size

    @property
    def format(self) -> str:
        return {
            8: 'd',
            4: 'f',
        }[self.size]

    def read(self, vm) -> float:
        return unpack('f', vm.stream.read(self.size))[0]

    def write(self, vm, value: float):
        vm.stream.write(pack(self.format, value))


class ComplexType(DataType, ABC):
    __slots__ = 'read_code', 'write_code'

    def __init__(self, read_code: CodeObject, write_code: CodeObject):
        self.read_code = read_code
        self.write_code = write_code

    @abstractmethod
    def empty(self) -> dict:
        ...

    def read(self, vm) -> dict:
        value = vm.run(self.read_code, self.empty())
        assert isinstance(value, dict)
        return value

    def write(self, vm, value: dict):
        vm.run(
            self.write_code,
            value,
        )
