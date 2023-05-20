from typing import Literal
from enum import IntEnum, IntFlag


class SeekMode(IntEnum):
    SET   = 0
    REL   = 1
    END   = 2


    # aliases
    @property
    def CURRENT(self):  # noqa
        return self.REL

    @property
    def CUR(self):  # noqa
        return self.REL

    @property
    def START(self):  # noqa
        return self.SET


class StreamMode(IntFlag):
    WRITE = 0b01
    READ  = 0b10
    SEEK  = 0b11

    def can_read(self) -> bool:
        return self & self.READ == self.READ

    def can_write(self) -> bool:
        return self & self.WRITE == self.WRITE

    def can_seek(self) -> bool:
        return self & self.SEEK == self.SEEK


class ByteOrder(IntEnum):
    LITTLE = 0
    BIG    = 1

    def as_literal(self) -> Literal['little', 'big']:
        return 'little' if self == self.LITTLE else 'big'  # noqa

    @classmethod
    def from_literal(cls, value: str):
        if value == 'little':
            return cls.LITTLE
        elif value == 'big':
            return cls.BIG
        else:
            raise ValueError('invalid literal', value)

    # aliases

    @property
    def LITTLE_ENDIAN(self):  # noqa
        return self.LITTLE

    @property
    def BIG_ENDIAN(self):  # noqa
        return self.BIG

    @property
    def little(self):
        return self.LITTLE

    @property
    def big(self):
        return self.BIG
