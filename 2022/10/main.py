import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_input():
    for line in fileinput.input():
        parts = line.strip().split()
        if len(parts) == 1:
            yield parts[0], None
            continue
        yield parts[0], int(parts[1])


class Device:
    def __init__(self):
        self.X = 1
        self.cycle = 0
        self.X_history = {}

    def exec_cycle(self):
        self.cycle += 1
        if (self.cycle + 20) % 40 == 0:
            self.X_history[self.cycle] = self.X

    def execute(self, program):
        for op, arg in program:
            debug(f"{op} {arg if arg else ''}")
            if op == 'noop':
                self.exec_cycle()
            elif op == 'addx':
                self.exec_cycle()
                self.exec_cycle()
                self.X += arg

    def sum_interesting(self):
        total = 0
        for c, v in self.X_history.items():
            total += c * v

        return total


if __name__ == '__main__':
    dev = Device()

    dev.execute(parse_input())

    debug(dev.X_history)
    print(dev.sum_interesting())
