from argparse import ArgumentParser
from utils import logger, parse_input, Point, noop, find_cycle

DEBUG = True


class Rock:
    def __init__(self, label: str, index: int, spec: list[str]):
        self.label = label
        self.idx = index
        self.width = len(spec[0])
        self.height = len(spec)
        self.lines = spec
        self.rows = [  # produce tuples of (offset, # of rock pieces)
            (line.index('#'), line.count('#'), label * len(line.strip()))
            for line in spec
        ]

        rock_lines = []
        for offset, width, _ in self.rows:
            r_margin = 5 - self.width
            if width < self.width:
                r_margin += self.width - (offset + width)
            rock_lines.append(f"|  {' ' * offset}{'@' * width}{' ' * r_margin}|")

        empty_lines = ['|       |'] * 3

        self.new_lines = [line for line in reversed(rock_lines)] + empty_lines

    def __repr__(self):
        return f"<Rock:{self.lines[0]}>"

    def __str__(self):
        return '\n'.join(self.new_lines)


# inverted for easier rendering etc
rock_sequence = {
    '-': Rock('-', 0, ['####']),  # 4 possible x outcomes * 9
    '+': Rock('+', 1, [          # 5 possible x outcomes * 9
        ' # ',
        '###',
        ' # '
    ]),
    'L': Rock('L', 2, [          # 5 possible x outcomes * 9
        '###',
        '  #',
        '  #'
    ]),
    'I': Rock('I', 3, [          # 7 possible x outcomes * 9
        '#',
        '#',
        '#',
        '#'
    ]),
    'o': Rock('o', 4, [          # 6 possible x outcomes * 9
        '##',
        '##'
    ])
}
rock_idx = [r for r in rock_sequence.values()]


SPAWN_OFFSET = Point(2, 3)


def encode_rock(rock: Rock, x: int, y: int):
    """Encode a rock outcome into an integer for easier analysis

    :param Rock rock: The Rock object to be encoded
    :param int x: the final x-displacement of the rock
    :param int y: the final y-displacement of the rock

    :return int: The encoded rock outcome
    """
    rock_comp = rock.idx << (5 + 3) # <8 options, 3 bits
    x_comp = x << 5                 # <8 options, 3 bits
    y_comp = y                      # <32 options, 5 bits
    return rock_comp | x_comp | y_comp


def decode_rock(code: int):
    """Decode a rock code into it's components

    :param int code: The integer code for this rock outcome

    :return tuple[Rock, int, int]: The Rock, and it's final x and y displacements
    """
    y = code & 0b11111              # first 5 bits (from right)
    x = (code >> 5) & 0b111         # next 3 bits
    idx = (code >> 5 + 3) & 0b111   # last 3 bits

    return rock_idx[idx], x, y


def measure_rocks(rocks: list[tuple[Rock, int, int]]):
    height = 0
    for rock, _, y in rocks:
        height += max(0, rock.height - y)
    return height

