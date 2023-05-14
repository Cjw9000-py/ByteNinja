import re
from .codes import OPCode, SeekMode, OperationCode


TokenType = int

class Token:
    __slots__ = (
        'type',
        'value',
        'lineno',
        'whitespace',
    )

    def __init__(self, typ: TokenType,
                 value: str | re.Pattern,
                 lineno: int = None,
                 whitespace: str = ''):

        self.type = typ
        self.value = value
        self.lineno = lineno
        self.whitespace = whitespace

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'type={TOKEN_TYPE_TO_NAME[self.type]}, '
            f'value={repr(self.value)}, '
            f'lineno={self.lineno}, '
            f'whitespace={repr(self.whitespace)})'
        )

def exact(t: TokenType, value: str) -> Token:
    return Token(
        t,
        re.compile(rf'^({re.escape(value)})(?:\W|$)'),
    )

c = iter(range(1000))

TOK_GET = next(c)
TOK_PUT = next(c)
TOK_EMPTY = next(c)
TOK_EDIT = next(c)
TOK_FLIP = next(c)
TOK_YIELD = next(c)
TOK_APPEND = next(c)
TOK_INDEX = next(c)
TOK_FINISH = next(c)
TOK_FORGET = next(c)
TOK_PUSH = next(c)
TOK_POP = next(c)
TOK_READ = next(c)
TOK_RARRAY = next(c)
TOK_WRITE = next(c)
TOK_WARRAY = next(c)
TOK_LOOPX = next(c)
TOK_LOOP = next(c)
TOK_BREAK = next(c)
TOK_TEST = next(c)
TOK_RET = next(c)
TOK_SEEK = next(c)
TOK_TELL = next(c)
TOK_ENCODE = next(c)
TOK_DECODE = next(c)
TOK_END = next(c)

TOK_EQ = next(c)
TOK_NE = next(c)
TOK_LT = next(c)
TOK_GT = next(c)
TOK_LE = next(c)
TOK_GE = next(c)
TOK_NOT = next(c)

TOK_NUMBER = next(c)
TOK_NAME = next(c)
TOK_COMMENT = next(c)

TOK_SEEK_START = next(c)
TOK_SEEK_REL = next(c)
TOK_SEEK_END = next(c)

TOK_COLON = next(c)
TOK_EOF = next(c)

WHITESPACE = re.compile(r'^[\t\r\n ]*')

TOKEN_DEFS = [
    exact(TOK_GET, 'get'),
    exact(TOK_PUT, 'put'),
    exact(TOK_EMPTY, 'empty'),
    exact(TOK_EDIT, 'edit'),
    exact(TOK_FLIP, 'flip'),
    exact(TOK_YIELD, 'yield'),
    exact(TOK_APPEND, 'append'),
    exact(TOK_INDEX, 'index'),
    exact(TOK_FINISH, 'finish'),
    exact(TOK_FORGET, 'forget'),
    exact(TOK_PUSH, 'push'),
    exact(TOK_POP, 'pop'),
    exact(TOK_READ, 'read'),
    exact(TOK_RARRAY, 'rarray'),
    exact(TOK_WRITE, 'write'),
    exact(TOK_WARRAY, 'warray'),
    exact(TOK_LOOPX, 'loopx'),
    exact(TOK_LOOP, 'loop'),
    exact(TOK_BREAK, 'break'),
    exact(TOK_TEST, 'test'),
    exact(TOK_RET, 'ret'),
    exact(TOK_SEEK, 'seek'),
    exact(TOK_TELL, 'tell'),
    exact(TOK_ENCODE, 'encode'),
    exact(TOK_DECODE, 'decode'),
    exact(TOK_END, 'end'),
    exact(TOK_EQ, 'EQ'),
    exact(TOK_NE, 'NE'),
    exact(TOK_LT, 'LT'),
    exact(TOK_GT, 'GT'),
    exact(TOK_LE, 'LE'),
    exact(TOK_GE, 'GE'),
    exact(TOK_NOT, 'NOT'),
    exact(TOK_SEEK_REL, 'REL'),
    exact(TOK_SEEK_START, 'START'),
    exact(TOK_SEEK_END, 'END'),
    exact(TOK_COLON, ':'),
    Token(TOK_NUMBER, re.compile(r'(^[0-9]+)')),
    Token(TOK_NAME, re.compile(r'(^\w+)')),
    Token(TOK_COMMENT, re.compile(r'(^#[^\n]+)')),
]

