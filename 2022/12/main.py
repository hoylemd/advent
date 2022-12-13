import fileinput
import logging


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


INFINITY = 9_999_999_999
LEFT = '<'
UP = '^'
RIGHT = '>'
DOWN = 'V'

dir_masks = {
    LEFT: (-1, 0),
    UP: (0, -1),
    RIGHT: (1, 0),
    DOWN: (0, 1)
}


class Map:
    def __init__(self, lines):
        self.start = None
        self.end = None
        self.pos = None
        self.map, self.visited, self.distance = self.parse(lines)
        self.steps = []

    def parse(self, lines):
        map, visited, distance = [], [], []
        for y, line in enumerate(lines):
            m_row, v_row, d_row = [], [], []
            for x, c in enumerate(line):
                if c == 'S':  # start found
                    self.start = (x, y)
                    self.pos = self.start
                    c = 'a'
                if c == 'E':  # end found
                    self.end = (x, y)
                    c = 'z'

                m_row.append(atoi(c))
                v_row.append(False)
                d_row.append(INFINITY)
            map.append(m_row)
            visited.append(v_row)
            distance.append(d_row)

        return map, visited, distance

    def valid_coords(self, x, y):
        if x < 0 or y < 0:
            return False
        if y > len(self.map) - 1:
            return False
        if x > len(self.map[0]) - 1:
            return False

        return True

    def render_visited(self, current_node, known):
        rows = []
        for y, row in enumerate(self.visited):
            r_str = []
            for x, cell in enumerate(row):
                pen = '#' if cell else '.'
                if (x, y) == self.start:
                    pen = 'S'
                if (x, y) == self.end:
                    pen = 'E'
                if (x, y) in known:
                    pen = 'o'
                if (x, y) == current_node:
                    pen = 'X'

                r_str.append(pen)
            rows.append(''.join(r_str))
        return rows

    def print_visited(self, current_node, known):
        return '\n'.join(self.render_visited(current_node, known))

    def render_distance(self):
        rows = []
        for y, row in enumerate(self.distance):
            r_cells = []
            for x, cell in enumerate(row):
                r_cells.append(f"{self.get_distance(x, y):3}")
            rows.append('|'.join(r_cells))
        return rows

    def print_distance(self):
        return '\n'.join(self.render_distance())

    def get_height(self, x, y):
        return self.map[y][x]

    def mark_visited(self, x, y):
        if self.visited[y][x]:
            raise ValueError
        self.visited[y][x] = True

    def is_visited(self, x, y):
        return self.visited[y][x]

    def set_distance(self, x, y, dist):
        c_dist = self.distance[y][x]
        if dist < c_dist:
            self.distance[y][x] = dist

    def get_distance(self, x, y):
        dist = self.distance[y][x]
        return 'inf' if dist == INFINITY else dist

    def get_neighbors(self, x, y):
        height = self.map[y][x]
        neighbors = []
        for dir, mask in dir_masks.items():
            dx, dy = mask
            nx, ny = x + dx, y + dy
            if not self.valid_coords(nx, ny):
                continue
            n_height = self.map[ny][nx]
            if n_height - height < 2 and not self.visited[ny][nx]:
                neighbors.append((nx, ny))

        return neighbors

    def consider_neighbors(self, neighbors, c_dist):
        n_dist = c_dist + 1
        for x, y in neighbors:
            self.set_distance(x, y, n_dist)

    def djikstra(self):
        current_node = self.start
        self.mark_visited(*current_node)
        self.set_distance(*current_node, 0)
        known = []

        def get_distance(coords):
            x, y = coords
            return self.distance[y][x]

        def r_known(x, y):
            return f"({x},{y}):{self.get_distance(x, y)}"

        while not self.is_visited(*self.end):
            neighbors = self.get_neighbors(*current_node)
            self.consider_neighbors(neighbors, self.get_distance(*current_node))
            logger.debug(f"curr: {r_known(*current_node)}")
            logger.debug(f"knew: {' '.join(r_known(*k) for k in known)}")
            logger.debug(f"neig: {' '.join(r_known(*n) for n in neighbors)}")

            known += neighbors

            known = sorted(known, key=get_distance)
            known.reverse()

            while self.is_visited(*current_node):
                current_node = known.pop()
            self.mark_visited(*current_node)

            logger.debug(f"next: {r_known(*current_node)}")
            logger.debug(f"know: {' '.join(r_known(*k) for k in known)}")
            logger.info(self.print_visited(current_node, known))
            logger.debug('')
            logger.debug(self.print_distance())
            logger.debug('')

        return self.distance[self.end[1]][self.end[0]]

    def render_line(self, line):
        return ''.join(itoa(c) for c in line)

    def __str__(self):
        return '\n'.join(self.render_line(row) for row in self.map)


if __name__ == '__main__':
    map = Map(parse_input())

    logger.info(map)
    logger.debug('')

    print(f"answer:\n{map.djikstra()}")
