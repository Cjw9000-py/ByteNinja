

DEF DEBUG = 1

from cpython cimport (
    PyBytes_FromString,
    PyBytes_FromStringAndSize,
)

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

cdef extern from "string.h":
    void strcpy(void*, void*)
    size_t strlen(void*)
    void memcpy(void*, void*, size_t)


from sys import byteorder
from byte_ninja.enums import ByteOrder