import pytest  # noqa

from byte_ninja.bytecode.token import *
from byte_ninja.bytecode.lexer import *
from byte_ninja.bytecode.syntax import *


test_code = """\
get some_name
put some_name
empty 42
edit 42
flip 42
yield 42
append 42
index 42
finish 42
forget 42
push 42
pop
read some_type
rarray some_type
write some_type
warray some_type
break
ret
seek END
tell
encode some_encoding
decode some_encoding

loop: 
    pop
    pop
end

loopx: 
    pop
    pop
end

test EQ: pop end
test NE: pop end
test LT: pop end
test GT: pop end
test LE: pop end
test GE: pop end
test NOT: pop end
"""


node_types = [
    OPCode.GET,
    OPCode.PUT,
    OPCode.EMPTY,
    OPCode.EDIT,
    OPCode.FLIP,
    OPCode.YIELD,
    OPCode.APPEND,
    OPCode.INDEX,
    OPCode.FINISH,
    OPCode.FORGET,
    OPCode.PUSH,
    OPCode.POP,
    OPCode.READ,
    OPCode.RARRAY,
    OPCode.WRITE,
    OPCode.WARRAY,
    OPCode.BREAK,
    OPCode.RET,
    OPCode.SEEK,
    OPCode.TELL,
    OPCode.ENCODE,
    OPCode.DECODE,

    OPCode.LOOP,
    OPCode.LOOPX,

    OPCode.TEST,
    OPCode.TEST,
    OPCode.TEST,
    OPCode.TEST,
    OPCode.TEST,
    OPCode.TEST,
    OPCode.TEST,
]

node_lengths = [
    1,  # OPCode.GET
    1,  # OPCode.PUT
    1,  # OPCode.EMPTY
    1,  # OPCode.EDIT
    1,  # OPCode.FLIP
    1,  # OPCode.YIELD
    1,  # OPCode.APPEND
    1,  # OPCode.INDEX
    1,  # OPCode.FINISH
    1,  # OPCode.FORGET
    1,  # OPCode.PUSH
    0,  # OPCode.POP
    1,  # OPCode.READ
    1,  # OPCode.RARRAY
    1,  # OPCode.WRITE
    1,  # OPCode.WARRAY
    0,  # OPCode.BREAK
    0,  # OPCode.RET
    1,  # OPCode.SEEK
    0,  # OPCode.TELL
    1,  # OPCode.ENCODE
    1,  # OPCode.DECODE
    2,  # OPCode.LOOP
    2,  # OPCode.LOOPX
    3,  # OPCode.TEST
    3,  # OPCode.TEST
    3,  # OPCode.TEST
    3,  # OPCode.TEST
    3,  # OPCode.TEST
    3,  # OPCode.TEST
    3,  # OPCode.TEST
]


def test_syntax():
    tokens = tokenize(test_code)
    tree = SyntaxTree(tokens)

    types = [n.type for n in tree]

    assert types == node_types

    assert [len(n) for n in tree] == node_lengths

