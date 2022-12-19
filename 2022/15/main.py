from os import environ
from utils import logger, parse_input


class Thing:
    def __init__(self, lines, part):
        self.part = part
        self.input = self.parse(lines)

    def __str__(self):
        return '\n'.join(self.input)

    def parse(self, lines):
        return [line for line in lines]

    def answer(self, *args, **kwargs):
        return 0


if __name__ == '__main__':
    part = int(environ.get('ADVENT_PART', 1))
    thing = Thing(parse_input(), part)

    logger.info(thing)
    logger.debug('')

    print(f"answer:\n{thing.answer()}")
