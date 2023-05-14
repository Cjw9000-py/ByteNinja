"""
Goals:
    exchange data type information
    guard the vm
    data type registry

"""

from __future__ import annotations

from byte_ninja.stream import Stream
from byte_ninja.virtual_machine.data_type import DataType
from .code_object import BaseCodeObject
from abc import ABC, abstractmethod


# a collection of types that must be natively
# implemented by a backend
primitive_types = {
    'bool',
    'int',
    'float32',
    'float64',
}


class Backend(ABC):
    @property
    @abstractmethod
    def database(self) -> dict[str, DataType]:
        ...

    @database.setter
    @abstractmethod
    def database(self, value: dict[str, DataType]):
        ...

    @abstractmethod
    def run(self, code: BaseCodeObject, stream: Stream, fields: dict[str, object]) -> dict:
        """ Run the code in the vm and return fields again. """


