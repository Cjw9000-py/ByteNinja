include "common.pxi"

from .buffer cimport *

# value types that are supported by the stack
cdef enum NodeType:
    int_type_e = 0
    uint_type_e = 1
    single_type_e = 2
    double_type_e = 3
    array_type_e = 4


#### UNIONS
cdef union int_data_t:
    uint64_t uint_value
    int64_t int_value
    # todo extend this

cdef union float_data_t:
    float single_value
    double double_value


#### NODES
cdef struct int_node_t:
    uint8_t ident
    int_data_t data
    void* next

cdef struct float_node_t:
    uint8_t ident
    float_data_t data
    void* next

cdef struct array_node_t:
    uint8_t ident
    buffer_t data_ptr
    void* next


#### STACK
cdef struct stack_frame_t:
    void* bp
    void* sp

    stack_frame_t* last
    stack_frame_t* next


cdef struct stack_t:
    buffer_t int_node_buffer
    buffer_t float_node_buffer
    buffer_t array_node_buffer
    stack_frame_t* bp
    stack_frame_t* sp

    uint64_t frame_count

cdef inline stack_init(stack_t self, buffer_resolution: uint64_t):
    buffer_init(self.int_node_buffer, buffer_resolution, sizeof(int_node_t))
    buffer_init(self.float_node_buffer, buffer_resolution, sizeof(float_node_t))
    buffer_init(self.array_node_buffer, buffer_resolution, sizeof(array_node_t))

    self.bp = NULL
    self.sp = NULL
    self.frame_count = 0

cdef inline stack_frame_t* stack_push_frame(stack_t self):
    cdef stack_frame_t* ptr = <stack_frame_t*>malloc(sizeof(stack_frame_t))

    # set everything to zero
    ptr.bp = NULL
    ptr.sp = NULL
    ptr.last = NULL
    ptr.next = NULL

    # no frames inside the stack
    if self.bp == NULL:
        self.bp = ptr
    if self.sp == NULL:
        self.sp = ptr
    else:
        # if were not the only frame
        # link the frames
        ptr.last = self.sp
        self.sp.next = ptr

    # push
    self.sp = ptr
    self.frame_count += 1

    return ptr

cdef inline void stack_pop_frame(stack_t self):
    # check if there are any frames to pop
    assert self.sp != NULL

    cdef stack_frame_t* ptr = self.sp
    self.sp = ptr.last
    self.frame_count -= 1

    # check if the stack has no frames anymore
    if self.sp == NULL:
        self.bp = NULL

    # deallocate the stack

cdef inline void stack_free(stack_t self):
    ...


