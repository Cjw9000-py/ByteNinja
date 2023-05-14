from libc.stdint cimport (
    uint8_t,
    int8_t,
    uint16_t,
    int16_t,
    uint32_t,
    int32_t,
    uint64_t,
    int64_t
)

cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void* realloc(void* ptr, size_t size)
    void free(void* ptr)
    void memcpy(void* dest, void* src, size_t size)

DEBUG_MEMORY = True


cdef union IntUnion:
    char raw[8]
    uint8_t uint8
    int8_t int8
    uint16_t uint16
    int16_t int16
    uint32_t uint32
    int32_t int32
    uint64_t uint64
    int64_t int64


cdef inline bint convert_is_native(uint64_t size):
    if size == 1: return True
    elif size == 2: return True
    elif size == 4: return True
    elif size == 8: return True
    else: return False

cdef inline int convert_int_union(IntUnion value, uint64_t size, bint sign):
    if size == 1 and sign:
        return value.int8
    elif size == 1 and not sign:
        return value.uint8
    elif size == 2 and sign:
        return value.int16
    elif size == 2 and not sign:
        return value.uint16
    elif size == 4 and sign:
        return value.int32
    elif size == 4 and not sign:
        return value.uint32
    elif size == 8 and sign:
        return value.int64
    elif size == 8 and not sign:
        return value.uint64
    else:
        raise TypeError


cdef int nullptr = 0