"""
This file is responsible for storing all publicly defined types,
and creating a type database when needed.
"""

from __future__ import annotations


class Registry:
    """
    A static class that holds all publicly
    registered data types.
    """

    def __init__(self):
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        raise NotImplementedError

    _database = dict()

    def add_type(self):...
    def remove_type(self):...





def predefined_types() -> dict[str, ...]:  # todo
    """
    Returns a collection of all predefined data types.
    # todo
    """

    return dict()     # todo



