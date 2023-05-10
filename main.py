from assembler import *
from minimal import *


source = """
# hello
push 2
put name
push 42
put age
ret
"""

bytecode = Assembler().assemble(source)
print(bytecode)
print('#' * 30)
print(Assembler.disassemble(bytecode))

class CustomType(ComplexType):
    def empty(self) -> dict:
        return {
            'name': ...,
            'age': ...,
        }


db = get_database()
db['custom'] = CustomType(None, None)

stream = BytesIO(b'fuck me\x00*\x00')
vm = VirtualMachine(db, DataStream(stream, OperationMode.READ))
res = vm.run(CodeObject.from_bytes(bytecode), db['custom'].empty())
print(res)
