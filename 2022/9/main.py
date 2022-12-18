import fileinput

DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


def parse_input():
    for line in fileinput.input():
        dir, mag = line.strip().split()
        yield dir, int(mag)


def decomp_direction(dir):
    return {
        'L': (-1, 0),
        'U': (0, 1),
        'R': (1, 0),
        'D': (0, -1)
    }[dir]


def reduce_vector(x, y):
    if x > 1:
        x = 1
    elif x < -1:
        x = -1

    if y > 1:
        y = 1
    elif y < -1:
        y = -1

    return (x, y)


def is_adjacent(dx, dy):
    # 3 if diagonal, 2 if cardinal
    thresh = 2 if dy == 0 or dx == 0 else 3

    return abs(dx) + abs(dy) < thresh


def vector(start, dest):
    return dest[0] - start[0], dest[1] - start[1]


class Rope:
    def __init__(self, knots=2):
        self.n_knots = knots
        self.tail_visited = set()
        self.grid_size = (0, 0)
        self.start_at = (0, 0)

    def __str__(self):
        return '\n'.join(
            reversed([self.render_line(i) for i in range(self.grid_size[1] + 1)])
        )

    def render_line(self, y):
        return ''.join(self.render_cell(x, y) for x in range(self.grid_size[0] + 1))

    def render_cell(self, x, y):
        knot_char = None

        for i, knot in enumerate(self.knots):
            if knot == (x, y):
                knot_char = str(i)
                break

        if knot_char == '0':
            return 'H'

        if self.t_pos == (x, y):
            return 'T'

        if knot_char:
            return knot_char

        if (x, y) in self.tail_visited:
            return 'x'

        return '.'

    @property
    def h_pos(self):
        return self.knots[0]

    @property
    def t_pos(self):
        return self.knots[-1]

    def move_head(self, dx, dy):
        return self.move_knot(0, dx, dy)

    def move_tail(self, dx, dy):
        return self.move_knot(-1, dx, dy)

    def move_knot(self, knot_index, dx, dy):
        current = self.knots[knot_index]
        self.knots[knot_index] = (current[0] + dx, current[1] + dy)

    def tail_vector(self):
        return vector(self.t_pos, self.h_pos)

    def move(self, dir):
        self.move_head(*decomp_direction(dir))

        tail_vector = self.tail_vector()
        if is_adjacent(*tail_vector):  # still touching
            debug(f"head at {self.h_pos}, tail at {self.t_pos}, delta: {tail_vector}")
            return

        self.move_tail(*reduce_vector(*tail_vector))

        debug(f"head at {self.h_pos}, tail at {self.t_pos}, delta: {tail_vector}")

        self.tail_visited.add(self.t_pos)

    def move_v2(self, dir):
        dx, dy = decomp_direction(dir)
        for i, pos in enumerate(self.knots):
            if i:  # means we're not looking at head
                dx, dy = vector(pos, self.knots[i - 1])
                if is_adjacent(dx, dy):
                    return  # later knots arent going to move either

            self.move_knot(i, *reduce_vector(dx, dy))

        self.tail_visited.add(self.t_pos)

    def execute(self, dir, dist):
        for i in range(dist):
            self.move_v2(dir)

        if DEBUG:
            print(self)
            print('')

    def check_instruction(self, dir, dist):
        unit = decomp_direction(dir)
        ax, ay = self.anal_surp
        gx, gy = self.grid_size

        dx, dy = (unit[0] * dist, unit[1] * dist)
        debug(f"checking {dir}, {dist}: {dx, dy}")

        if dx < 0:
            ax += dx
        else:
            delta = ax + dx
            if delta <= 0:
                ax += dx
            else:
                ax = 0
                gx += delta

        if dy < 0:
            ay += dy
        else:
            delta = ay + dy
            if delta <= 0:
                ay += dy
            else:
                ay = 0
                gy += delta

        self.grid_size = (gx, gy)
        self.anal_surp = (ax, ay)
        debug(f"{self.grid_size=}, {self.anal_surp=}")

        return (dir, dist)

    def check(self, instructions):
        acked = [self.check_instruction(*instr) for instr in instructions]

        print(f"{self.grid_size=}, {self.anal_surp=}")

        left, down = self.grid_size[0] + self.anal_surp[0], self.grid_size[1] + self.anal_surp[1]
        self.grid_offset = (min(0, left), min(0, down))
        self.grid_size = (self.grid_size[0] - self.grid_offset[0], self.grid_size[1] - self.grid_offset[1])

        st = (-self.grid_offset[0], -self.grid_offset[1])

        self.knots = [(st[0], st[1]) for knot in self.knots]

        print(f"{left=}, {down=}, {self.grid_offset=}")

        return acked

    def check_v2(self, instructions):
        self.acked = []
        x_max = (0, 0)
        y_max = (0, 0)
        pos = (0, 0)

        for dir, dist in instructions:
            self.acked.append((dir, dist))
            unit = decomp_direction(dir)

            dx, dy = (unit[0] * dist, unit[1] * dist)
            debug(f"checking {dir}, {dist}: {dx, dy}")

            pos = (pos[0] + dx, pos[1] + dy)

            if pos[0] < x_max[0]:
                x_max = (pos[0], x_max[1])
            if pos[0] > x_max[1]:
                x_max = (x_max[0], pos[0])

            if pos[1] < y_max[0]:
                y_max = (pos[1], y_max[1])
            if pos[1] > y_max[1]:
                y_max = (y_max[0], pos[1])
            debug(f"bounds: {x_max=}, {y_max=}")

        grid_dims = (x_max[1] - x_max[0], y_max[1] - y_max[0])
        start = (-x_max[0], -y_max[0])
        debug(f"{x_max=}, {y_max=} => {grid_dims=}, {start=}")

        self.grid_size = grid_dims
        self.start = start

        return self.acked

    def simulate(self, instructions):
        acked = self.check_v2(instructions)

        self.knots = [(self.start[0], self.start[1]) for i in range(self.n_knots)]

        self.tail_visited.add(self.t_pos)

        print(self)
        print()

        for dir, dist in acked:
            # breakpoint()
            print(f"executing {dir} {dist}")
            self.execute(dir, dist)

    def visited_grid(self):
        x_bounds = [0, 5]
        y_bounds = [0, 5]
        # for x, y in self.tail_visited:
        #     if x < x_bounds[0]: x_bounds[0] = x
        #     elif x > x_bounds[1]: x_bounds[1] = x

        #     if y < y_bounds[0]: y_bounds[0] = y
        #     elif y > y_bounds[1]: y_bounds[1] = y

        n_rows = (y_bounds[1] - y_bounds[0]) + 1
        n_cols = (x_bounds[1] - x_bounds[0]) + 1

        rows = []
        for y in range(n_rows):
            row = ''
            for x in range(n_cols):
                if (x, y) == self.h_pos:
                    row += 'H'
                    continue
                elif (x, y) == self.t_pos:
                    row += 'T'
                    continue
                row += '#' if (x, y) in self.tail_visited else '.'
            rows.append(row)

        return '\n'.join(rows)


if __name__ == '__main__':
    rope = Rope(10)
    rope.simulate(parse_input())
    print(len(rope.tail_visited))
