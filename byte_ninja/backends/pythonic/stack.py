from byte_ninja.base import ListBased


class StackFrame(ListBased):
    @property
    def top(self):
        return self[-1]

    def push(self, value: object):
        self.append(value)

    def pop(self, index=-1) -> object:
        return super().pop(index)


class Stack(ListBased):
    class NoStackFramesError(Exception):
        ...

    def _check_empty(self):
        if len(self) == 0:
            raise self.NoStackFramesError

    def push_frame(self, frame: StackFrame = None):
        self.append(frame or StackFrame())

    def pop_frame(self) -> StackFrame:
        self._check_empty()
        return super().pop(-1)

    def push(self, value: object):
        self._check_empty()
        self[-1].append(value)

    def pop(self, index=-1) -> object:
        self._check_empty()
        return self[-1].pop()

    @property
    def top(self):
        return self[-1].top
