from __future__ import annotations

from byte_ninja.sizes import BYTE
from byte_ninja.enums import ByteOrder, StreamMode

from io import BytesIO, IOBase, RawIOBase, SEEK_END


__all__ = [
    'Stream',
    'BufferedStream',
    'StreamWrapper',
]


class Stream(RawIOBase):
    def __init__(self, byteorder: ByteOrder = None):
        self._byteorder = byteorder
        self._mode: StreamMode | None = None
        self._set_mode()

    def _set_mode(self):
        self._mode = 0
        if self.readable():
            self._mode |= StreamMode.READ

        if self.writable():
            self._mode |= StreamMode.WRITE

        if self.seekable():
            self._mode |= StreamMode.SEEK

    @property
    def stream_mode(self) -> StreamMode:
        return self._mode

    @property
    def eof(self) -> bool:
        if not self._mode.can_seek():
            raise NotImplementedError

        pos = self.tell()
        end = self.seek(0, SEEK_END)
        self.seek(pos)
        return end == pos

    @property
    def byteorder(self) -> ByteOrder | None:
        return self._byteorder

    @byteorder.setter
    def byteorder(self, value: ByteOrder):
        self._byteorder = value

    def require(self, size: int) -> bytes:
        """
        Read an amount of bytes from the stream,
        but when eof is reached a EOFError is raised.
        """

        data = self.read(size)

        if len(data) != size:
            raise EOFError

        return data

    def read_int(self, size: int, byteorder: ByteOrder = None, signed: bool = False) -> int:
        """ Read an integer from the stream. """

        byteorder = byteorder or self.byteorder
        assert byteorder is not None, 'no byteorder provided'

        return int.from_bytes(
            self.require(size),
            byteorder.as_literal(),
            signed=signed,
        )

    def write_int(self, value: int, size: int, byteorder: ByteOrder = None, signed: bool = False):
        """ Write an integer to the stream. """
        assert isinstance(value, int)

        byteorder = byteorder or self.byteorder
        assert byteorder is not None, 'no byteorder provided'

        self.write(value.to_bytes(
            size,
            byteorder.as_literal(),
            signed=signed,
        ))

    def read_uint(self, size: int, byteorder: ByteOrder = None) -> int:
        """ Read an unsigned integer from the stream. """
        return self.read_int(size, byteorder, False)

    def read_sint(self, size: int, byteorder: ByteOrder = None) -> int:
        """ Read a signed integer from the stream. """
        return self.read_int(size, byteorder, True)

    def write_uint(self, value: int, size: int, byteorder: ByteOrder = None):
        """ Write an unsigned integer to the stream. """
        return self.write_int(value, size, byteorder, False)

    def write_sint(self, value: int,  size: int, byteorder: ByteOrder = None):
        """ Write a signed integer to the stream. """
        return self.write_int(value, size, byteorder, True)

    def read_raw_cstring(self, delimiter: bytes = b'\x00', fail_eof: bool = False) -> bytes:
        """
        Read a sequence of bytes,
        which are delimited by a delimiter, from the stream.
        """

        assert len(delimiter) == 1, 'only delimiters of length 1 are allowed'

        result = list()

        while ...:
            if not fail_eof:
                char = self.read(BYTE)
            else:
                char = self.require(BYTE)

            if char == delimiter:
                break

            result.append(char[0])

        return bytes(result)


    def write_raw_cstring(self, string: bytes,
                          delimiter: bytes = b'\x00'):
        """
        Write a sequence of bytes,
        which are delimited by a delimiter, to the stream.
        """

        assert len(delimiter) == 1, 'only delimiters of length 1 are allowed'
        self.write(string + delimiter)


    def read_cstring(self, delimiter: bytes = b'\x00',
                     encoding: str = 'utf8',
                     fail_eof: bool = False) -> str:
        """
        Read a string, which is delimited by a delimiter, from the stream.
        """

        return self.read_raw_cstring(
            delimiter,
            fail_eof,
        ).decode(encoding)

    def write_cstring(self, string: str,
                      encoding: str = 'utf8',
                      delimiter: bytes = b'\x00'):
        """
        Write a string, which is delimited by a delimiter, to the stream.
        """
        self.write_raw_cstring(
            string.encode(encoding),
            delimiter,
        )


class BufferedStream(Stream, BytesIO):
    def __init__(self, data: bytes = b'', byteorder: ByteOrder = None):
        BytesIO.__init__(self, data)
        Stream.__init__(self, byteorder)


class StreamWrapper(Stream):
    def __init__(self, stream: IOBase, byteorder: ByteOrder = None):
        super().__init__(byteorder)
        self._stream = stream

    @property
    def inner(self) -> IOBase:
        return self._stream

