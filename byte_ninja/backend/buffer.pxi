
################################################
##### Memory Buffer                        #####
################################################

cdef struct buffer_t:
    void* bp
    uint64_t resolution  # allocation resolution
    uint64_t alloc_size  # current allocated size 0 -> 1 == 0 -> step_size
    uint64_t unit_size  # the size of every unit in this buffer (in bytes)
    uint64_t length  # how many units are stored in this buffer


cdef buffer_init(buffer_t* self, uint64_t resolution, uint64_t unit_size):
        self.resolution = resolution
        self.alloc_size = 1
        self.unit_size = unit_size
        self.length = 0

        self.bp = malloc_s(self.resolution)

cdef void buffer_manage_memory(buffer_t* self):
    cdef uint64_t val = self.alloc_size

    # calculate needed space
    self.alloc_size = self.length * self.unit_size // self.resolution + 1

    # if we don't need more space, return
    if self.alloc_size == val:
        return

    # else allocate/deallocate needed memory
    self.bp = realloc_s(self.bp, self.alloc_size * self.resolution)

    if self.bp == NULL:
        raise MemoryError('could not allocate enough memory')

cdef void* buffer_index(buffer_t* self, uint64_t value):
    """ Returns a pointer to the given index. """
    return self.bp + (value * self.unit_size)

cdef void buffer_expand(buffer_t* self, uint64_t size):
    self.length += size
    buffer_manage_memory(self)

cdef void buffer_shrink(buffer_t* self, uint64_t size):
    self.length -= size
    buffer_manage_memory(self)

cdef void buffer_free(buffer_t* self):
    if self.bp == NULL:
        return # nothing to free

    free_s(self.bp)
    self.bp = NULL
    self.length = 0
    self.alloc_size = 0

