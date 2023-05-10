from __future__ import annotations

from os import SEEK_CUR, SEEK_END
from io import BytesIO
from struct import pack, unpack
from enum import IntEnum, Enum
from abc import ABC, abstractmethod
from typing import BinaryIO, Literal

BYTE = 1
WORD = 2
DWORD = 4
QWORD = 8

CODE_BYTEORDER: Literal['little', 'big'] = 'little'


c = iter(range(1000))

class Instruction(IntEnum):
    # data structure manipulation
    GET = next(c)  # get a field from input
    PUT = next(c)  # put a field into output

    # array manipulation
    EMPTY = next(c)  # start a new array
    EDIT = next(c)  # load a existing array from a field
    FLIP = next(c)  # flip the array ?
    YIELD = next(c)  # remove the last value from the array and place onto stack
    APPEND = next(c)  # append the value to the array (value taken from stack)
    INDEX = next(c)  # put a value from an array onto stack
    FINISH = next(c)  # move the array onto stack
    FORGET = next(c)  # free the array

    # stack manipulation
    PUSH = next(c)  # push a primitive to the stack
    POP = next(c)  # pop a value from stack


    # stream manipulation
    SEEK = next(c)  # jump to a position in the stream (taken from stack)
    TELL = next(c)  # push the current stream pos to the stack

    # input ops
    READ = next(c)  # read a type from input (can be a complex type)
    RARRAY = next(c)  # read a type x times (x is taken from stack)

    # output ops
    WRITE = next(c)  # write the type to output with the value from stack
    WARRAY = next(c)  # write a type x times (x is taken from stack)

    # branching
    LOOP = next(c)  # loop the next x instructions until break inst
    LOOPX = next(c)  # loop the next x instructions n times
    BREAK = next(c)  # break the current loop
    TEST = next(c)  # test a condition (where left and right operand is taken from stack)
    RET = next(c)  # end the processing of current type
    GOTO = next(c)  # go to the specified offset

    # strings
    ENCODE = next(c)  # encode an array from the stack
    DECODE = next(c)  # decode an array from the stack


INSTRUCTION_LENGTHS = {
    Instruction.GET: BYTE + QWORD,
    Instruction.PUT: BYTE + QWORD,
    Instruction.EMPTY: BYTE + WORD,
    Instruction.EDIT: BYTE + WORD + QWORD,
    Instruction.FLIP: BYTE + WORD,
    Instruction.YIELD: BYTE + WORD,
    Instruction.APPEND: BYTE + WORD,
    Instruction.INDEX: BYTE + QWORD + WORD,
    Instruction.FINISH: BYTE + WORD,
    Instruction.FORGET: BYTE + WORD,
    Instruction.PUSH: BYTE + QWORD,
    Instruction.POP: BYTE,
    Instruction.READ: BYTE + QWORD,
    Instruction.RARRAY: BYTE + QWORD,
    Instruction.WRITE: BYTE + QWORD,
    Instruction.WARRAY: BYTE + QWORD,
    Instruction.LOOP: BYTE + QWORD,
    Instruction.LOOPX: BYTE + QWORD + QWORD,
    Instruction.BREAK: BYTE,
    Instruction.TEST: BYTE + BYTE + QWORD,
    Instruction.RET: BYTE,
    Instruction.GOTO: BYTE + QWORD,
    Instruction.ENCODE: BYTE + QWORD,
    Instruction.DECODE: BYTE + QWORD,
}


class TestOperation(IntEnum):
    EQ = 0
    NE = 1
    LT = 2
    GT = 3
    LE = 4
    GE = 5
    NOT = 6


class SeekMode(IntEnum):
    START = 0
    REL = 1
    END = 2


class OperationMode(IntEnum):
    WRITE = 0
    READ = 1


class Byteorder(Enum):
    LITTLE = 'little'
    BIG = 'big'


