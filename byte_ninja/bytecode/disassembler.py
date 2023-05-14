from .token import *
from .codes import *
from byte_ninja.sizes import *
from byte_ninja.backends.pythonic.code_object import BaseCodeObject

from io import StringIO
from enum import IntEnum


class Disassembler:
    class PatternType(IntEnum):
        EMIT_LEVEL = 0
        EMIT_ENUM = 1
        EMIT_NAME = 2
        EMIT_INTEGER = 3
        EMIT_TOKEN = 4

    TOK_EOL = -1

    def __init__(self, code: BaseCodeObject):
        self.code = code
        self.source = StringIO()
        self.indent_level = 0
        self.line_buffer = StringIO()

        emit_level = (self.PatternType.EMIT_LEVEL,)
        emit_name = (self.PatternType.EMIT_NAME,)

        emit_integer = lambda s: (self.PatternType.EMIT_INTEGER, s)
        emit_enum = lambda opts, s: (self.PatternType.EMIT_ENUM, opts, s)
        emit_token = lambda t: (self.PatternType.EMIT_TOKEN, t)
        emit_eol = (self.PatternType.EMIT_TOKEN, self.TOK_EOL)

        self.patterns = {
            OPCode.GET: [emit_name, emit_eol],
            OPCode.PUT: [emit_name, emit_eol],
            OPCode.EMPTY: [emit_integer(WORD), emit_eol],
            OPCode.EDIT: [emit_integer(WORD), emit_eol],
            OPCode.FLIP: [emit_integer(WORD), emit_eol],
            OPCode.YIELD: [emit_integer(WORD), emit_eol],
            OPCode.APPEND: [emit_integer(WORD), emit_eol],
            OPCode.INDEX: [emit_integer(WORD), emit_eol],
            OPCode.FINISH: [emit_integer(WORD), emit_eol],
            OPCode.FORGET: [emit_integer(WORD), emit_eol],
            OPCode.PUSH: [emit_integer(QWORD), emit_eol],
            OPCode.POP: [emit_eol],
            OPCode.READ: [emit_name, emit_eol],
            OPCode.RARRAY: [emit_name, emit_eol],
            OPCode.WRITE: [emit_name, emit_eol],
            OPCode.WARRAY: [emit_name, emit_eol],
            OPCode.LOOP: [emit_token(TOK_COLON), emit_eol, emit_level, emit_eol],
            OPCode.LOOPX: [emit_token(TOK_COLON), emit_eol, emit_level, emit_eol],
            OPCode.BREAK: [emit_eol],
            OPCode.TEST: [emit_enum({
                OperationCode.EQ: TOK_EQ,
                OperationCode.NE: TOK_NE,
                OperationCode.LT: TOK_LT,
                OperationCode.GT: TOK_GT,
                OperationCode.LE: TOK_LE,
                OperationCode.GE: TOK_GE,
                OperationCode.NOT: TOK_NOT,
            }, BYTE), emit_token(TOK_COLON), emit_eol, emit_level, emit_eol],
            OPCode.RET: [emit_eol],
            OPCode.SEEK: [emit_enum({
                SeekMode.START: TOK_SEEK_START,
                SeekMode.REL: TOK_SEEK_REL,
                SeekMode.END: TOK_SEEK_END,
            }, BYTE), emit_eol],
            OPCode.TELL: [emit_eol],
            OPCode.ENCODE: [emit_name, emit_eol],
            OPCode.DECODE: [emit_name, emit_eol],
        }

        while not self.code.eof:
            self.emit_instruction()

    def emit(self, source: str):
        indent = ' ' * 4

        while source:
            # read a line segment
            line_seg, eol, source = source.partition('\n')

            self.line_buffer.write(line_seg)

            if not eol:
                break

            # we reached eol, flush the buffer
            self.source.write(
                indent * self.indent_level + self.line_buffer.getvalue() + eol
            )

            self.line_buffer.seek(0)
            self.line_buffer.truncate()


    def emit_integer(self, size: int):
        value = self.code.read_uint(size)
        self.emit(str(value))

    def emit_enum(self, opts: dict[int, TokenType], size: int):
        value = self.code.read_uint(size)

        tok = TOKEN_TYPE_TO_EXACT[opts[value]]
        self.emit(tok)

    def emit_name(self):
        self.emit(
            self.code.read_name()
        )

    def emit_token(self, typ: TokenType):
        if typ == -1:
            self.emit('\n')
            return

        self.emit(TOKEN_TYPE_TO_EXACT[typ])

    def emit_pattern(self, pattern: list[tuple]):

        for sub in pattern:
            if sub[0] == self.PatternType.EMIT_LEVEL:
                self.emit_level()
            elif sub[0] == self.PatternType.EMIT_NAME:
                self.emit_name()
            elif sub[0] == self.PatternType.EMIT_ENUM:
                self.emit_enum(*sub[1:])
            elif sub[0] == self.PatternType.EMIT_INTEGER:
                self.emit_integer(*sub[1:])
            elif sub[0] == self.PatternType.EMIT_TOKEN:
                self.emit_token(*sub[1:])
            else:
                assert False

    def emit_instruction(self):
        op = self.code.read_uint(BYTE)

        self.emit(
            TOKEN_TYPE_TO_EXACT[
                OPCODE_TO_TOKEN[op]
            ]
        )

        self.emit_pattern(
            self.patterns[op]
        )

    def emit_level(self):
        self.indent_level += 1

        # read count
        count = self.code.read_uint(QWORD)

        for _ in range(count):
            self.emit_instruction()

        self.indent_level -= 1
        self.emit_token(TOK_END)
