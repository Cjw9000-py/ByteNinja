from byte_ninja.sizes import *
from byte_ninja.stream import Stream
from byte_ninja.bytecode.codes import OPCode, OperationCode

from .stack import Stack, StackFrame
from .code_object import CodeObject
from .data_type import DataType


class VirtualMachine:
    def __init__(self, database: dict[str, DataType], stream: Stream):
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
        if operation == OperationCode.NOT:
            result = not left
        else:
            right = self.stack[-1][-2]

            if operation == OperationCode.EQ:
                result = left == right
            elif operation == OperationCode.NE:
                result = left != right
            elif operation == OperationCode.LT:
                result = left < right
            elif operation == OperationCode.GT:
                result = left > right
            elif operation == OperationCode.LE:
                result = left <= right
            elif operation == OperationCode.GE:
                result = left >= right
            elif operation == OperationCode.NOT:
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
            OPCode.GET: self.exec_get,
            OPCode.PUT: self.exec_put,
            OPCode.EMPTY: self.exec_empty,
            OPCode.EDIT: self.exec_edit,
            OPCode.FLIP: self.exec_flip,
            OPCode.YIELD: self.exec_yield,
            OPCode.APPEND: self.exec_append,
            OPCode.INDEX: self.exec_index,
            OPCode.FINISH: self.exec_finish,
            OPCode.FORGET: self.exec_forget,
            OPCode.PUSH: self.exec_push,
            OPCode.POP: self.exec_pop,
            OPCode.READ: self.exec_read,
            OPCode.WRITE: self.exec_write,
            OPCode.LOOP: self.exec_loop,
            OPCode.LOOPX: self.exec_loopx,
            OPCode.BREAK: self.exec_break,
            OPCode.TEST: self.exec_test,
            OPCode.RET: self.exec_ret,
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
