from __future__ import annotations

from byte_ninja.enums import ByteOrder, StreamMode

from abc import ABC, abstractmethod
from io import (
    BytesIO,
    IOBase,
    RawIOBase,
    SEEK_SET,
    SEEK_CUR,
    SEEK_END,
)


__all__ = [
    'BaseStream',
    'BaseBufferedStream',
    'BaseStreamWrapper',

    'SEEK_CUR',
    'SEEK_SET',
    'SEEK_END',
]


class BaseStream(RawIOBase, ABC):
    """
    The base class for any stream defined in byte ninja.
    """

    @property
    @abstractmethod
    def stream_mode(self) -> StreamMode:
        ...

    @property
    @abstractmethod
    def eof(self) -> bool:
        ...

    @property
    @abstractmethod
    def byteorder(self) -> ByteOrder | None:
        ...

    @byteorder.setter
    @abstractmethod
    def byteorder(self, value: ByteOrder):
        ...

    @abstractmethod
    def require(self, size: int) -> bytes:
        """
        Read a specific amount of bytes from the stream.
        :raises EOFError:
        """
        ...

    @abstractmethod
    def read_int(self, size: int, byteorder: ByteOrder = None, signed: bool = False) -> int:
        """ Read an integer from the stream. """
        ...

    @abstractmethod
    def write_int(self, value: int, size: int, byteorder: ByteOrder = None, signed: bool = False):
        """ Write an integer to the stream. """

    @abstractmethod
    def read_uint(self, size: int, byteorder: ByteOrder = None) -> int:
        """ Read an unsigned integer from the stream. """

    @abstractmethod
    def read_sint(self, size: int, byteorder: ByteOrder = None) -> int:
        """ Read a signed integer from the stream. """

    @abstractmethod
    def write_uint(self, value: int, size: int, byteorder: ByteOrder = None):
        """ Write an unsigned integer to the stream. """

    @abstractmethod
    def write_sint(self, value: int,  size: int, byteorder: ByteOrder = None):
        """ Write a signed integer to the stream. """

    @abstractmethod
    def read_raw_cstring(self, delimiter: bytes = b'\x00', fail_eof: bool = False) -> bytes:
        """
        Read a sequence of bytes,
        which are delimited by a delimiter, from the stream.
        """
    @abstractmethod
    def write_raw_cstring(self, string: bytes,
                          delimiter: bytes = b'\x00'):
        """
        Write a sequence of bytes,
        which are delimited by a delimiter, to the stream.
        """

    @abstractmethod
    def read_cstring(self, delimiter: bytes = b'\x00',
                     encoding: str = 'utf8',
                     fail_eof: bool = False) -> str:
        """
        Read a string, which is delimited by a delimiter, from the stream.
        """

    @abstractmethod
    def write_cstring(self, string: str,
                      encoding: str = 'utf8',
                      delimiter: bytes = b'\x00'):
        """
        Write a string, which is delimited by a delimiter, to the stream.
        """


class BaseBufferedStream(BytesIO, BaseStream, ABC):
    """ A stream wrapped around a memory buffer for fast access. """


class BaseStreamWrapper(BaseStream, ABC):
    """ A stream wrapper, that can wrap any stream. """

    @property
    @abstractmethod
    def inner(self) -> IOBase:
        ...

