import pytest
from byte_ninja.bytecode.stream import BufferedStream
from byte_ninja.bytecode.codes import Byteorder


@pytest.fixture
def stream():
    return BufferedStream()


def test_read_int_with_no_byteorder_provided_raises_error(stream):
    with pytest.raises(AssertionError):
        stream.read_int(2)


def test_write_int_with_non_integer_value_raises_error(stream):
    with pytest.raises(AssertionError):
        stream.write_int("invalid", 2)  # noqa


def test_write_int_writes_correct_value(stream):
    stream.write_int(42, 2, Byteorder.BIG)
    assert stream.getvalue() == b'\x00\x2a'


def test_read_int_reads_correct_value(stream):
    stream.write_int(42, 2, Byteorder.BIG)
    stream.seek(0)
    assert stream.read_int(2, Byteorder.BIG) == 42


def test_read_raw_cstring_reads_correct_value(stream):
    stream.write(b'hello\x00world\x00')
    stream.seek(0)
    assert stream.read_raw_cstring() == b'hello'


def test_write_raw_cstring_writes_correct_value(stream):
    stream.write_raw_cstring(b'hello')
    assert stream.getvalue() == b'hello\x00'


def test_read_cstring_reads_correct_value(stream):
    stream.write(b'hello\x00')
    stream.seek(0)
    assert stream.read_cstring() == 'hello'


def test_write_cstring_writes_correct_value(stream):
    stream.write_cstring('hello')
    assert stream.getvalue() == b'hello\x00'
