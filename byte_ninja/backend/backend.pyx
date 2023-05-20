include "imports.pxi"
include "memory.pxi"
include "buffer.pxi"
include "code_obj.pxi"



cdef class CodeObject:
    cdef code_image_t* memory_image

    def __init__(self, code: bytes):
        cdef size_t length = len(code)
        cdef char* c_code = <char*>malloc_s(length)

        # copy the data into the carray
        for i in range(length):
            c_code[i] = code[i]

        self.memory_image = code_init(c_code, length)
        free_s(c_code)

    cpdef bytes to_bytes(self):
        """ Read the raw memory representation. """

        cdef uint64_t size = self.memory_image.total_image_size
        return PyBytes_FromStringAndSize(<char*>self.memory_image, size)





