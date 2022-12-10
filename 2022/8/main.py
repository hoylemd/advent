import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_line(line):
    return [int(c) for c in line.strip()]


class TreeGrid:
    def __init__(self):
        self.grid = []  #[parse_line(line) for line in fileinput.input()]
        self.ext_vis_map = []
        self.scenic_map = []
        self.width = 0
        self.height = 0
        self.max_scenic = 0
        for line in fileinput.input():
            grid_line = []
            vis_line = []
            scenic_line = []
            for c in line.strip():
                if self.height == 0: self.width += 1
                grid_line.append(int(c))
                vis_line.append(False)
                scenic_line.append(0)
            self.height += 1

            self.grid.append(grid_line)
            self.ext_vis_map.append(vis_line)
            self.scenic_map.append(scenic_line)

    def __str__(self):
        return '\n'.join(
            self.str_grid_line(line)
            for line in self.grid
        )

    def str_grid_line(self, line):
        return f"{''.join(''.join(str(c) for c in line))}"

    def vis_grid_vis(self):
        return '\n'.join(
            self.vis_grid_line(line)
            for line in self.ext_vis_map
        )

    def vis_grid_line(self, line):
        return f"{''.join(''.join('V' if c else '.' for c in line))}"

    def scenic_grid_line(self, line):
        return '|'.join(f"{c:2}" for c in line)

    def print_grids(self):
        lines = []

        for y in range(len(self.grid)):
            lines.append(f"{self.str_grid_line(self.grid[y])} {self.scenic_grid_line(self.scenic_map[y])}")

        return('\n'.join(lines))

    def get_tree(self, x, y):
        try:
            return self.grid[y][x]
        except IndexError:
            return None

    def mark_visible(self, x, y):
        try:
            self.ext_vis_map[y][x] = True
        except TypeError as exc:
            debug(self.print_grids())
            debug(f"{x=}, {y=}")
            raise

    def scan_line(self, y):
        line = self.grid[y]

        # from left
        tallest = -1
        x = 0

        for tree in line:
            if tree > tallest: # visible
                tallest = tree
                self.mark_visible(x, y)

            if tallest == 9:
                break  # max height, everything behind invisible

            x += 1

        # from right
        tallest = -1
        for x in range(len(line)-1, -1, -1):
            tree = line[x]
            if tree > tallest: # visible
                tallest = tree
                self.mark_visible(x, y)

            if tallest == 9:
                break  # max height

    def rotate_grids(self):
        self.grid = list(list(col) for col in zip(*self.grid[::-1]))
        self.ext_vis_map = list(list(col) for col in zip(*self.ext_vis_map[::-1]))

    def scan_grid(self):
        # horizontal scanning
        for y in range(len(self.grid)):
            self.scan_line(y)

        debug(self.print_grids())

        # rotate grid
        self.rotate_grids()

        # vertical scanning
        for y in range(len(self.grid)):
            self.scan_line(y)

    def count_ext_visible(self):
        # count up the ext_vis_map
        return sum(line.count(True) for line in self.ext_vis_map)

    def calc_scenic_score(self, x, y):
        height = self.get_tree(x, y)
        debug(f"calc scenic for ({x}, {y}): {height}")

        # scan left
        l_dist = 0
        for i in range(x-1, -1, -1):
            l_dist += 1
            if self.get_tree(i, y) >= height:
                break
        debug(f"{l_dist=}")

        # scan up
        u_dist = 0
        for i in range(y-1, -1, -1):
            u_dist += 1
            if self.get_tree(x, i) >= height:
                break
        debug(f"{u_dist=}")

        # scan right
        r_dist = 0
        for i in range(x+1, self.width, 1):
            r_dist += 1
            if self.get_tree(i, y) >= height:
                break
        debug(f"{r_dist=}")

        # scan down
        d_dist = 0
        for i in range(y+1, self.height, 1):
            d_dist += 1
            if self.get_tree(x, i) >= height:
                break
        debug(f"{d_dist=}")

        score = l_dist * u_dist * r_dist * d_dist
        self.scenic_map[y][x] = score
        return score

    def scan_scenic(self):
        max_scenic = 0
        for y in range(1, len(self.grid) - 1):
            for x in range(1, len(self.grid[y]) - 1):
                score = self.calc_scenic_score(x, y)
                if score > max_scenic: max_scenic = score
                debug(f"score for ({x},{y}): {score}{'*' if score == max_scenic else ''}")
        return max_scenic

if __name__ == '__main__':
    grid = TreeGrid()

    print(grid.scan_scenic())
    #print(grid.calc_scenic_score(2, 3))

    print(grid.print_grids())
