from io import BytesIO, RawIOBase

from .sizes import BYTE
from .codes import Byteorder, BYTEORDER_TO_LITERAL


class Stream(RawIOBase):
    byteorder: Byteorder | None

    def __init__(self):
        self.byteorder = None

    def require(self, size: int) -> bytes:
        """
        Read an amount of bytes from the stream,
        but when eof is reached a EOFError is raised.
        """

        data = self.read(size)

        if len(data) != size:
            raise EOFError

        return data

    def read_int(self, size: int, byteorder: Byteorder = None, signed: bool = False) -> int:
        """ Read an integer from the stream. """

        byteorder = byteorder or self.byteorder
        assert byteorder is not None, 'no byteorder provided'
        literal = BYTEORDER_TO_LITERAL[byteorder]

        return int.from_bytes(
            self.require(size),
            literal,
            signed=signed,
        )

    def write_int(self, value: int, size: int, byteorder: Byteorder = None, signed: bool = False):
        """ Write an integer to the stream. """
        assert isinstance(value, int)

        byteorder = byteorder or self.byteorder
        assert byteorder is not None, 'no byteorder provided'
        literal = BYTEORDER_TO_LITERAL[byteorder]

        self.write(value.to_bytes(
            size,
            literal,
            signed=signed,
        ))

    def read_uint(self, size: int, byteorder: Byteorder = None) -> int:
        """ Read an unsigned integer from the stream. """
        return self.read_int(size, byteorder, False)

    def read_sint(self, size: int, byteorder: Byteorder = None) -> int:
        """ Read a signed integer from the stream. """
        return self.read_int(size, byteorder, True)

    def write_uint(self, value: int, size: int, byteorder: Byteorder = None):
        """ Write an unsigned integer to the stream. """
        return self.write_int(value, size, byteorder, False)

    def write_sint(self, value: int,  size: int, byteorder: Byteorder = None):
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


class BufferedStream(BytesIO, Stream):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.byteorder = None
