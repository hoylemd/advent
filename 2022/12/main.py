import fileinput
import logging
from collections import defaultdict


LOG_LEVEL = 'INFO'
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)


def parse_input():
    return (line.strip() for line in fileinput.input())


def atoi(string):
    return ord(string) - ord('a')


def itoa(integer):
    return chr(integer + ord('a'))


LEFT = '<'
UP = '^'
RIGHT = '>'
DOWN = 'V'


class Map:
    def __init__(self, lines):
        self.start = None
        self.end = None
        self.pos = None
        self.map = [self.parse_line(line, y) for y, line in enumerate(lines)]
        self.steps = []
        self.bad_dirs = defaultdict(list)

    def parse_line(self, line, y):
        row = []
        for x, c in enumerate(line):
            if c == 'S':  # start found
                self.start = (x, y)
                self.pos = self.start
                c = 'a'
            if c == 'E':  # end found
                self.end = (x, y)
                c = 'z'

            row.append(atoi(c))

        return row

    def valid_coords(self, x, y):
        if x < 0 or y < 0:
            return False
        if y > len(self.map) - 1:
            return False
        if x > len(self.map[0]) - 1:
            return False

        return True

    def coords_from_pos_n_dir(self, pos, dir):
        if dir == LEFT:
            next_step = (pos[0] - 1, pos[1])
        if dir == UP:
            next_step = (pos[0], pos[1] - 1)
        if dir == RIGHT:
            next_step = (pos[0] + 1, pos[1])
        if dir == DOWN:
            next_step = (pos[0], pos[1] + 1)

        return next_step if self.valid_coords(*next_step) else None

    def step(self, dir):
        next_step = self.coords_from_pos_n_dir(self.pos, dir)

        self.steps.append((self.pos, dir))
        self.pos = next_step

    def go_back(self):
        self.pos, bad_dir = self.steps.pop()
        self.bad_dirs[self.pos].append(bad_dir)

    def render_path(self):
        grid = [
            ['.' for c in range(len(row))]
            for row in self.map
        ]

        for coords, dir in self.steps:
            x, y = coords
            grid[y][x] = dir

        grid[self.start[1]][self.start[0]] = 'S'
        grid[self.end[1]][self.end[0]] = 'E'
        grid[self.pos[1]][self.pos[0]] = 'X'

        return '\n'.join(
            ''.join(row) for row in grid
        )

    def too_high(self, x, y):
        here = self.map[self.pos[1]][self.pos[0]]
        there = self.map[y][x]
        if there - here < 2:
            return False
        return True

    def greedy_directions(self):
        dx = self.end[0] - self.pos[0]
        dy = self.end[1] - self.pos[1]

        dir_order = []

        if abs(dx) > abs(dy):
            dir_order.append(LEFT if dx < 0 else RIGHT)
            dir_order.append(UP if dy < 0 else DOWN)
            dir_order.append(UP if DOWN in dir_order else DOWN)
            dir_order.append(LEFT if RIGHT in dir_order else RIGHT)
        elif abs(dy) > abs(dx):
            dir_order.append(UP if dy < 0 else DOWN)
            dir_order.append(LEFT if dx < 0 else RIGHT)
            dir_order.append(LEFT if RIGHT in dir_order else RIGHT)
            dir_order.append(UP if DOWN in dir_order else DOWN)
        else:
            if dx < 0 and dy < 0:
                dir_order = (LEFT, DOWN, UP, RIGHT)
            elif dx > 0 and dy < 0:
                dir_order = (RIGHT, DOWN, UP, LEFT)
            elif dx < 0 and dy > 0:
                dir_order = (LEFT, UP, DOWN, RIGHT)
            else:
                dir_order = (RIGHT, UP, DOWN, LEFT)

        return dir_order

    def visited(self, x, y):
        for coords, dir in self.steps[::-1]:
            if (x, y) == coords:
                return True

        return False

    def backtracks(self, x, y):
        return self.visited(x, y) and self.map[y][x] <= self.map[self.pos[1]][self.pos[0]]

    def pick_path(self):
        ok_dirs = {}
        next_step = None
        next_dir = None
        dirs = self.greedy_directions()
        logger.debug(f" trying directions {dirs}")
        for dir in dirs:
            next_step = self.coords_from_pos_n_dir(self.pos, dir)
            if next_step is None: continue
            if self.too_high(*next_step) or self.backtracks(*next_step) or dir in self.bad_dirs[next_step]:
                next_step = None
                continue
            ok_dirs[dir] = self.map[next_step[1]][next_step[0]]

        def get_height(pair):
            return pair[1]

        if ok_dirs:
            sortd = sorted(ok_dirs.items(), reverse=True, key=get_height)
            next_dir = sortd[0][0]
            logger.debug(f"going {next_dir}")
        return next_dir

    def seek_summit(self):
        while self.pos != self.end:
            dir = self.pick_path()
            if dir:
                self.step(dir)
            else:
                self.go_back()

            logger.debug(self)
            logger.debug(self.render_path())
            logger.debug('')
            # breakpoint()

    def render_line(self, line):
        return ''.join(itoa(c) for c in line)

    def __str__(self):
        return '\n'.join(self.render_line(row) for row in self.map)


if __name__ == '__main__':
    map = Map(parse_input())

    logger.info(map)
    logger.info(map.render_path())
    logger.debug('')
    map.seek_summit()

    print(f"answer:\n{len(map.steps)}")
