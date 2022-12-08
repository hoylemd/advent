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
        for line in fileinput.input():
            grid_line = []
            vis_line = []
            for c in line.strip():
                grid_line.append(int(c))
                vis_line.append(False)
            self.grid.append(grid_line)
            self.ext_vis_map.append(vis_line)

        self.scan_grid()


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

    def print_grids(self):
        lines = []

        for y in range(len(self.grid)):
            lines.append(f"{self.str_grid_line(self.grid[y])} {self.vis_grid_line(self.ext_vis_map[y])}")

        debug('\n'.join(lines))
        debug()

    def get_tree(self, x, y):
        try:
            return self.grid[y][x]
        except IndexError:
            return None

    def mark_visible(self, x, y):
        try:
            self.ext_vis_map[y][x] = True
        except TypeError as exc:
            self.print_grids()
            debug(f"{x=}, {y=}")
            breakpoint()
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

        self.print_grids()

        # rotate grid
        self.rotate_grids()

        # vertical scanning
        for y in range(len(self.grid)):
            self.scan_line(y)


    def count_ext_visible(self):
        # count up the ext_vis_map
        return sum(line.count(True) for line in self.ext_vis_map)


if __name__ == '__main__':
    grid = TreeGrid()

    grid.print_grids()

    print(grid.count_ext_visible())
