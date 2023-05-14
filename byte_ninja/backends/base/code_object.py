from abc import ABC, abstractmethod

from byte_ninja.stream import BaseStream


class BaseCodeObject(BaseStream, ABC):
    @abstractmethod
    def read_name(self) -> str:
        """
        Reads a name number from the stream
        and looks up the name in the name table.
        """

    @classmethod
    @abstractmethod
    def from_bytes(cls, data: bytes):
        """ Create a new code object from the given binary representation. """

    @abstractmethod
    def to_bytes(self) -> bytes:
        """ Parse the code object into a binary representation. """
