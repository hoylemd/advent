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


def render_message(message):
    if isinstance(message, int): return str(message)
    return json.dumps(message, separators=(',', ':'))


def render_packet(*parts):
    return '\n'.join(
        render_message(part)
        for part in parts
    )


def noop():
    return


FIRST_DIVIDER = [[2]]
SECOND_DIVIDER = [[6]]


class WrongOrder(Exception):
    """Raised when evidence of wrong order found"""
    pass


def compare_lists(left, right, level=1):
    for i, l_op in enumerate(left):
        try:
            r_op = right[i]
        except IndexError as exc:
            logger.info(f"{'  ' * level}- Right side ran out of items so inputs are not in the right order")
            raise WrongOrder() from exc  # right ran out first

        if compare(l_op, r_op, level):
            return True

    if len(right) > len(left):
        logger.info(f"{'  ' * level}- Left side ran out of items so inputs are in the right order")
        return True  # left ran out furst


def compare(left, right, level=1):
    logger.info(f"{'  ' * level}- Compare {render_message(left)} vs {render_message(right)}")
    if isinstance(left, int) and isinstance(right, int):  # both ints
        if left < right:
            logger.info(f"{'  ' * (level + 1)}- Left side is smaller so inputs are in the right order")
            return True
        if left > right:
            logger.info(f"{'  ' * (level + 1)}- Right side is smaller so inputs are not in the right order")
            raise WrongOrder
        return False

    if isinstance(left, int):
        logger.info(f"{'  ' * (level + 1)}- Mixed types; convert left to [{left}] and retry comparison")
        left = [left]
    if isinstance(right, int):
        logger.info(f"{'  ' * (level + 1)}- Mixed types; convert right to [{right}] and retry comparison")
        right = [right]

    if compare_lists(left, right, level + 1):
        return True


def quicksort(list):
    length = len(list)
    if length < 2: return list  # base case, we done
    pivot = list.pop()

    lower = []
    higher = []
    for element in list:
        logger.info(f"- Compare {render_message(element)} vs {render_message(pivot)}")
        try:
            if compare(element, pivot):
                lower.append(element)
            else:
                logger.warning('lolwut')
                breakpoint()
        except WrongOrder:
            higher.append(element)

    assert len(lower) + 1 + len(higher) == length

    return quicksort(lower) + [pivot] + quicksort(higher)


def is_sorted(left, right):
    logger.info(f"- Compare {render_message(left)} vs {render_message(right)}")

    try:
        return compare(left, right)
    except WrongOrder:
        return False


class Thing:
    def __init__(self, lines, part='1'):
        self.part = int(part)
        if self.part == 1:
            self.packets = self.parse(lines)
        else:
            self.packets = self.parse_2(lines) + [FIRST_DIVIDER, SECOND_DIVIDER]

    def __str__(self):
        if self.part == 1:
            return '\n\n'.join(
                render_packet(*pair) for pair in self.packets
            )
        else:
            return '\n'.join(render_message(packet) for packet in self.packets)

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

    def parse_2(self, lines):
        return [json.loads(line) for line in lines if line]

    def count_sorted(self):
        ok_indicies = []
        for i, packet in enumerate(self.packets):
            logger.info(f"== Pair {i+1} ==")
            if is_sorted(*packet):
                ok_indicies.append(i + 1)
            logger.info('')

        logger.info(f"Sorted Indicies: {ok_indicies}")
        return sum(ok_indicies)

    def find_dividers(self):
        first_index = 0
        second_index = 0

        self.packets = quicksort(self.packets)
        logger.info(self)

        for i, packet in enumerate(self.packets):
            if packet == FIRST_DIVIDER:
                first_index = i + 1

            if packet == SECOND_DIVIDER:
                second_index = i + 1

        logger.info(f"First divider at {first_index}, Second at {second_index}")
        return first_index * second_index

    def answer(self, func, *args, **kwargs):
        return func()

    def for_part(self, part='1'):
        return {
            '1': [self.count_sorted],
            '2': [self.find_dividers]
        }[part]


if __name__ == '__main__':
    thing = Thing(parse_input(), part=environ['ADVENT_PART'])

    logger.debug(thing)
    logger.debug('')

    print(f"answer:\n{thing.answer(*thing.for_part(environ['ADVENT_PART']))}")
