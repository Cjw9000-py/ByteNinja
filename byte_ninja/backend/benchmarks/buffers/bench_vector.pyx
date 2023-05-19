# distutils: language = c++
from libcpp.vector cimport vector



from memory.run_counts import *


cpdef void run():
    cdef vector[unsigned long long] buf
    cdef size_t part_ops = OPS // 10

    for i in range(ITERS):
        for _ in range(10):
            for j in range(part_ops):
                # push values
                buf.push_back(j)

            for j in range(part_ops):
                # pop values
                buf.pop_back()
