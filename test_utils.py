from utils import CharGrid


def test_djikstra():
    grid = CharGrid.from_dims(10, 10)
    nav_map = CharGrid(grid.djikstra((0, 0)))

    print(nav_map.render_grid(column_delimiter='|', row_delimiter='-+'))


if __name__ == '__main__':
    test_djikstra()
