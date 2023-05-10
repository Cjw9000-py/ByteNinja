from .token import *
from enum import IntEnum
from .codes import OPCode

# an extra node type for levels
NODE_LEVEL = max(TOKEN_TO_OPCODE.values()) + 1

class Node(list):
    def __init__(self, typ: int, *values):
        super().__init__(values)
        self.type = typ

    def __repr__(self):
        return (
            f'{self.__class__.__name__}(' 
            f'type={self.type}, '
            f'{", ".join(repr(i) for i in self)})'
        )
class PatternType(IntEnum):
    REQUIRE = 0
    BRANCH = 1
    LEVEL = 2


class SyntaxTree(list):
    def __init__(self, stack: list[Token]):
        super().__init__()

        # invert for speed and simplicity
        self.tokens = stack[::-1]

        # filter comments
        self.tokens = list(filter(
            lambda t: t.type != TOK_COMMENT,
            self.tokens
        ))

        require = lambda t: (PatternType.REQUIRE, t)
        branch = lambda opts: (PatternType.BRANCH, opts)
        level = (PatternType.LEVEL,)

        self.patterns = {
            TOK_GET: [require(TOK_NAME)],
            TOK_PUT: [require(TOK_NAME)],
            TOK_EMPTY: [require(TOK_NUMBER)],
            TOK_EDIT: [require(TOK_NUMBER)],
            TOK_FLIP: [require(TOK_NUMBER)],
            TOK_YIELD: [require(TOK_NUMBER)],
            TOK_APPEND: [require(TOK_NUMBER)],
            TOK_INDEX: [require(TOK_NUMBER)],
            TOK_FINISH: [require(TOK_NUMBER)],
            TOK_FORGET: [require(TOK_NUMBER)],
            TOK_PUSH: [require(TOK_NUMBER)],
            TOK_POP: [],
            TOK_READ: [require(TOK_NAME)],
            TOK_RARRAY: [require(TOK_NAME)],
            TOK_WRITE: [require(TOK_NAME)],
            TOK_WARRAY: [require(TOK_NAME)],
            TOK_LOOPX: [require(TOK_COLON), level],
            TOK_LOOP: [require(TOK_COLON), level],
            TOK_BREAK: [],
            TOK_TEST: [
                branch((
                    TOK_EQ,
                    TOK_NE,
                    TOK_LT,
                    TOK_GT,
                    TOK_LE,
                    TOK_GE,
                    TOK_NOT,
                )),
                require(TOK_COLON),
                level,
            ],
            TOK_RET: [],
            TOK_SEEK: [branch((
                TOK_SEEK_START,
                TOK_SEEK_REL,
                TOK_SEEK_END,
            ))],
            TOK_TELL: [],
            TOK_ENCODE: [require(TOK_NAME)],
            TOK_DECODE: [require(TOK_NAME)],
        }

        # move the global level
        # to the root of the syntax tree
        self.extend(
            self.parse_level()
        )

    def require(self, t: TokenType) -> Token:
        tok = self.tokens.pop()

        if tok.type != t:
            raise SyntaxError(
                f"expected '{TOKEN_TYPE_TO_NAME[t].lower()}' "
                f"but got {tok.value} at line {tok.lineno}"
            )

        return tok

    def branch(self, opts: tuple[TokenType]) -> Token:
        tok = self.tokens.pop()

        if tok.type not in opts:
            names = ', '.join(f"'{TOKEN_TYPE_TO_NAME[t]}'".lower() for t in opts)
            raise SyntaxError(
                f"expected any of {names} "
                f"but got {tok.value} at line {tok.lineno}"
            )

        return tok

    def parse_pattern(self, node_type: OPCode, pattern: list[tuple]) -> Node:
        node = Node(node_type)

        for sub in pattern:
            if sub[0] == PatternType.REQUIRE:
                node.append(self.require(sub[1]))
            elif sub[0] == PatternType.BRANCH:
                node.append(self.branch(sub[1]))
            elif sub[0] == PatternType.LEVEL:
                node.append(self.parse_level())

        return node

    def parse_instruction(self) -> Node:
        tok = self.tokens.pop()
        pattern = self.patterns[tok.type]

        return self.parse_pattern(
            TOKEN_TO_OPCODE[tok.type],
            pattern
        )

    def parse_level(self) -> Node:
        node = Node(NODE_LEVEL)

        while ...:
            # peek
            try:
                tok = self.tokens[-1]
            except IndexError:
                raise SyntaxError('expected an instruction but got eof')

            if tok.type in (TOK_END, TOK_EOF):
                self.tokens.pop()
                # exit the current level
                break

            node.append(
                self.parse_instruction()
            )

        return node

