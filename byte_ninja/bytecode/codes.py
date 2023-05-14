from enum import IntEnum

from byte_ninja.enums import ByteOrder
from byte_ninja.sizes import *


c = iter(range(1000))
class OPCode(IntEnum):
    # data structure manipulation
    GET = next(c)  # get a field from input
    PUT = next(c)  # put a field into output

    # array manipulation
    EMPTY = next(c)  # start a new array
    EDIT = next(c)  # load an existing array from a field
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

    # strings
    ENCODE = next(c)  # encode an array from the stack
    DECODE = next(c)  # decode an array from the stack


# the length of every instruction
INSTRUCTION_LENGTHS = {
    OPCode.GET: BYTE + QWORD,
    OPCode.PUT: BYTE + QWORD,
    OPCode.EMPTY: BYTE + WORD,
    OPCode.EDIT: BYTE + WORD + QWORD,
    OPCode.FLIP: BYTE + WORD,
    OPCode.YIELD: BYTE + WORD,
    OPCode.APPEND: BYTE + WORD,
    OPCode.INDEX: BYTE + QWORD + WORD,
    OPCode.FINISH: BYTE + WORD,
    OPCode.FORGET: BYTE + WORD,
    OPCode.PUSH: BYTE + QWORD,
    OPCode.POP: BYTE,
    OPCode.READ: BYTE + QWORD,
    OPCode.RARRAY: BYTE + QWORD,
    OPCode.WRITE: BYTE + QWORD,
    OPCode.WARRAY: BYTE + QWORD,
    OPCode.LOOP: BYTE + QWORD,
    OPCode.LOOPX: BYTE + QWORD + QWORD,
    OPCode.BREAK: BYTE,
    OPCode.TEST: BYTE + BYTE + QWORD,
    OPCode.RET: BYTE,
    OPCode.SEEK: BYTE + BYTE,
    OPCode.TELL: BYTE,
    OPCode.ENCODE: BYTE + QWORD,
    OPCode.DECODE: BYTE + QWORD,
}


class OperationCode(IntEnum):
    EQ = 0
    NE = 1
    LT = 2
    GT = 3
    LE = 4
    GE = 5
    NOT = 6


BYTECODE_BYTEORDER = ByteOrder.LITTLE
