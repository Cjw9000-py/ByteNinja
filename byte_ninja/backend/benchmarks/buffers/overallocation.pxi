from buffers.run_counts import *

from libc.stdint cimport (
    uint64_t
)

cdef extern from "stdlib.h":
    void* malloc(size_t)
    void* realloc(void*, size_t)
    void free(void*)
    void memcpy(void*, void*, size_t)


ctypedef unsigned long long item_t

cdef struct buffer_t:
    void* bp
    uint64_t resolution  # allocation resolution
    uint64_t alloc_size  # current allocated size 0 -> 1 == 0 -> step_size
    uint64_t unit_size  # the size of every unit in this buffer (in bytes)
    uint64_t length  # how many units are stored in this buffer


cdef inline buffer_init(buffer_t* self, uint64_t resolution, uint64_t unit_size):
        self.resolution = resolution
        self.alloc_size = 1
        self.unit_size = unit_size
        self.length = 0

        self.bp = malloc(self.resolution)

cdef inline void buffer_manage_memory(buffer_t* self):
    cdef uint64_t val = self.alloc_size

    # calculate needed space
    self.alloc_size = self.length * self.unit_size // self.resolution + 1

    # if we don't need more space, return
    if self.alloc_size == val:
        return

    # else allocate/deallocate needed memory
    self.bp = realloc(self.bp, self.alloc_size * self.resolution)

    if self.bp == NULL:
        raise MemoryError('could not allocate enough memory')

cdef inline void* buffer_index(buffer_t* self, uint64_t value):
    """ Returns a pointer to the given index. """
    return self.bp + (value * self.unit_size)

cdef inline void buffer_expand(buffer_t* self, uint64_t size):
    self.length += size
    buffer_manage_memory(self)

cdef inline void buffer_shrink(buffer_t* self, uint64_t size):
    self.length -= size
    buffer_manage_memory(self)

cdef inline void buffer_free(buffer_t* self):
    if self.bp == NULL:
        return # nothing to free

    free(self.bp)
    self.bp = NULL
    self.length = 0
    self.alloc_size = 0



cpdef void run_with_resolution(size_t res):
    cdef buffer_t buf
    buffer_init(&buf, res, sizeof(item_t))
    cdef size_t part_ops = OPS // 10

    for i in range(ITERS):
        for _ in range(10):
            for j in range(part_ops):
                # push values
                buffer_expand(&buf, 1)

            for j in range(part_ops):
                # pop values
                buffer_shrink(&buf, 1)
