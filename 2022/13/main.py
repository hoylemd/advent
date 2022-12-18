from os import environ
import fileinput
import logging
import json


LOG_LEVEL = 'INFO'
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)
logger.addHandler(ch)


def parse_input():
    return (line.strip() for line in fileinput.input())


def render_packet(*parts):
    return '\n'.join(
        json.dumps(part, separators=(',', ':'))
        for part in parts
    )


class Thing:
    def __init__(self, lines):
        self.packets = self.parse(lines)

    def __str__(self):
        return '\n\n'.join(
            render_packet(*pair) for pair in self.packets
        )

    def parse(self, lines):
        packets = []
        buffer = None
        for line in lines:
            if not line: continue
            parsed = json.loads(line)
            if buffer is None:
                buffer = parsed
            else:
                packets.append((buffer, parsed))
                buffer = None

        return packets

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