class DataStream:
    def __init__(self, stream: BinaryIO, mode: OperationMode):
        self._stream = stream
        self.mode = mode

        if mode == OperationMode.READ:
            assert stream.readable()
        else:
            assert stream.writable()

    def tell(self) -> int:
        return self._stream.tell()

    def seek(self, pos: int, mode: int):
        if mode == SeekMode.START:
            return self._stream.seek(pos)
        elif mode == SeekMode.REL:
            return self._stream.seek(pos, SEEK_CUR)
        elif mode == SeekMode.END:
            return self._stream.seek(pos, SEEK_END)
        else:
            assert False

    def read(self, n: int) -> bytes:
        assert self.mode == OperationMode.READ

        data = self._stream.read(n)

        if len(data) != n:
            raise EOFError
        return data

    def write(self, data: bytes):
        assert self.mode == OperationMode.WRITE

        self._stream.write(data)


class CodeObject:
    def __init__(self, names: dict[int, str], code: bytes):
        self.names = names
        self.code = BytesIO(code)
        self.code_length = len(code)

    @property
    def debug(self):
        pos = self.code.tell()
        val = self.code.getvalue()
        return val[:pos], val[pos:]

    @property
    def eof(self) -> bool:
        return self.code.tell() == self.code_length

    def tell(self) -> int:
        return self.code.tell()

    def seek(self, pos: int):
        self.code.seek(pos)

    def tell_end(self, count: int):
        start = self.tell()
        for _ in range(count):
            op = self.read_int(BYTE)
            length = INSTRUCTION_LENGTHS[op]
            self.code.seek(length, SEEK_CUR)
        end = self.tell()
        self.seek(start)
        return end

    def read(self, size: int) -> bytes:
        data = self.code.read(size)

        if len(data) != size:
            raise EOFError

        return data

    def read_int(self, size: int) -> int:
        return int.from_bytes(
            self.read(size),
            CODE_BYTEORDER,
        )

    def read_name(self) -> str:
        return self.names[self.read_int(QWORD)]

    def reset(self):
        self.code.seek(0)

    @classmethod
    def from_bytes(cls, data: bytes):
        raw = BytesIO(data)
        data = DataStream(raw, OperationMode.READ)

        nt_size = int.from_bytes(data.read(QWORD), CODE_BYTEORDER)
        names = dict()

        for i in range(nt_size):
            # read string
            parts = list()

            while ...:
                char = data.read(BYTE)
                if char[0] == 0:
                    break
                parts.append(char)

            names[i] = b''.join(parts).decode('utf8')

        return cls(names, raw.read())


class StackFrame(list):
    @property
    def top(self):
        return self[-1]

    def push(self, value: object):
        self.append(value)

    def pop(self, index=-1) -> object:
        return super().pop(index)


class Stack(list):
    class NoStackFramesError(Exception):
        ...

    def _check_empty(self):
        if len(self) == 0:
            raise self.NoStackFramesError

    def push_frame(self, frame: StackFrame = None):
        self.append(frame or StackFrame())

    def pop_frame(self) -> StackFrame:
        self._check_empty()
        return super().pop(-1)

    def push(self, value: object):
        self._check_empty()
        self[-1].append(value)

    def pop(self, index=-1) -> object:
        self._check_empty()
        return self[-1].pop()

    @property
    def top(self):
        return self[-1].top


