import os
os.environ['BYTE_NINJA_MEMORY_DEBUG'] = 'yes'


from byte_ninja.backend.tests.ctest_buffer import ctest_buffer
from tmp.memory import check_and_clean


def test_buffer():
    ctest_buffer()
    check_and_clean()
