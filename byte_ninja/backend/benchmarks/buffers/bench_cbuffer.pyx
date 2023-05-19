from memory.run_counts import *

cdef extern from "stdlib.h":
    void* malloc(size_t)
    void* realloc(void*, size_t)
    void free(void*)
    void memcpy(void*, void*, size_t)


ctypedef unsigned long long item_t

cdef struct buffer_t:
    void* bp
    size_t length


cdef void buffer_init(buffer_t* buf):
    buf.bp = NULL
    buf.length = 0


cdef void buffer_push(buffer_t* buf, item_t value):
    if buf.bp == NULL:
        # allocate new buffer
        buf.bp = malloc(sizeof(value))
    else:
        buf.bp = realloc(buf.bp, sizeof(value) * (buf.length + 1))

    assert buf.bp != NULL

    memcpy(buf.bp + (buf.length * sizeof(value)), &value, sizeof(value))
    buf.length += 1


cdef item_t buffer_pop(buffer_t* buf):
    assert buf.bp != NULL
    buf.length -= 1

    cdef item_t value
    memcpy(&value, buf.bp + ((buf.length + 1) * sizeof(value)), sizeof(value))

    if buf.length == 0:
        free(buf.bp)
        buf.bp = NULL
        return value

    buf.bp = realloc(buf.bp, (buf.length * sizeof(value)))
    return value



cpdef void run():
    cdef buffer_t buf
    buffer_init(&buf)
    cdef size_t part_ops = OPS // 10

    for i in range(ITERS):
        for _ in range(10):
            for j in range(part_ops):
                # push values
                buffer_push(&buf, j)

            for j in range(part_ops):
                # pop values
                buffer_pop(&buf)