class VirtualMachine:
    def __init__(self, database: dict[str, DataType], stream: DataStream):
        self.database = database
        self.stream = stream
        self.stack = Stack()
        self.arrays: dict[int, list] = dict()
        self.outputs = StackFrame()

        self.stop = False
        self.break_loop = False

    @property
    def output(self):
        return self.outputs[-1]

    def exec_get(self, code: CodeObject):
        """ Get a field from output. """
        name = code.read_name()
        self.stack.push(self.output[name])

    def exec_put(self, code: CodeObject):
        """ Put a value into output. """
        name = code.read_name()
        self.output[name] = self.stack.top

    def exec_empty(self, code: CodeObject):
        """ Create an empty array. """
        no = code.read_int(WORD)
        self.arrays[no] = list()

    def exec_edit(self, code: CodeObject):
        """ Load an existing array. """
        no = code.read_int(WORD)
        name = code.read_name()
        self.arrays[no] = self.output[name]

    def exec_flip(self, code: CodeObject):
        """ Flip an array. """
        no = code.read_int(WORD)
        self.arrays[no] = self.arrays[no][::-1]

    def exec_yield(self, code: CodeObject):
        """ Pop a value from an array."""
        no = code.read_int(WORD)
        value = self.arrays[no].pop(-1)
        self.stack.push(value)

    def exec_append(self, code: CodeObject):
        """ Push a value onto the array. """
        no = code.read_int(WORD)
        self.arrays[no].append(self.stack.top)

    def exec_index(self, code: CodeObject):
        """ Get an index for an array. """
        index = code.read_int(QWORD)
        no = code.read_int(WORD)
        value = self.arrays[no][index]
        self.stack.push(value)

    def exec_finish(self, code: CodeObject):
        """ Move an array onto the stack. """
        no = code.read_int(WORD)
        value = self.arrays.pop(no)
        self.stack.push(value)

    def exec_forget(self, code: CodeObject):
        """ Free an array. """
        no = code.read_int(WORD)
        self.arrays.pop(no)

    def exec_push(self, code: CodeObject):
        """ Push a value onto the stack. """
        value = code.read_int(QWORD)
        self.stack.push(value)

    def exec_pop(self, _: CodeObject):
        """ Pop a value from the stack. """
        self.stack.pop()

    def exec_tell(self, _: CodeObject):
        """ Push the current stream pos to stack. """
        self.stack.push(self.stream)

    def exec_seek(self, code: CodeObject):
        """ Seek to a new position in the stream. """
        mode = code.read_int(BYTE)
        self.stream.seek(self.stack.top, mode)

    def exec_read(self, code: CodeObject):
        """ Read a data type from the stream. """
        name = code.read_name()

        dt = self.database[name]
        value = dt.read(self)
        self.stack.push(value)

    def exec_write(self, code: CodeObject):
        """ Write a data type to the stack. """
        name = code.read_name()

        dt = self.database[name]
        dt.write(self, self.stack.top)

    def exec_loop(self, code: CodeObject):
        count = code.read_int(QWORD)

        end = code.tell_end(count)
        start = code.tell()
        self.break_loop = False
        while not self.break_loop:
            for _ in range(count):
                self.exec_inst(code)

                if self.break_loop:
                    break

            code.seek(start)
        code.seek(end)

    def exec_loopx(self, code: CodeObject):
        iterations = code.read_int(QWORD)
        count = code.read_int(QWORD)

        end = code.tell_end(count)
        start = code.tell()
        self.break_loop = False
        for _ in range(iterations):
            if self.break_loop:
                break

            for _ in range(count):
                self.exec_inst(code)
                if self.break_loop:
                    break

            code.seek(start)
        code.seek(end)

    def exec_break(self, _: CodeObject):
        self.break_loop = True

    def exec_test(self, code: CodeObject):
        operation = code.read_int(BYTE)
        count = code.read_int(QWORD)

        left = self.stack.top

        result = None
        if operation == TestOperation.NOT:
            result = not left
        else:
            right = self.stack[-1][-2]

            if operation == TestOperation.EQ:
                result = left == right
            elif operation == TestOperation.NE:
                result = left != right
            elif operation == TestOperation.LT:
                result = left < right
            elif operation == TestOperation.GT:
                result = left > right
            elif operation == TestOperation.LE:
                result = left <= right
            elif operation == TestOperation.GE:
                result = left >= right
            elif operation == TestOperation.NOT:
                ...
            else:
                assert False

        if not result:
            end = code.tell_end(count)
            code.seek(end)
            return

        for _ in range(count):
            self.exec_inst(code)

    def exec_ret(self, _: CodeObject):
        self.stop = True

    def exec_inst(self, code: CodeObject):
        op = code.read_int(BYTE)

        proc = {
            Instruction.GET: self.exec_get,
            Instruction.PUT: self.exec_put,
            Instruction.EMPTY: self.exec_empty,
            Instruction.EDIT: self.exec_edit,
            Instruction.FLIP: self.exec_flip,
            Instruction.YIELD: self.exec_yield,
            Instruction.APPEND: self.exec_append,
            Instruction.INDEX: self.exec_index,
            Instruction.FINISH: self.exec_finish,
            Instruction.FORGET: self.exec_forget,
            Instruction.PUSH: self.exec_push,
            Instruction.POP: self.exec_pop,
            Instruction.READ: self.exec_read,
            Instruction.WRITE: self.exec_write,
            Instruction.LOOP: self.exec_loop,
            Instruction.LOOPX: self.exec_loopx,
            Instruction.BREAK: self.exec_break,
            Instruction.TEST: self.exec_test,
            Instruction.RET: self.exec_ret,
            # Instruction.GOTO: self.exec_goto,
        }[op]

        proc(code)  # noqa

    def run(self, code: CodeObject, value: object) -> object:
        self.outputs.push(value)
        self.stack.push_frame()

        self.stop = False
        while not self.stop:
            self.exec_inst(code)

        self.stack.pop_frame()
        return self.outputs.pop()


