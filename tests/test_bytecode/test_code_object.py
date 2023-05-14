import pytest  # noqa
from byte_ninja.bytecode.codes import OperationMode
from byte_ninja.backends.pythonic.code_object import BaseCodeObject


def test_read_name():
    # Define sample data
    mode = OperationMode.READ
    names = {0: 'foo', 1: 'bar'}
    bytecode = b'\x01\x00\x00\x00\x00\x00\x00\x00'

    # Create a code object instance
    code_obj = BaseCodeObject(mode, names, bytecode)

    # Test read_name() method
    assert code_obj.read_name() == 'bar'


def test_from_bytes_and_to_bytes():
    # Define sample data
    mode = OperationMode.WRITE
    names = {0: 'baz', 1: 'qux'}
    bytecode = b'bytecode'

    code_obj1 = BaseCodeObject(mode, names, bytecode)

    bytes_obj = code_obj1.to_bytes()
    code_obj2 = BaseCodeObject.from_bytes(bytes_obj)

    # Test the attributes of the new code object
    assert code_obj2.operation_mode == mode
    assert code_obj2.name_table == names
    assert code_obj2.getvalue() == bytecode



def test_from_bytes_with_invalid_name_table():
    # Define sample data with invalid name table
    mode = OperationMode.READ
    names = {0: 'foo', 2: 'bar'}  # name table is not continuous
    bytecode = b'bytecode'
    code_obj = BaseCodeObject(mode, names, bytecode)

    # Test that from_bytes() method raises a ValueError for invalid name table
    with pytest.raises(ValueError):
        assert code_obj.to_bytes()
