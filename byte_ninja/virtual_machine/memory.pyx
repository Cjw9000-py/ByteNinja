include "types.pxi"


cdef class MemoryChecker:
    cdef dict allocations

    def __init__(self):
        self.allocations = dict()

    cpdef void call_to_malloc(self, uint64_t ptr, uint64_t size):
        assert size != 0, 'malloc called with zero size'
        assert ptr != 0, 'malloc returned nullptr'

        self.allocations[ptr] = size

    cpdef void call_to_realloc(self, uint64_t prev_ptr, uint64_t new_ptr, uint64_t size):
        assert prev_ptr != 0 and prev_ptr not in self.allocations, 'realloc called with unknown pointer'

        if prev_ptr == 0:
            # new allocation is made
            assert size != 0, 'realloc called with nullptr and zero size'
            assert new_ptr != 0, 'realloc returned nullptr while prev_ptr was null'
            self.allocations[new_ptr] = size
            return

        if size == 0:
            # memory is completely freed
            del self.allocations[prev_ptr]
            return

        # memory is resized
        assert new_ptr != 0, 'realloc returned nullptr while prev_ptr was known'
        del self.allocations[prev_ptr]
        self.allocations[new_ptr] = size

    cpdef void call_to_free(self, uint64_t ptr):
        assert ptr != 0, 'free called with nullptr'
        assert ptr in self.allocations, 'free called with unknown pointer'

        del self.allocations[ptr]

    cpdef dict get_allocations(self):
        return self.allocations








