from abc import ABC, abstractmethod
from typing import SupportsBytes


class DataType(ABC):
    __has_bytecode__: bool


    @classmethod
    @abstractmethod
    def from_bytes(cls, data: SupportsBytes, *args, **kwargs) -> object:
        ...

    @abstractmethod
    def to_bytes(self, *args, **kwargs) -> bytes:
        ...


class Structure(DataType):
    __has_bytecode__: bool = True
    __compiled__: bool
    __read_code__: ...


    @classmethod
    def from_bytes(cls, data: SupportsBytes, *args, **kwargs) -> object:
        pass

    def to_bytes(self, *args, **kwargs) -> bytes:
        pass

