import pytest

from byte_ninja.bytecode.sizes import *
from byte_ninja.bytecode.assembler import Assembler
from byte_ninja.bytecode.codes import (
    BYTECODE_BYTEORDER_AS_LITERAL,
    OperationMode,
    SeekMode,
    TestOperation,
    OPCode,
)

QWORD_ONE = b'\01' + b'\x00' * (QWORD - 1)
QWORD_NULL = b'\x00' * QWORD
WORD_NULL = b'\x00' * WORD

def j(*args: bytes) -> bytes:
    return b''.join(args)

def b(x: int) -> bytes:
    return bytes([x])

def enc(x: int, size: int) -> bytes:
    return x.to_bytes(size, BYTECODE_BYTEORDER_AS_LITERAL)

def run(source: str, expected_bytecode: bytes):
    asm = Assembler(source, None)  # noqa
    assert expected_bytecode == asm.bytecode.getvalue(), (
        expected_bytecode, asm.bytecode.getvalue())
    
def test_get(): run('get name', j(b(OPCode.GET), QWORD_NULL)),
def test_put(): run('put name', j(b(OPCode.PUT), QWORD_NULL)),
def test_empty(): run('empty 0', j(b(OPCode.EMPTY), WORD_NULL)),
def test_edit(): run('edit 0', j(b(OPCode.EDIT), WORD_NULL)),
def test_flip(): run('flip 0', j(b(OPCode.FLIP), WORD_NULL)),
def test_yield(): run('yield 0', j(b(OPCode.YIELD), WORD_NULL)),
def test_append(): run('append 0', j(b(OPCode.APPEND), WORD_NULL)),
def test_index(): run('index 0', j(b(OPCode.INDEX), WORD_NULL)),
def test_finish(): run('finish 0', j(b(OPCode.FINISH), WORD_NULL)),
def test_forget(): run('forget 0', j(b(OPCode.FORGET), WORD_NULL)),
def test_push(): run('push 0', j(b(OPCode.PUSH), QWORD_NULL)),
def test_pop(): run('pop', j(b(OPCode.POP))),
def test_read(): run('read name', j(b(OPCode.READ), QWORD_NULL)),
def test_rarray(): run('rarray name', j(b(OPCode.RARRAY), QWORD_NULL)),
def test_write(): run('write name', j(b(OPCode.WRITE), QWORD_NULL)),
def test_warray(): run('warray name', j(b(OPCode.WARRAY), QWORD_NULL)),
def test_loopx(): run('loopx: pop end', j(b(OPCode.LOOPX), QWORD_ONE, b(OPCode.POP))),
def test_loop(): run('loop: pop end', j(b(OPCode.LOOP), QWORD_ONE, b(OPCode.POP))),
def test_break(): run('break', j(b(OPCode.BREAK))),
def test_test(): run('test EQ: pop end', j(b(OPCode.TEST), enc(TestOperation.EQ, BYTE), QWORD_ONE, b(OPCode.POP))),
def test_ret(): run('ret', j(b(OPCode.RET))),
def test_seek(): run('seek END', j(b(OPCode.SEEK), enc(SeekMode.END, BYTE))),
def test_tell(): run('tell', j(b(OPCode.TELL))),
def test_encode(): run('encode name', j(b(OPCode.ENCODE), QWORD_NULL)),
def test_decode(): run('decode name', j(b(OPCode.DECODE), QWORD_NULL)),
