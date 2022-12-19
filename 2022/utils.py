import os
import logging
import fileinput

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)


def parse_input():
    return (line.strip() for line in fileinput.input())


def render_line(line, shader=str):
    return ''.join(shader(c) for c in line)


def render_lines(lines, shader=str):
    return (render_line(line, shader) for line in lines)


def render_grid(grid, shader=str):
    return '\n'.join(render_lines(grid, shader))


def num_width(number):
    width = 1
    if number < 0:
        width += 1

    val = abs(number)
    while val := int(val / 10):
        width += 1

    return width


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


def vector(start, dest):
    return dest[0] - start[0], dest[1] - start[1]
