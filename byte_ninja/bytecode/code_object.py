from .sizes import *
from .stream import BufferedStream
from .codes import OperationMode, BYTECODE_BYTEORDER


class CodeObject(BufferedStream):
    def __init__(self, mode: OperationMode,
                 names: dict[int, str],
                 bytecode: bytes):

        super().__init__(bytecode)
        self.byteorder = BYTECODE_BYTEORDER

        self.operation_mode = mode
        self.name_table = names

    def read_name(self) -> str:
        """
        Reads a name number from the stream
        and looks up the name in the name table.
        """

        no = self.read_uint(QWORD, BYTECODE_BYTEORDER)

        try:
            return self.name_table[no]
        except KeyError as e:
            raise KeyError('no name with that number does exist', no) from e

    @classmethod
    def from_bytes(cls, data: bytes):
        """ Create a new code object from the given binary representation. """
        stream = BufferedStream(data)
        stream.byteorder = BYTECODE_BYTEORDER

        mode = OperationMode(stream.read_uint(BYTE))
        name_table_size = stream.read_uint(QWORD)

        names = dict()
        for i in range(name_table_size):
            names[i] = stream.read_cstring()

        return cls(mode, names, stream.read())

    def to_bytes(self) -> bytes:
        """ Parse the code object into a binary representation. """
        stream = BufferedStream()
        stream.byteorder = BYTECODE_BYTEORDER

        items = sorted(self.name_table.items(), key=lambda x: x[0])
        if [i[0] for i in items] != list(range(len(items))):
            raise ValueError('name table is not continuous')

        stream.write_uint(self.operation_mode, BYTE)
        stream.write_uint(len(items), QWORD)

        for i, n in items:
            stream.write_cstring(n)

        stream.write(self.getvalue())
        return stream.getvalue()

