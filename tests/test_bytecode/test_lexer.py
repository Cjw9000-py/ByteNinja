import pytest  # noqa

from byte_ninja.bytecode.token import *
from byte_ninja.bytecode.lexer import *

basic_token_code = """\
 push 42 pop
end START END
"""

token_code = """\
get
put
empty
edit
flip
yield
append
index
finish
forget
push
pop
read
write
loopx
loop
break
test
ret
seek
tell
end
EQ
NE
LT
GT
LE
GE
NOT
REL
START
END
42
some_name
# some comment
"""

token_types = [
    TOK_GET,
    TOK_PUT,
    TOK_EMPTY,
    TOK_EDIT,
    TOK_FLIP,
    TOK_YIELD,
    TOK_APPEND,
    TOK_INDEX,
    TOK_FINISH,
    TOK_FORGET,
    TOK_PUSH,
    TOK_POP,
    TOK_READ,
    TOK_WRITE,
    TOK_LOOPX,
    TOK_LOOP,
    TOK_BREAK,
    TOK_TEST,
    TOK_RET,
    TOK_SEEK,
    TOK_TELL,
    TOK_END,
    TOK_EQ,
    TOK_NE,
    TOK_LT,
    TOK_GT,
    TOK_LE,
    TOK_GE,
    TOK_NOT,
    TOK_SEEK_REL,
    TOK_SEEK_START,
    TOK_SEEK_END,
    TOK_NUMBER,
    TOK_NAME,
    TOK_COMMENT,
    TOK_EOF,
]

def test_with_mock_code():
    tokens = tokenize(basic_token_code)
    types = [t.type for t in tokens]

    assert types == [
        TOK_PUSH,
        TOK_NUMBER,
        TOK_POP,
        TOK_END,
        TOK_SEEK_START,
        TOK_SEEK_END,
        TOK_EOF,
    ]

    ln_one = tokens[:3]
    ln_two = tokens[3:-1]  # exclude eof

    assert ln_one[0].lineno == 1
    assert ln_one[1].lineno == 1
    assert ln_one[2].lineno == 1

    assert ln_two[0].lineno == 2
    assert ln_two[1].lineno == 2
    assert ln_two[2].lineno == 2

    for t in tokens:
        assert t.whitespace

def test_lex_all_tokens():
    tokens = tokenize(token_code)
    types = [TOKEN_TYPE_TO_NAME[t.type] for t in tokens]

    assert types == [TOKEN_TYPE_TO_NAME[t] for t in token_types]


