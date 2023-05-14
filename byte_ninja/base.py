from __future__ import annotations
from abc import ABC, abstractmethod


class ListBased(list):
    """ Provides a custom object representation for classes subclassing :type list:"""

    def __str__(self):
        return repr(self)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' \
               f'{", ".join(repr(i) for i in self)})'


class FieldBased(ABC):
    """ Provides a custom object representation for specific fields. """

    @abstractmethod
    def __repr_fields__(self) -> dict:
        ...

    def __repr__(self):
        ...

