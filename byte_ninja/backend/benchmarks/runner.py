from sys import argv
from pathlib import Path
from time import perf_counter
from importlib import import_module
from cProfile import Profile

from memory import (
    bench_buffer
)

suites = {
    'memory': [
        bench_buffer
    ]
}



def run_suite(suite: list, count: int, **kwargs):
    # results = dict()
    for mod in suite:
        assert hasattr(mod, 'run'), 'bench module has no run function'

        print(f'Running benchmarks for {str(mod)}')

        values = list()
        p = Profile()
        for i in range(count):
            p.enable()
            start = perf_counter()
            mod.run(**kwargs)
            end = perf_counter()
            p.disable()

            delta = end - start
            values.append(delta)

            print(f'Round {i + 1} with %.10f seconds' % delta)


        print(f'Results for {str(mod)}')
        print('Avg time %.10f seconds' % (sum(values) / len(values)))
        p.print_stats('cumtime')


if __name__ == '__main__':
    target_suite_name = argv[1]
    target_suite_count = int(argv[2])

    run_suite(suites[target_suite_name], target_suite_count)




