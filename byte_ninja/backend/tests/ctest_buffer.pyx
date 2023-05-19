# """
# This file exposes buffer_t to python
# """
#

include "common.pxi"
from tmp.buffer cimport *


cpdef int ctest_buffer() except *:
    cdef buffer_t buf
    cdef long * ptr

    buffer_init(&buf, 100, sizeof(long))

    for _ in range(10):
        buffer_expand(&buf, 1000)
        for i in range(1000):
            ptr = <long*>buffer_index(&buf, i)
            ptr[0] = i

        for i in range(1000):
            assert (<long *> buffer_index(&buf, i))[0] == i

        buffer_shrink(&buf, 1000)

    buffer_free(&buf)


