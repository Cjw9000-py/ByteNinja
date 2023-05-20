from buffers.run_counts import *

def run():
    buf = list()

    part_ops = OPS // 10

    for i in range(ITERS):
        for _ in range(10):
            for j in range(part_ops):
                # push values
                buf.append(j)

            for j in range(part_ops):
                # pop values
                buf.pop(-1)
