import os
# from byte_ninja.backend.memory import __checker__

from libc.stdint cimport (  # noqa
    int8_t,                 # noqa
    int16_t,                # noqa
    int32_t,                # noqa
    int64_t,                # noqa
    uint8_t,                # noqa
    uint16_t,               # noqa
    uint32_t,               # noqa
    uint64_t,               # noqa
)

cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void* realloc(void* ptr, size_t size)
    void free(void* ptr)


# DEBUG_MEMORY = {
#     'yes': True,
#     'no': False,
#     'true': True,
#     'false': False,
# }[os.environ.get('BYTE_NINJA_MEMORY_DEBUG', 'no').lower()]


# memory allocation wrappers
# if DEBUG_MEMORY is true these will check memory allocation
# for memory leaks and errors


cdef inline void* malloc_s(size_t size):
    cdef void* ptr = malloc(size)

    if ptr == NULL:
        # todo advance on this
        raise MemoryError(f'could not allocate {size} bytes')

    # if DEBUG_MEMORY:
    #     __checker__.call_to_malloc(<uint64_t>ptr, size)

    return ptr


cdef inline void* realloc_s(void* ptr, size_t size):
    cdef void* new_ptr = realloc(ptr, size)

    if ptr == NULL and size != 0:
        raise MemoryError(f'could not reallocate {size} bytes at {hex(<uint64_t>ptr)}')

    # if DEBUG_MEMORY and ptr != NULL:
    #     __checker__.call_to_realloc(<uint64_t>ptr, <uint64_t>new_ptr, size)

    return new_ptr


cdef inline void free_s(void* ptr):
    free(ptr)
    #
    # if DEBUG_MEMORY:
    #     __checker__.call_to_free(<uint64_t>ptr)