class Cave:
    def __init__(self, lines, part=1, width=7):
        self.part = part
        self.jets = self.parse(lines)
        self.width = width
        self.rows = []
        self.masks = []
        self.rocks = []
        self.preamble = None  # will be (# rocks before repeats begin, height before repeats begin)
        self.cycle = None  # will be (# rocks/cycle, height of the cycle)

    @property
    def height(self):
        return len(self.rows)

    def render_spec(self):
        return self.jet_spec

    def parse(self, lines):
        self.jet_spec = [line.strip() for line in lines][0]
        self.jets_mod = len(self.jet_spec)
        return [-1 if c == '<' else 1 for c in self.jet_spec]

    def render(self, rows=None):
        if rows is None:
            start = 0
        else:
            start = -rows
        return reversed(([f"+{'-' * self.width}+"] + [
            f'|{r}|' for r in self.rows[start:]
        ]))

    def __str__(self):
        lines = self.render()
        return '\n'.join(lines) if lines else ''

    def top_n_rows(self, rows):
        return '\n'.join(self.render(rows))

    def rock_specs(self):
        seen_ys = {label: set() for label in rock_sequence.keys()}
        with open('rocks.txt', 'w') as fp:
            for rock, x, y in self.rocks:
                seen_ys[rock.label].add(y)
                fp.write(f"{rock.label},{x},{y}\n")

        n_states = 0
        for label, ys in seen_ys.items():
            rock = rock_sequence[label]
            total_possibilities = max(ys) * (7 - rock.width)
            print(f"Max y seen for {label}: {max(ys)}, possible x outcomes: {7 - rock.width} {total_possibilities=}")
            n_states += total_possibilities

        print(f"Total possible outcomes: {n_states} (from simulating {len(self.rocks)} rocks)")

    def analyze_specs(self):
        # convert specs into an int array
        rox = [encode_rock(*spec) for spec in self.rocks]

        start, length = find_cycle(rox)

        cycle_spex = rox[start:start + length]

        return start, [decode_rock(spec) for spec in cycle_spex]

    def add_rows(self, n):
        for _ in range(n):
            self.rows.append(' ' * self.width)

    def rock_spawner(self):
        i = 0
        seq = ''.join(rock_sequence.keys())
        while True:
            new_rock = rock_sequence[seq[i]]

            pos = Point(SPAWN_OFFSET.x, self.height + SPAWN_OFFSET.y)

            yield new_rock, pos
            i = (i + 1) % len(seq)

    def freeze_rock(self, rock, x, y):
        # ensure rows exist
        new_height = y + rock.height
        prev_height = self.height
        self.add_rows(new_height - self.height)

        pen_y = y
        for offset, width, line in rock.rows:
            row = self.rows[pen_y]
            pen_x = x + offset
            self.rows[pen_y] = row[:pen_x] + line + row[pen_x + width:]

            pen_y += 1

        self.rocks.append((rock, x, -(y - prev_height)))

    def collides(self, rock, x, y):
        if x < 0 or x + rock.width > self.width or y < 0:  # cave boundaries
            return True

        pen_y = y
        for offset, width, _ in rock.rows:
            try:
                row = self.rows[pen_y]
            except IndexError:
                return False  # no row at this Y? must be empty
            pen_x = x + offset
            if row[pen_x:pen_x + width].strip():
                return True

            pen_y += 1

        return False

    def answer(self, n_rocks=2022, _debug=True):
        t = 0
        rock = None
        spawner = self.rock_spawner()
        pos = None
        falls = 0

        def __debug(m=None):
            print(m)
        debug = __debug if _debug else noop

        while len(self.rocks) < n_rocks:
            if rock is None:
                # spawn new rock
                rock, pos = next(spawner)
                debug(rock)
                debug(self.top_n_rows(7))
                falls = 0
                pass

            # first move by jet
            jet = self.jets[t % self.jets_mod]
            next_x = pos.x + jet
            if not self.collides(rock, next_x, pos.y):
                debug(f"jet moved {jet}")
                pos = Point(next_x, pos.y)
            else:
                debug(f"jet movement blocked ({jet})")

            # then try to move down
            next_y = pos.y - 1

            if self.collides(rock, pos.x, next_y):
                self.freeze_rock(rock, pos.x, pos.y)
                debug(f"shifts: {pos.x - SPAWN_OFFSET.x}, falls: {falls}, height: {self.height}")
                debug(self.top_n_rows(14))
                debug()

                rock = None
            else:
                pos = Point(pos.x, next_y)
                debug("fell down")
                falls += 1

            t += 1

        with open('dump.txt', 'w') as fp:
            fp.write(str(self))

        return self.height

    def answer2(self, n_rocks=1_000_000_000_000):
        # simulate a bunch of rocks, that should be enough to reveal the pattern
        sim_rocks = 3 * ((len(cave.jet_spec) // 3) * len(rock_sequence))

        if sim_rocks >= n_rocks:
            return self.answer()

        self.answer(20_000, False)
        # search for the loop
        cycle_start, cycle = self.analyze_specs()

        # measure the preamble
        preamble_height = measure_rocks(self.rocks[:cycle_start])

        # calculate the looping parts
        rocks_per_cycle = len(cycle)
        cycle_height = measure_rocks(cycle)
        cycle_rocks = n_rocks - cycle_start
        n_cycles = cycle_rocks // rocks_per_cycle
        cycles_height = n_cycles * cycle_height
        coda_rocks = cycle_rocks % rocks_per_cycle

        # calculate the coda
        coda_height = measure_rocks(cycle[:coda_rocks])

        return preamble_height + cycles_height + coda_height


arg_parser = ArgumentParser('python -m 17.main 17', description="Advent of Code Day 17")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    cave = Cave(parse_input(argus.input_path), argus.part)

    logger.info(cave)
    logger.debug('')

    if argus.part == 1:
        print(f"answer:\n{cave.answer()}")
        cave.rock_specs()
    else:
        print(f"answer:\n{cave.answer2()}")
