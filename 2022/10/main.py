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


LINE_WIDTH = 40


class Device:
    def __init__(self):
        self.X = 1
        self.cycle = 0
        self.lines = [[]]
        self.line = self.lines[0]

    def exec_cycle(self):
        # draw pixel
        x_targ = self.cycle % 40
        self.line.append('#' if abs(x_targ - self.X) < 2 else '.')

        # go to next row
        if x_targ == LINE_WIDTH - 1:
            self.lines.append([])
            self.line = self.lines[-1]

        self.cycle += 1

    def execute(self, program):
        for op, arg in program:
            debug(f"{op} {arg if arg else ''}")
            if op == 'noop':
                self.exec_cycle()
            elif op == 'addx':
                self.exec_cycle()
                self.exec_cycle()
                self.X += arg

    def render(self):
        return '\n'.join(''.join(c for c in line) for line in self.lines)


if __name__ == '__main__':
    dev = Device()

    dev.execute(parse_input())

    print(dev.render())
