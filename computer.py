class Computer:
    tape: list[tuple[str, ...]]
    ip: int
    x: int

    def __init__(self, tape: str, x: int = 1):
        self.tape = list(map(lambda i: tuple(i.split()), tape.splitlines()))
        self.ip = 0
        self.x = x

    def addx(self, n: int):
        yield self
        yield self
        self.x += n

    def noop(self):
        yield self

    def run(self):
        while self.ip < len(self.tape):
            instruction, *args = self.tape[self.ip]
            self.ip += 1
            yield from getattr(self, instruction)(*map(int, args))

    def copy(self):
        out = Computer("", self.x)
        out.tape = self.tape.copy()
        out.ip = self.ip
        return out
