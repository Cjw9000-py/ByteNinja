# from .data_type import PrimitiveType
#
#
# class IntType(PrimitiveType):
#     __slots__ = 'size', 'byteorder', 'sign'
#
#     cpdef read(self, vm) -> object:
#         ...
#
#     cpdef write(self, vm, value: int):
#         assert isinstance(value, int)
#
#
# class FloatType(PrimitiveType):
#     __slots__ = 'size',
#
#     def __init__(self, size: int):
#         assert size in (4, 8)
#         self.size = size
#
#     cpdef read(self, vm) -> float:
#         ...
#
#     cpdef write(self, vm, value: float):
#         ...
#
