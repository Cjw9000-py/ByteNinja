
class MemoryChecker:
    def __init__(self):
        self.allocations = dict()

    def call_to_malloc(self, ptr: int, size: int):
        assert size != 0, 'malloc called with zero size'
        assert ptr != 0, 'malloc returned nullptr'

        self.allocations[ptr] = size

    def call_to_realloc(self, prev_ptr: int, new_ptr: int, size: int):
        assert prev_ptr == 0 or prev_ptr in self.allocations, 'realloc called with unknown pointer'
        assert new_ptr not in self.allocations, 'realloc called with new_ptr that is already registered'

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

    def call_to_free(self, ptr: int):
        assert ptr != 0, 'free called with nullptr'
        assert ptr in self.allocations, 'free called with unknown pointer'

        del self.allocations[ptr]

    def get_allocations(self):
        return self.allocations

    def check_allocations(self):
        """ Check if any memory has leaked. """
        if not self.allocations:
            # everything was freed
            return

        errors = list()
        for ptr, size in self.allocations.items():
            errors.append(f'memory leak at {hex(ptr)} of size {size}')

        self.allocations.clear()
        raise MemoryError('memory was leaked\n' + '\n'.join(errors))

    # def clean_memory_leaks(self):
    #     """ Free all leaked memory. """
    #
    #     for ptr, size in self.allocations.items():
    #         print('FREEING', hex(<long>ptr))
    #         free(<void*>ptr)
    #
    #     self.allocations.clear()

__checker__ = MemoryChecker()

def check_and_clean():
    global __checker__
    try:
        __checker__.check_allocations()
    finally:
        __checker__ = MemoryChecker()




