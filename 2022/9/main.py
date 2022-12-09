import fileinput

DEBUG = True


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


class Rope:
    def __init__(self):
        self.h_pos = (0, 0)
        self.t_pos = (0, 0)
        self.tail_visited = set()
        self.tail_visited.add(self.t_pos)

    def move_head(self, dx, dy):
        self.h_pos = (self.h_pos[0] + dx, self.h_pos[1] + dy)

    def move_tail(self, dx, dy):
        self.t_pos = (self.t_pos[0] + dx, self.t_pos[1] + dy)

    def tail_vector(self):
        return self.h_pos[0] - self.t_pos[0], self.h_pos[1] - self.t_pos[1]

    def move(self, dir):
        self.move_head(*decomp_direction(dir))

        tail_vector = self.tail_vector()
        if is_adjacent(*tail_vector): # still touching
            debug(f"head at {self.h_pos}, tail at {self.t_pos}, delta: {tail_vector}")
            return

        self.move_tail(*reduce_vector(*tail_vector))

        debug(f"head at {self.h_pos}, tail at {self.t_pos}, delta: {tail_vector}")

        self.tail_visited.add(self.t_pos)

    def execute(self, dir, dist):
        for i in range(dist):
            self.move(dir)

    def simulate(self, instructions):
        for dir, dist in instructions:
            debug(f"executing {dir} {dist}")
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
    rope = Rope()
    rope.simulate(parse_input())
    print(len(rope.tail_visited))
