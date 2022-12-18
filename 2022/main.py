from os import environ
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


class Thing:
    def __init__(self, lines):
        self.parse(lines)

    def parse(self, lines):
        for line in lines:
            pass

    def answer(self, *args, **kwargs):
        return 0

    def for_part(self, part='1'):
        return {
            '1': [],
            '2': []
        }[part]


if __name__ == '__main__':
    thing = Thing(parse_input())

    logger.info(thing)
    logger.debug('')

    print(f"answer:\n{thing.answer(*thing.for_part(environ['ADVENT_PART']))}")
