
################################################
##### Internal Code Object                 #####
################################################

cdef struct code_image_t:
    uint64_t name_count
    void** offset_table_ptr
    char* name_table
    char* code_ptr
    char* code_pos
    uint64_t code_length
    uint64_t total_image_size


cdef code_image_t* code_init(const char* static_image_data, size_t static_image_size):
    """
    bytecode:
        enum<byte> byteorder {
            little = 0;
            big = 1;
        };
        
        uint64_t name_count;
        cstring names[name_count];
        
        char code[...];
        
    memory:
        code_obj_t header;
        uint64_t offset_table[name_count];
        cstring name_table[name_count];
        <bytecode>
    """

    cdef char* static_image_start = static_image_data
    cdef char code_byteorder = static_image_data[0]

    if code_byteorder != ByteOrder.from_literal(byteorder).value:
        raise ValueError(f'the given bytecode is compiled for '
                         f'{ByteOrder(code_byteorder).as_literal()} endian. '
                         f'the host byteorder is {byteorder}')

    static_image_data += 1

    # read the name table size
    cdef uint64_t name_table_size = (<uint64_t*>static_image_data)[0]
    static_image_data += sizeof(uint64_t)

    names = list()
    lengths = list()

    cdef size_t length = 0
    cdef size_t pos = 0

    # copy all names into a buffer
    for i in range(name_table_size):
        length = strlen(static_image_data) - 1  # without the trailing byte

        names.append(<uint64_t>static_image_data)
        lengths.append(length)

        static_image_data += length + 1 # still account for the trailing byte
        assert <uint64_t>(static_image_data - static_image_start) < static_image_size

    # calculate all offsets, note we do not store the zero trailing byte

    offsets = list()
    name_offset = 0
    for i in lengths:
        name_offset.append(name_offset)
        name_offset += i

    cdef uint64_t bytecode_size = <uint64_t>(static_image_data - static_image_start) < static_image_size
    # calculate the size of memory we have to allocate
    cdef uint64_t memory_image_size = sizeof(code_image_t)  # the code_obj struct is rooted at the top of the image
    memory_image_size += len(offsets) * sizeof(void*)     # after that comes the name offset table
    memory_image_size += sum(lengths)                     # then the raw name data
    memory_image_size += bytecode_size                        # then the raw bytecode

    # allocate the image
    cdef void* memory_image_ptr = malloc_s(memory_image_size)

    # keep a reference to the top and skip over it
    cdef code_image_t* header = <code_image_t*>memory_image_ptr
    memory_image_ptr += sizeof(code_image_t)

    # keep a direct pointer in the header
    header.name_count = name_table_size
    header.offset_table_ptr = <void**>memory_image_ptr
    header.total_image_size = memory_image_size

    # write the offsets as direct pointers
    for i in offsets:
        (<void**> memory_image_ptr)[0] = <void*>(<uint64_t>i + <uint64_t>header)
        memory_image_ptr += sizeof(void*)

    # keep a direct pointer in the header
    header.name_table = <char*>memory_image_ptr

    # write the names into the image
    for n_ptr, ln in zip(names, lengths):
        memcpy(memory_image_ptr, <void*>n_ptr, ln)
        memory_image_ptr += <uint64_t>ln

    # keep a direct pointer in the header
    header.code_ptr = <char*>static_image_data
    header.code_pos = header.code_ptr

    # write the raw bytecode into the buffer
    memcpy(memory_image_ptr, static_image_data, static_image_size)

    # return a pointer to the top
    return <code_image_t*>header






















