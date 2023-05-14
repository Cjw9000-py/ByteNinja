from os import environ
from pathlib import Path
from warnings import warn
from importlib import import_module


BACKEND_VARIABLE_NAME = 'BYTE_NINJA_BACKEND'
# SEARCH_PATH_VARIABLE_NAME = 'BYTE_NINJA_BACKEND_PATH'

PYTHON_BACKEND = 'pythonic'
CYTHON_BACKEND = 'native'

DEFAULT_BACKEND = PYTHON_BACKEND
# DEFAULT_SEARCH_PATH = Path(__file__).parent


EXCLUDE_NAMES = {
    'base',
    '__init__.py',
}

# __search_paths__ = {
#     DEFAULT_SEARCH_PATH,
# }
#
#
# def get_search_paths() -> set:
#     return __search_paths__
#
#
# def search_backend(name: str):
#     if name in EXCLUDE_NAMES:
#         warn(
#             f'A byte_ninja backend cannot be named "{name}". '
#             f'Please check the {BACKEND_VARIABLE_NAME} environment variable. '
#             f'Defaulting to backend {DEFAULT_BACKEND}',
#             UserWarning,
#         )
#         name = DEFAULT_BACKEND
#
#     for path in __search_paths__:
#         path = Path(path)
#         backend_path = path / name
#
#
#
#

__backend__ = environ.get(BACKEND_VARIABLE_NAME, DEFAULT_BACKEND)

if __backend__ == CYTHON_BACKEND:
    try:
        from .native import *
    except ImportError:
        warn(f'Failed to import the native backend falling back to "{PYTHON_BACKEND}"')
        __backend__ = PYTHON_BACKEND

if __backend__ == PYTHON_BACKEND:
    from .pythonic import *









