import fileinput

DEBUG = False  # True
INFO = False  # True


def info(*args):
    if INFO: print(*args)


def debug(*args):
    if DEBUG: print(*args)

# TODO add basic logging
# TODO autopep8


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
        self.t_insps = 0
        self.f_insps = 0

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

    def perform_op(self, item):
        match self.op:
            case '+':
                worry = item + self.arg
                debug(f"    Worry level increases by {self.arg} to {worry}")
            case '*':
                worry = item * self.arg
                debug(f"    Worry level is multiplied by {self.arg} to {worry}")
            case '**':
                worry = item ** 2
                debug(f"    Worry level is multiplied by itself to {worry}")

        return worry

    def inspect(self, item):
        self.inspections += 1
        debug(f"  Monkey inspects an item with a worry level of {item}.")

        return self.perform_op(item)

    def throw(self, item):
        if item % self.div == 0:
            self.t_insps += 1
            targ = self.true_targ
            div_state = ''
        else:
            self.f_insps += 1
            targ = self.false_targ
            div_state = ' not'

        debug(f"    Current worry level is{div_state} divisible by {self.div}.")
        debug(f"    Item with worry level {item} is thrown to monkey {targ}.")
        self.game.monkeys[targ].items.append(item)

    def take_turn(self):
        for item in self.items:
            worry = self.inspect(item)
            proj = worry % self.game.worry_limit
            if (worry != proj): info(f"    Worry Limit Exceeded ({worry}%{self.game.worry_limit}={proj}")
            self.throw(proj)

        self.items = []


class Game:
    def __init__(self, notes):
        self.monkeys = []
        buffer = []
        self.worry_limit = 1
        for note in notes:
            if not note:
                self.parse_monkey(buffer)
                buffer = []
                continue
            buffer.append(note)

        # and get the last one
        self.parse_monkey(buffer)
        info(f"Worry limit is {self.worry_limit}({'*'.join(str(m.div) for m in self.monkeys)})")

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

        monkey = Monkey(self, number, items, op, arg, div, true_targ, false_targ)
        self.monkeys.append(monkey)
        self.worry_limit *= monkey.div
        return monkey

    def __str__(self):
        return '\n\n'.join(str(monkey) for monkey in self.monkeys)

    def sim_round(self):
        for monkey in self.monkeys:
            debug(f"Monkey {monkey.number}:")
            monkey.take_turn()

    def summarize_monkeys(self):
        lines = (
            f"  Monkey {m.number} inspected items {m.inspections} times. ({m.t_insps}/{m.f_insps})"
            f"({','.join(str(i) for i in m.items)})"
            for m in self.monkeys
        )
        return '\n'.join(lines)

    def simulate(self, rounds):
        for i in range(rounds):
            info()
            info(f"Round {i}:    (limit:{self.worry_limit})")
            self.sim_round()
            info(self.summarize_monkeys())

    def monkey_business(self):
        top, sec = sorted([m.inspections for m in self.monkeys])[-1:-3:-1]
        return top * sec


if __name__ == '__main__':
    game = Game(parse_input())

    rounds = 10_000

    breakpoint()
    game.simulate(rounds)

    print(game.monkey_business())
