from byte_ninja.bytecode.assembler import *
from byte_ninja.bytecode.disassembler import *
from byte_ninja.backends.pythonic.code_object import BaseCodeObject

def strip(source: str) -> str:
    return (
        source
        .replace(' ', '')
        .replace('\t', '')
        .replace('\n', '')
        .replace('\r', '')
    )

def run(source: str):
    asm = Assembler(source, OperationMode.READ)

    obj = BaseCodeObject.from_bytes(
        asm.get_output()
    )

    dis = Disassembler(obj)
    dis_source = dis.source.getvalue()

    assert strip(source) == strip(dis_source)



def test_get(): run('get name')
def test_put(): run('put name')
def test_empty(): run('empty 0')
def test_edit(): run('edit 0')
def test_flip(): run('flip 0')
def test_yield(): run('yield 0')
def test_append(): run('append 0')
def test_index(): run('index 0')
def test_finish(): run('finish 0')
def test_forget(): run('forget 0')
def test_push(): run('push 0')
def test_pop(): run('pop')
def test_read(): run('read name')
def test_rarray(): run('rarray name')
def test_write(): run('write name')
def test_warray(): run('warray name')
def test_loopx(): run('loopx: pop end')
def test_loop(): run('loop: pop end')
def test_break(): run('break')
def test_test(): run('test EQ: pop end')
def test_ret(): run('ret')
def test_seek(): run('seek END')
def test_tell(): run('tell')
def test_encode(): run('encode name')
def test_decode(): run('decode name')

