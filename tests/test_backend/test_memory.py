import pytest
from byte_ninja.backend.memory import MemoryChecker


def test_memory_no_leak():
    checker = MemoryChecker()

    for i in range(1, 1000):
        checker.call_to_malloc(i, i * 10)

    for i in range(1, 1000):
        checker.call_to_realloc(i, i + 1000, i * 100)

    for i in range(1 + 1000, 1000 + 1000):
        checker.call_to_free(i)

    checker.check_allocations()


def test_memory_leak():
    checker = MemoryChecker()

    for i in range(1, 1000):
        checker.call_to_malloc(i, i * 10)

    for i in range(1, 1000):
        checker.call_to_realloc(i, i + 1000, i * 100)

    for i in range(1 + 1000, 1000 + 1000 - 10):  # 10 memory leaks
        checker.call_to_free(i)

    with pytest.raises(MemoryError):
        checker.check_allocations()