class DataType(ABC):
    @abstractmethod
    def read(self, vm: VirtualMachine) -> object:
        ...

    @abstractmethod
    def write(self, vm: VirtualMachine, value: object):
        ...


class PrimitiveType(DataType, ABC):
    ...


class IntType(PrimitiveType):
    __slots__ = 'size', 'byteorder', 'signed'

    def __init__(self, size: int, byteorder: Byteorder, signed: bool):
        self.size = size
        self.byteorder = byteorder
        self.signed = signed

    def read(self, vm: VirtualMachine) -> int:
        return int.from_bytes(
            bytes=vm.stream.read(self.size),
            byteorder=self.byteorder,  # noqa
            signed=self.signed,
        )

    def write(self, vm: VirtualMachine, value: int):
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

    def read(self, vm: VirtualMachine) -> float:
        return unpack('f', vm.stream.read(self.size))[0]

    def write(self, vm: VirtualMachine, value: float):
        vm.stream.write(pack(self.format, value))


class ComplexType(DataType, ABC):
    __slots__ = 'read_code', 'write_code'

    def __init__(self, read_code: CodeObject, write_code: CodeObject):
        self.read_code = read_code
        self.write_code = write_code

    @abstractmethod
    def empty(self) -> dict:
        ...

    def read(self, vm: VirtualMachine) -> dict:
        value = vm.run(self.read_code, self.empty())
        assert isinstance(value, dict)
        return value

    def write(self, vm: VirtualMachine, value: dict):
        vm.run(
            self.write_code,
            value,
        )


def get_database() -> dict:
    return {
        'u8l': IntType(1, Byteorder.LITTLE, False),
        'u16l': IntType(2, Byteorder.LITTLE, False),
        'u32l': IntType(4, Byteorder.LITTLE, False),
        'u64l': IntType(8, Byteorder.LITTLE, False),
        'i8l': IntType(1, Byteorder.LITTLE, True),
        'i16l': IntType(2, Byteorder.LITTLE, True),
        'i32l': IntType(4, Byteorder.LITTLE, True),
        'i64l': IntType(8, Byteorder.LITTLE, True),

        'u8b': IntType(1, Byteorder.BIG, False),
        'u16b': IntType(2, Byteorder.BIG, False),
        'u32b': IntType(4, Byteorder.BIG, False),
        'u64b': IntType(8, Byteorder.BIG, False),
        'i8b': IntType(1, Byteorder.BIG, True),
        'i16b': IntType(2, Byteorder.BIG, True),
        'i32b': IntType(4, Byteorder.BIG, True),
        'i64b': IntType(8, Byteorder.BIG, True),

        'f32': FloatType(4),
        'f64': FloatType(8),
    }


