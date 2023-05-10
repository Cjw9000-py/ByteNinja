import re
from math import inf
from io import BytesIO
from minimal import (
    Instruction,
    TestOperation,
    CodeObject,
    SeekMode,
    QWORD,
    DWORD,
    WORD,
    BYTE,
    CODE_BYTEORDER,
)

class Lexer:
    def __init__(self):
        exact = [
            ('GET', 'get'),
            ('PUT', 'put'),
            ('EMPTY', 'empty'),
            ('EDIT', 'edit'),
            ('FLIP', 'flip'),
            ('YIELD', 'yield'),
            ('APPEND', 'append'),
            ('INDEX', 'index'),
            ('FINISH', 'finish'),
            ('FORGET', 'forget'),
            ('PUSH', 'push'),
            ('POP', 'pop'),
            ('READ', 'read'),
            ('WRITE', 'write'),
            ('LOOPX', 'loopx'),
            ('LOOP', 'loop'),
            ('BREAK', 'break'),
            ('TEST', 'test'),
            ('RET', 'ret'),
            ('SEEK', 'seek'),
            ('TELL', 'tell'),
            ('DO', 'do'),
            ('END', 'end'),
            ('EQ', 'EQ'),
            ('NE', 'NE'),
            ('LT', 'LT'),
            ('GT', 'GT'),
            ('LE', 'LE'),
            ('GE', 'GE'),
            ('NOT', 'NOT'),
            ('REL', 'REL'),
            ('START', 'START'),
            ('END', 'END'),
        ]

        complex_tokens = [
            ('NUMBER', re.compile(r'^[0-9]+')),
            ('NAME', re.compile(r'^\w+')),
            ('COMMENT', re.compile(r'^#[^\n]+')),
        ]

        self.tokens = [(n, re.compile(rf'^{re.escape(v)}\W')) for n, v in exact]
        self.tokens += complex_tokens

    def tokenize(self, source: str) -> list[tuple[str, str]]:
        whitespace = re.compile(r'^[\t\r\n ]*')
        stack = list()

        while source:
            m = whitespace.match(source)
            source = source[m.span()[-1]:]

            if not source:
                break

            for name, token in self.tokens:
                m = token.match(source)

                if m is None:
                    continue

                source = source[m.span()[-1]:]
                stack.append((name, m.group()))
                break
            else:
                raise SyntaxError(f'invalid syntax {repr(source)}')

        return stack

TOKEN_TO_OPCODE = {
    'GET': Instruction.GET,
    'PUT': Instruction.PUT,
    'EMPTY': Instruction.EMPTY,
    'EDIT': Instruction.EDIT,
    'FLIP': Instruction.FLIP,
    'YIELD': Instruction.YIELD,
    'APPEND': Instruction.APPEND,
    'INDEX': Instruction.INDEX,
    'FINISH': Instruction.FINISH,
    'FORGET': Instruction.FORGET,
    'PUSH': Instruction.PUSH,
    'POP': Instruction.POP,
    'READ': Instruction.READ,
    'WRITE': Instruction.WRITE,
    'LOOP': Instruction.LOOP,
    'LOOPX': Instruction.LOOPX,
    'SEEK': Instruction.SEEK,
    'TELL': Instruction.TELL,
    'BREAK': Instruction.BREAK,
    'TEST': Instruction.TEST,
    'RET': Instruction.RET,
}

TOKEN_TO_MODE = {
    'REL': SeekMode.REL,
    'START': SeekMode.START,
    'END': SeekMode.END,
}


def token_from_opcode(opcode: int) -> str:
    for name, op in TOKEN_TO_OPCODE.items():
        if op == opcode:
            return name.lower()


def token_from_mode(mode: int) -> str:
    for name, op in TOKEN_TO_MODE.items():
        if op == mode:
            return name.lower()


TOKEN_TO_OPERATION = {
    'EQ': TestOperation.EQ,
    'NE': TestOperation.NE,
    'LT': TestOperation.LT,
    'GT': TestOperation.GT,
    'LE': TestOperation.LE,
    'GE': TestOperation.GE,
    'NOT': TestOperation.NOT,
}


class Node(list):
    def __init__(self, typ: int, *values):
        super().__init__(values)
        self.type = typ


