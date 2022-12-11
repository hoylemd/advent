import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_input():
    return (line.strip() for line in fileinput.input())


class Monkey:
    def __init__(self, game, number, items, op, arg, div, true_targ, false_targ):
        self.number = number
        self.game = game
        self.items = items
        self.op = op
        self.arg = arg
        self.div = div
        self.true_targ = true_targ
        self.false_targ = false_targ

        self.inspections = 0

    def __str__(self):
        if self.op == '**':
            op_spec = '* old'
        else:
            op_spec = f"{self.op} {self.arg}"

        return '\n'.join([
            f"Monkey {self.number}:",
            f"  Starting items: {', '.join(str(i) for i in self.items)}",
            f"  Operation: new = old {op_spec}",
            f"  Test: divisible by {self.div}",
            f"    If true: throw to monkey {self.true_targ}",
            f"    If false: throw to monkey {self.false_targ}"
        ])


class Game:
    def __init__(self, notes):
        self.monkeys = []
        buffer = []
        for note in notes:
            if not note:
                self.monkeys.append(Monkey(*self.parse_monkey(buffer)))
                buffer = []
                continue
            buffer.append(note)

        # and get the last one
        self.monkeys.append(Monkey(*self.parse_monkey(buffer)))

    def parse_monkey(self, monkey_spec):
        number = int(monkey_spec[0][-2])
        items = [int(n) for n in monkey_spec[1].split(':')[1].split(', ')]
        op, arg = monkey_spec[2][21:].split()
        if arg == 'old':
            op = '**'
            arg = 2
        else:
            arg = int(arg)

        div = int(monkey_spec[3][19:])
        true_targ = int(monkey_spec[4][25:])
        false_targ = int(monkey_spec[5][26:])

        return self, number, items, op, arg, div, true_targ, false_targ

    def __str__(self):
        return '\n\n'.join(str(monkey) for monkey in self.monkeys)


if __name__ == '__main__':
    game = Game(parse_input())

    print(game)
