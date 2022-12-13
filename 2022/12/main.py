import fileinput
from logging import getLogger

logger = getLogger(__name__)


def parse_input():
    return (line.strip() for line in fileinput.input())


if __name__ == '__main__':
    lines = parse_input()

    for line in lines:
        logger.debug(line)