class SyntaxTree(list):
    def parse(self, stack: list[tuple[str, str]]):
        # strip comments
        stack = list(filter(lambda t: t[0] != 'COMMENT', stack))[::-1]

        def require(name: str) -> tuple:
            tok = stack.pop()

            if tok[0] != name:
                raise SyntaxError(f'expected {name}: {tok[1]}')

            return tok

        level_stack = [(None, list())]

        def append(value):
            nonlocal level_stack
            level_stack[-1][1].append(value)  # noqa

        # parse nodes
        while stack:
            inst = stack.pop()

            if inst[0] in (
                'GET',
                'PUT',
                'READ',
                'WRITE',
            ):
                append(
                    Node(
                        TOKEN_TO_OPCODE[inst[0]],
                        inst, require('NAME')
                    )
                )

            # instructions that only need a number
            elif inst[0] in (
                'EMPTY',
                'EDIT',
                'FLIP',
                'YIELD',
                'APPEND',
                'FINISH',
                'FORGET',
                'PUSH',
            ):
                append(
                    Node(
                        TOKEN_TO_OPCODE[inst[0]],
                        inst, require('NUMBER')
                    )
                )

            # instructions that have no arguments
            elif inst[0] in (
                'POP',
                'BREAK',
                'RET',
                'TELL',
            ):
                append(
                    Node(
                        TOKEN_TO_OPCODE[inst[0]],
                        inst,
                    )
                )

            elif inst[0] == 'SEEK':
                append(
                    Node(
                        TOKEN_TO_OPCODE[inst[0]],
                        inst,
                    )
                )

            elif inst[0] == 'INDEX':
                append(
                    Node(
                        Instruction.INDEX,
                        inst,
                        require('NUMBER'),
                        require('NUMBER'),
                    )
                )

            elif inst[0] in ('LOOP', 'LOOPX'):
                node = Node(
                    TOKEN_TO_OPCODE[inst[0]],
                    inst,
                    require('DO'),
                )

                append(node)
                level_stack.append((
                    node, list()
                ))

            elif inst[0] == 'TEST':
                node = Node(
                    Instruction.TEST,
                    inst,
                )

                token = stack.pop()
                options = (
                    'EQ',
                    'NE',
                    'LT',
                    'GT',
                    'LE',
                    'GE',
                    'NOT',
                )

                if token[0] not in options:
                    raise SyntaxError(
                        f'expected any of {", ".join(options)}: {token[1]}'
                    )

                node.append(token)
                node.append(require('DO'),)

                append(node)
                level_stack.append((
                    node, list()
                ))

            elif inst[0] == 'END':
                # close the current level
                target, nodes = level_stack.pop()
                target.extend(nodes)

            else:
                raise SyntaxError(f'unexpected token: {inst[1]}')

        if len(level_stack) > 1:
            raise SyntaxError('not all frames where close with an "end" stmt')

        assert level_stack, 'expected a global level'
        assert level_stack[0][0] is None

        self.extend(level_stack[0][1])  # noqa


