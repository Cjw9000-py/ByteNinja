from .sizes import *
from .token import *
from .lexer import tokenize
from .stream import BufferedStream
from .syntax import SyntaxTree, Node, NODE_LEVEL
from .codes import BYTECODE_BYTEORDER, OperationMode

from enum import IntEnum


class Assembler:
    class PatternType(IntEnum):
        EMIT_LEVEL = 0
        EMIT_INTEGER = 1
        EMIT_ENUM = 2
        EMIT_NAME = 3
        SKIP = 4


    def __init__(self, source: str, mode: OperationMode):
        self.mode = mode
        self.tokens = tokenize(source)
        self.tree = SyntaxTree(self.tokens)
        self.name_table = list()
        self.bytecode = BufferedStream()
        self.bytecode.byteorder = BYTECODE_BYTEORDER

        emit_level = (self.PatternType.EMIT_LEVEL, )
        emit_name = (self.PatternType.EMIT_NAME,)
        skip = (self.PatternType.SKIP,)

        emit_integer = lambda s: (self.PatternType.EMIT_INTEGER, s)
        emit_enum = lambda opts, s: (self.PatternType.EMIT_ENUM, opts, s)

        self.patterns = {
            OPCode.GET: [emit_name],
            OPCode.PUT: [emit_name],
            OPCode.EMPTY: [emit_integer(WORD)],
            OPCode.EDIT: [emit_integer(WORD)],
            OPCode.FLIP: [emit_integer(WORD)],
            OPCode.YIELD: [emit_integer(WORD)],
            OPCode.APPEND: [emit_integer(WORD)],
            OPCode.INDEX: [emit_integer(WORD)],
            OPCode.FINISH: [emit_integer(WORD)],
            OPCode.FORGET: [emit_integer(WORD)],
            OPCode.PUSH: [emit_integer(QWORD)],
            OPCode.POP: [],
            OPCode.READ: [emit_name],
            OPCode.RARRAY: [emit_name],
            OPCode.WRITE: [emit_name],
            OPCode.WARRAY: [emit_name],
            OPCode.LOOPX: [skip, emit_level],
            OPCode.LOOP: [skip, emit_level],
            OPCode.BREAK: [],
            OPCode.TEST: [emit_enum({
                TOK_EQ: TestOperation.EQ,
                TOK_NE: TestOperation.NE,
                TOK_LT: TestOperation.LT,
                TOK_GT: TestOperation.GT,
                TOK_LE: TestOperation.LE,
                TOK_GE: TestOperation.GE,
                TOK_NOT: TestOperation.NOT,
            }, BYTE), skip, emit_level],
            OPCode.RET: [],
            OPCode.SEEK: [emit_enum({
                TOK_SEEK_START: SeekMode.START,
                TOK_SEEK_REL: SeekMode.REL,
                TOK_SEEK_END: SeekMode.END,
            }, BYTE)],
            OPCode.TELL: [],
            OPCode.ENCODE: [emit_name],
            OPCode.DECODE: [emit_name],
        }

        for n in self.tree:
            self.emit_instruction(n)

    def get_output(self) -> bytes:
        return self.parse_header() + self.bytecode.getvalue()

    def parse_header(self) -> bytes:
        buf = BufferedStream()
        buf.byteorder = BYTECODE_BYTEORDER

        buf.write_uint(self.mode, BYTE)
        buf.write_uint(len(self.name_table), QWORD)

        for n in self.name_table:
            buf.write_cstring(n)

        return buf.getvalue()

    def emit_integer(self, tok: Token, size: int):
        assert tok.type == TOK_NUMBER
        self.bytecode.write_uint(int(tok.value), size)

    def emit_name(self, tok: Token):
        assert tok.type == TOK_NAME

        index = len(self.name_table)
        self.name_table.append(tok.value)
        self.bytecode.write_uint(index, QWORD)

    def emit_enum(self, tok: Token, opts: dict[TokenType, int], size: int):
        assert tok.type in opts.keys()

        value = opts[tok.type]
        self.bytecode.write_uint(value, size)

    def emit_pattern(self, pattern: list[tuple], nodes: list):
        assert len(pattern) == len(nodes)

        for p, n in zip(pattern, nodes):
            if p[0] == self.PatternType.EMIT_NAME:
                self.emit_name(n)
            elif p[0] == self.PatternType.EMIT_ENUM:
                self.emit_enum(n, *p[1:])
            elif p[0] == self.PatternType.EMIT_INTEGER:
                self.emit_integer(n, *p[1:])
            elif p[0] == self.PatternType.EMIT_LEVEL:
                self.emit_level(n)
            elif p[0] == self.PatternType.SKIP:
                ...
            else:
                assert False

    def emit_instruction(self, node: Node):
        assert node.type in self.patterns

        self.bytecode.write_uint(node.type, BYTE)  # token type is the opcode

        pattern = self.patterns[node.type]
        self.emit_pattern(pattern, node)

    def emit_level(self, node: Node):
        assert node.type == NODE_LEVEL

        self.bytecode.write_uint(len(node), QWORD)

        for n in node:
            self.emit_instruction(n)
