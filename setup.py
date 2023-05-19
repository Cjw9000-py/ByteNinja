from setuptools import setup

setup(
    name='ByteNinja',
    version='0.0.1-alpha',
    packages=['tests', 'tests.test_vm', 'tests.test_bytecode', 'byte_ninja', 'byte_ninja.vm', 'byte_ninja.branch', 'byte_ninja.builder', 'byte_ninja.backends', 'byte_ninja.backends.base', 'byte_ninja.backends.pythonic', 'byte_ninja.bytecode'],
    url='',
    license='MIT',
    author='Cjw9000',
    author_email='',
    description='A library for byte processing'
)
