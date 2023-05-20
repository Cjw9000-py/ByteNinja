from __future__ import annotations

import os
from pathlib import Path
from os import environ, walk
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize


DEBUG_BUILD = {
    'yes': True,
    'no': False,
}[environ.get('BYTE_NINJA_DEBUG', 'no').lower()]

print(f'BYTE_NINJA_DEBUG={DEBUG_BUILD}')

include_dirs = [
    'byte_ninja/backend/',
    'include/',
]

source_files = [
    'byte_ninja/backend/**/*.pyx',
    # 'byte_ninja/backend/tests/*.pyx',
]

extensions = [
    Extension(
        name=source.rpartition('.')[0].split('/')[-1],
        sources=[str(source)],
        include_dirs=include_dirs,
        extra_compile_args=['-O0', '-Wno-cpp'] if DEBUG_BUILD else [],
    ) for source in source_files
]

setup(
    name='ByteNinja',
    version='0.0.1a0',
    packages=[
        'byte_ninja',
        'byte_ninja.vm',
        'byte_ninja.branch',
        'byte_ninja.builder',
        'byte_ninja.bytecode',
    ],
    url='',
    license='MIT',
    author='Cjw9000',
    author_email='',
    description='A library for byte processing',
    ext_modules=cythonize(
        module_list=extensions,
        nthreads=os.cpu_count(),
        language_level='3',
        include_path=include_dirs,
    ),

)
