from argparse import ArgumentParser
from utils import logger, parse_input, Point, decomp_direction


class HouseGrid:
    def __init__(self, commands: str, agents: int = 1):
        self.agents = [Point(0, 0) for i in range(agents)]
        self.commands = ''.join(command for command in commands)
        self.visited = set()

    def __str__(self):
        return f"House grid with {len(self.commands)} commands and {len(self.agents)} agents."

    def count_unique_houses(self, *args, **kwargs):
        # account for first house
        self.visited.add(self.agents[0])

        for i, dir in enumerate(self.commands):
            agent_id = i % len(self.agents)
            house = self.agents[agent_id] + decomp_direction(dir)
            self.agents[agent_id] = house
            self.visited.add(house)

        return len(self.visited)


arg_parser = ArgumentParser('python -m 2015.3.main', description="Advent of Code 2015 Day 3")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    thing = HouseGrid(parse_input(argus.input_path), argus.part)

    logger.info(thing)
    logger.debug('')

    print(f"answer:\n{thing.count_unique_houses()}")
