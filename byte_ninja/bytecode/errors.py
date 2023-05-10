# from abc import ABC, abstractmethod
# from .token import TokenType, TOKEN_TYPE_TO_NAME, Token
#
# class ParsingSyntaxError(Exception, ABC):
#     @abstractmethod
#     def pretty(self) -> str:
#         ...
#
#
# class LexerSyntaxError(ParsingSyntaxError):
#     def __init__(self, msg: str, rem_source: str):
#         self.msg = msg
#         self.rem_source = rem_source
#
#     def pretty(self) -> str:
#         return f"{self.msg}: '{self.rem_source}'"
#
#
# class SyntaxTreeError(ParsingSyntaxError):
#     def __init__(self, msg: str, expected: TokenType, actual: Token):
#         self.msg = msg
#         self.expected = expected
#         self.actual = actual
#
#     def pretty(self) -> str:
#         return f"{self.msg}: '{self.rem_source}'"