TOKEN_TYPE_TO_NAME = {
    TOK_GET: 'GET',
    TOK_PUT: 'PUT',
    TOK_EMPTY: 'EMPTY',
    TOK_EDIT: 'EDIT',
    TOK_FLIP: 'FLIP',
    TOK_YIELD: 'YIELD',
    TOK_APPEND: 'APPEND',
    TOK_INDEX: 'INDEX',
    TOK_FINISH: 'FINISH',
    TOK_FORGET: 'FORGET',
    TOK_PUSH: 'PUSH',
    TOK_POP: 'POP',
    TOK_READ: 'READ',
    TOK_RARRAY: 'RARRAY',
    TOK_WRITE: 'WRITE',
    TOK_WARRAY: 'WARRAY',
    TOK_LOOPX: 'LOOPX',
    TOK_LOOP: 'LOOP',
    TOK_BREAK: 'BREAK',
    TOK_TEST: 'TEST',
    TOK_RET: 'RET',
    TOK_SEEK: 'SEEK',
    TOK_TELL: 'TELL',
    TOK_ENCODE: 'ENCODE',
    TOK_DECODE: 'DECODE',
    TOK_END: 'END',
    TOK_EQ: 'EQ',
    TOK_NE: 'NE',
    TOK_LT: 'LT',
    TOK_GT: 'GT',
    TOK_LE: 'LE',
    TOK_GE: 'GE',
    TOK_NOT: 'NOT',
    TOK_SEEK_REL: 'SEEK_REL',
    TOK_SEEK_START: 'SEEK_START',
    TOK_SEEK_END: 'SEEK_END',
    TOK_NUMBER: 'NUMBER',
    TOK_NAME: 'NAME',
    TOK_COMMENT: 'COMMENT',
    TOK_COLON: 'COLON',
    TOK_EOF: 'EOF',
}

TOKEN_TYPE_TO_EXACT = {
    TOK_GET: 'get',
    TOK_PUT: 'put',
    TOK_EMPTY: 'empty',
    TOK_EDIT: 'edit',
    TOK_FLIP: 'flip',
    TOK_YIELD: 'yield',
    TOK_APPEND: 'append',
    TOK_INDEX: 'index',
    TOK_FINISH: 'finish',
    TOK_FORGET: 'forget',
    TOK_PUSH: 'push',
    TOK_POP: 'pop',
    TOK_READ: 'read',
    TOK_RARRAY: 'rarray',
    TOK_WRITE: 'write',
    TOK_WARRAY: 'warray',
    TOK_LOOPX: 'loopx',
    TOK_LOOP: 'loop',
    TOK_BREAK: 'break',
    TOK_TEST: 'test',
    TOK_RET: 'ret',
    TOK_SEEK: 'seek',
    TOK_TELL: 'tell',
    TOK_ENCODE: 'encode',
    TOK_DECODE: 'decode',
    TOK_END: 'end',
    TOK_EQ: 'EQ',
    TOK_NE: 'NE',
    TOK_LT: 'LT',
    TOK_GT: 'GT',
    TOK_LE: 'LE',
    TOK_GE: 'GE',
    TOK_NOT: 'NOT',
    TOK_SEEK_REL: 'REL',
    TOK_SEEK_START: 'START',
    TOK_SEEK_END: 'END',
    TOK_COLON: ':',
}

TOKEN_TO_OPCODE = {
    TOK_GET: OPCode.GET,
    TOK_PUT: OPCode.PUT,
    TOK_EMPTY: OPCode.EMPTY,
    TOK_EDIT: OPCode.EDIT,
    TOK_FLIP: OPCode.FLIP,
    TOK_YIELD: OPCode.YIELD,
    TOK_APPEND: OPCode.APPEND,
    TOK_INDEX: OPCode.INDEX,
    TOK_FINISH: OPCode.FINISH,
    TOK_FORGET: OPCode.FORGET,
    TOK_PUSH: OPCode.PUSH,
    TOK_POP: OPCode.POP,
    TOK_READ: OPCode.READ,
    TOK_RARRAY: OPCode.RARRAY,
    TOK_WRITE: OPCode.WRITE,
    TOK_WARRAY: OPCode.WARRAY,
    TOK_LOOPX: OPCode.LOOPX,
    TOK_LOOP: OPCode.LOOP,
    TOK_BREAK: OPCode.BREAK,
    TOK_TEST: OPCode.TEST,
    TOK_RET: OPCode.RET,
    TOK_SEEK: OPCode.SEEK,
    TOK_TELL: OPCode.TELL,
    TOK_ENCODE: OPCode.ENCODE,
    TOK_DECODE: OPCode.DECODE,
}

TOKEN_TO_SEEK_MODE = {
    TOK_SEEK_REL: SeekMode.REL,
    TOK_SEEK_START: SeekMode.START,
    TOK_SEEK_END: SeekMode.END,
}


TOKEN_TO_OPERATION = {
    TOK_EQ: OperationCode.EQ,
    TOK_NE: OperationCode.NE,
    TOK_LT: OperationCode.LT,
    TOK_GT: OperationCode.GT,
    TOK_LE: OperationCode.LE,
    TOK_GE: OperationCode.GE,
    TOK_NOT: OperationCode.NOT,
}


OPCODE_TO_TOKEN = {v: k for k, v in TOKEN_TO_OPCODE.items()}
SEEK_MODE_TO_TOKEN = {v: k for k, v in TOKEN_TO_OPCODE.items()}
OPERATION_TO_TOKEN = {v: k for k, v in TOKEN_TO_OPCODE.items()}
