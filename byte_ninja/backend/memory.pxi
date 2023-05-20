
################################################
##### Memory Management                    #####
################################################

IF DEBUG == 1:
    allocations = dict()

cdef void* malloc_s(size_t size) except *:
    cdef void* ptr = malloc(size)

    if ptr == NULL:
        # todo advance on this
        raise MemoryError(f'could not allocate {size} bytes')

    IF DEBUG == 1:
        assert size != 0, 'malloc called with zero size'
        assert ptr != NULL, 'malloc returned nullptr'

        allocations[<long>ptr] = size

    return ptr

cdef void* realloc_s(void* ptr, size_t size) except *:
    cdef bint ptr_was_null = ptr == NULL  # we are doing this to omit warnings
    cdef size_t cpy = <size_t> ptr

    IF DEBUG == 1:
        assert ptr == NULL or <long> ptr in allocations, 'realloc called with unknown pointer'
        del allocations[<long> ptr]


    cdef void * new_ptr = realloc(ptr, size)
    if ptr_was_null and size != 0:
        raise MemoryError(f'could not reallocate {size} bytes at {hex(<uint64_t>cpy)}')

    IF DEBUG == 1:
        assert <long>new_ptr not in allocations, 'realloc called with new_ptr that is already registered'

        if ptr_was_null:
            # new allocation is made
            assert size != 0, 'realloc called with nullptr and zero size'
            assert new_ptr != NULL, 'realloc returned nullptr while prev_ptr was null'
            allocations[<long>new_ptr] = size
            return new_ptr

        if size == 0:
            # memory is completely freed

            return new_ptr

        # memory is resized
        assert new_ptr != NULL, 'realloc returned nullptr while prev_ptr was known'
        allocations[<long>new_ptr] = size

    return new_ptr


cdef void free_s(void* ptr) except *:
    IF DEBUG == 1:
        assert ptr != NULL, 'free called with nullptr'
        assert <long>ptr in allocations, 'free called with unknown pointer'

        del allocations[<long>ptr]

    free(ptr)