class Assembler:
    def __init__(self):
        self.names = list()
        self.tokens = None
        self.tree = SyntaxTree()
    #
    # def parse_name(self, line: str) -> tuple[bytes, str]:
    #     line = line.strip()
    #     m = re.match(r'^\w+', line)
    #
    #     if not m:
    #         raise SyntaxError('expected a name', line)
    #
    #     index = len(self.names)
    #     self.names.append(m.group())
    #     return index.to_bytes(QWORD, CODE_BYTEORDER), m.string
    #
    # @staticmethod
    # def parse_number(line: str, size: int) -> tuple[bytes, str]:
    #     line = line.strip()
    #     m = re.match(r'^[0-9]+', line)
    #
    #     if not m:
    #         raise SyntaxError('expected a number', line)
    #
    #     return int(m.group()).to_bytes(size, CODE_BYTEORDER), m.string
    #
    # def parse_name_inst(self, line: str) -> bytes:
    #     return self.parse_name(line)[0]
    #
    # def parse_array_inst(self, line: str) -> bytes:
    #     return self.parse_number(line, WORD)[0]
    #
    # def parse_index(self, line: str) -> bytes:
    #     first, line = self.parse_number(line, QWORD)
    #     second, line = self.parse_number(line, WORD)
    #     return first + second
    #
    # def parse_push(self, line: str) -> bytes:
    #     return self.parse_number(line, QWORD)[0]
    #
    # def parse_indented(self, lines: list[str]) -> tuple[bytes, int]:
    #     indented = list()
    #     for line in lines:
    #         if line.startswith('\t'):
    #             indented.append(line[1:])
    #         elif line.startswith('\t'):
    #             indented.append(line[4:])
    #         else:
    #             break
    #
    #     for line in indented:
    #         self.parse_instruction()
    #
    #
    #
    #
    #
    # def parse_loop(self, lines: list[str]) -> bytes:
    #     lines[0] = lines[0].strip()
    #
    #     if not lines[0].startswith(':'):
    #         raise SyntaxError('expected ":"', lines[0])
    #
    #     return self.parse_indented(lines[1:])
    #
    # def parse_loopx(self, lines: list[str]) -> bytes:
    #     lines[0] = lines[0].strip()
    #
    #     if not lines[0].startswith(':'):
    #         raise SyntaxError('expected ":"', lines[0])
    #
    #     data = self.parse_number(lines[0], QWORD)[0]
    #
    #     return self.parse_indented(lines[1:]) + data
    #
    # @staticmethod
    # def parse_test(line: list[str]) -> bytes:
    #     line = line.strip()
    #     op_map = {
    #         TestOperation.EQ: 'EQ',
    #         TestOperation.NE: 'NE',
    #         TestOperation.LT: 'LT',
    #         TestOperation.GT: 'GT',
    #         TestOperation.LE: 'LE',
    #         TestOperation.GE: 'GE',
    #         TestOperation.NOT: 'NOT',
    #     }
    #
    #     for op, v in op_map.items():
    #         if line.startswith(v):
    #             return op.to_bytes(BYTE, CODE_BYTEORDER)
    #
    #     raise SyntaxError('invalid operation', line)
    #
    # def parse_instruction(self, lines: list[str]):
    #     nop = lambda ln: ...
    #     procs = {
    #         'get': (self.parse_name_inst, Instruction.GET),
    #         'put': (self.parse_name_inst, Instruction.PUT),
    #         'empty': (self.parse_array_inst, Instruction.EMPTY),
    #         'edit': (self.parse_array_inst, Instruction.EDIT),
    #         'flip': (self.parse_array_inst, Instruction.FLIP),
    #         'yield': (self.parse_array_inst, Instruction.YIELD),
    #         'append': (self.parse_array_inst, Instruction.APPEND),
    #         'index': (self.parse_index, Instruction.INDEX),
    #         'finish': (self.parse_array_inst, Instruction.FINISH),
    #         'forget': (self.parse_array_inst, Instruction.FORGET),
    #         'push': (self.parse_push, Instruction.PUSH),
    #         'pop': (nop, Instruction.POP),
    #         'read': (self.parse_name_inst, Instruction.READ),
    #         'write': (self.parse_name_inst, Instruction.WRITE),
    #         'loop': (self.parse_loop, Instruction.LOOP),
    #         'loopx': (self.parse_loopx, Instruction.LOOPX),
    #         'break': (nop, Instruction.BREAK),
    #         'test': (self.parse_test, Instruction.TEST),
    #         'ret': (nop, Instruction.RET),
    #     }
    #
    #     for name, (proc, op) in procs.items():
    #         if lines[0].startswith(name):
    #             data = op.to_bytes(
    #                 BYTE,
    #                 CODE_BYTEORDER,
    #             )
    #
    #             line = lines[0][len(name):]
    #             lines[0] = line
    #
    #             if name in (
    #                 'loop',
    #                 'loopx',
    #                 'test',
    #             ):
    #                 data += proc(lines)
    #             else:
    #                 data += proc(lines[0])
    #
    #     raise SyntaxError('invalid instruction', lines[0])

    def assemble_name_table(self) -> bytes:
        data = len(self.names).to_bytes(QWORD, CODE_BYTEORDER)

        parts = list()
        for name in self.names:
            parts.append(
                name.encode('utf8') + b'\x00'
            )

        return data + b''.join(parts)

    def register_name(self, name: str) -> bytes:
        assert isinstance(name, str)

        index = len(self.names)
        self.names.append(name)
        return index.to_bytes(QWORD, CODE_BYTEORDER)

    def translate(self, nodes: list[Node]) -> bytes:
        parts = list()

        get_val = lambda t: t[1]

        for node in nodes:
            if node[0][0] in (
                'GET',
                'PUT',
                'READ',
                'WRITE',
            ):

                parts.extend((
                    node.type.to_bytes(BYTE, CODE_BYTEORDER),
                    self.register_name(get_val(node[1])),
                ))

            elif node[0][0] in (
                'EMPTY',
                'EDIT',
                'FLIP',
                'YIELD',
                'APPEND',
                'FINISH',
                'FORGET',
            ):
                parts.extend((
                    node.type.to_bytes(BYTE, CODE_BYTEORDER),
                    int(get_val(node[1])).to_bytes(WORD, CODE_BYTEORDER),
                ))

            elif node[0][0] == 'PUSH':
                parts.extend((
                    node.type.to_bytes(BYTE, CODE_BYTEORDER),
                    int(get_val(node[1])).to_bytes(QWORD, CODE_BYTEORDER),
                ))

            elif node[0][0] in (
                'POP',
                'BREAK',
                'RET',
                'TELL',
                'SEEK',
            ):
                parts.append(
                    node.type.to_bytes(BYTE, CODE_BYTEORDER)
                )
            elif node[0][0] == 'INDEX':
                parts.extend((
                    node.type.to_bytes(BYTE, CODE_BYTEORDER),
                    int(get_val(node[1])).to_bytes(WORD, CODE_BYTEORDER),
                    int(get_val(node[2])).to_bytes(WORD, CODE_BYTEORDER),
                ))


            elif node[0][0] in ('LOOP', 'LOOPX'):
                parts.extend((
                    node.type.to_bytes(BYTE, CODE_BYTEORDER),
                    (len(node) - 3).to_bytes(QWORD, CODE_BYTEORDER),
                    self.translate(node[2:]),
                ))

            elif node[0][0] == 'TEST':
                parts.extend((
                    node.type.to_bytes(BYTE, CODE_BYTEORDER),
                    int(
                        TOKEN_TO_OPERATION[node[1][0]]
                    ).to_bytes(BYTE, CODE_BYTEORDER),
                    (len(node) - 3).to_bytes(QWORD, CODE_BYTEORDER),
                    self.translate(node[3:]),
                ))

            elif node[0][0] == 'END':
                # ignore
                ...

        return b''.join(parts)

    def assemble(self, source: str) -> bytes:
        self.tokens = Lexer().tokenize(source)
        self.tree.clear()
        self.tree.parse(self.tokens)

        bytecode = self.translate(self.tree)
        nt_data = self.assemble_name_table()
        return nt_data + bytecode

    @classmethod
    def disassemble_instructions(cls, code: CodeObject, size: int = inf) -> list[str]:
        lines = list()

        def indent(n: list[str]):
            return [
                ' ' * 4 + i for i in n
            ]

        count = 0
        while count < size and not code.eof:
            op = code.read_int(BYTE)

            if op in (
                Instruction.GET,
                Instruction.PUT,
                Instruction.READ,
                Instruction.WRITE,
            ):
                name = code.read_name()
                lines.append(f'{token_from_opcode(op)} {name}')

            elif op in (
                Instruction.EMPTY,
                Instruction.EDIT,
                Instruction.FLIP,
                Instruction.YIELD,
                Instruction.INDEX,
                Instruction.APPEND,
                Instruction.FINISH,
                Instruction.FORGET,

            ):
                no = code.read_int(WORD)
                lines.append(f'{token_from_opcode(op)} {no}')

            elif op == Instruction.PUSH:
                no = code.read_int(QWORD)
                lines.append(f'{token_from_opcode(op)} {no}')

            elif op in (
                Instruction.POP,
                Instruction.BREAK,
                Instruction.RET,
                Instruction.TELL,
                Instruction.SEEK,
            ):
                lines.append(token_from_opcode(op))

            elif op in (
                Instruction.LOOP,
                Instruction.LOOPX,
            ):
                inst_count = code.read_int(QWORD)
                lines.append(f'{token_from_opcode(op)} do')
                lines.extend(
                    indent(
                        Assembler.disassemble_instructions(code, inst_count)
                    )
                )
                lines.append('end')

            elif op == Instruction.TEST:
                operation = code.read_int(BYTE)
                inst_count = code.read_int(QWORD)

                tok = None
                for tok, val in TOKEN_TO_OPERATION.items():
                    if operation == val:
                        break

                assert tok is not None


                lines.append(f'{token_from_opcode(op)} {tok} do')
                lines.extend(
                    indent(
                        Assembler.disassemble_instructions(code, inst_count)
                    )
                )
                lines.append('end')
            else:
                assert False

            count += 1
        return lines

    @classmethod
    def disassemble(cls, bytecode: bytes) -> str:
        code = CodeObject.from_bytes(bytecode)

        lines = cls.disassemble_instructions(code)
        return '\n'.join(lines)

