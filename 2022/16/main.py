import re
from argparse import ArgumentParser
from utils import logger, parse_input, LOG_LEVEL
from collections import deque

def render_open_valves(valves, relief):
    if not valves:
        return "No valves are open."

    return f"Valve {', '.join(v.label for v in valves)} open, releasing {relief} pressure."


def backtrack(distances, dest, src):
    cur = src
    path = []

    def get_distance(key):
        return distances[key]

    while cur != dest:
        path.append(cur)

        opts = cur.tunnels.keys()
        cur = cur.tunnels[sorted(opts, key=get_distance)[0]]

    path.reverse()
    return path


INFINITY = 9_999_999_999

class Valve:
    pattern = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)$')

    def __init__(self, label, flow_rate, tunnels, volcano):
        self.label = label
        self.flow_rate = flow_rate
        self.tunnels = {t: None for t in tunnels}
        self.volcano = volcano
        self.opened_at = None
        self.paths = {}

    def add_tunnel(self, other):
        self.tunnels[other.label] = other
        self.paths[other.label] = [other.label]

    def find_path(self, dest, _search=True):
        path = self.paths.get(dest)
        if path: return path

        if _search:
            self.map_tunnels()
            return self.find_path(dest, False)

        raise IndexError(f"Path for {dest} was not found from {self.label}")

    def map_tunnels(self):
        tent_dist = {}
        unvisited = []
        for v in self.volcano.valves:
            tent_dist[v.label] = 0 if v == self else INFINITY
            unvisited.append(v)

        def get_tentative(valve):
            return tent_dist[valve.label]

        visited = set()

        while unvisited:
            unvisited.sort(key=get_tentative, reverse=True)
            cur = unvisited.pop()

            c_dist = tent_dist[cur.label]
            neighbors = [self.volcano.index[t] for t in cur.tunnels if t not in visited]

            for n in neighbors:
                n_dist = c_dist + 1
                if n_dist < tent_dist[n.label]: tent_dist[n.label] = n_dist

            visited.add(cur)
            if self != cur:
                self.paths[cur.label] = backtrack(tent_dist, self, cur)


    def __str__(self):
        raw_tunnels = self.tunnels.keys()
        pluralized = 'tunnels lead to valves' if len(raw_tunnels) > 1 else 'tunnel leads to valve'
        return (
            f"Valve {self.label} has flow rate={self.flow_rate}; {pluralized} {', '.join(raw_tunnels)}"
        )

    def render_paths(self):
        return [f"Paths from {self.label}:"] + [
            f"- {dest}: {','.join(v.label for v in path)}({len(path)})"
            for dest, path in self.paths.items()
        ]

    def __repr__(self):
        return f"<Valve {self.label}>"

    def __hash__(self):
        return hash(self.label)

    def __eq__(self, other):
        if isinstance(other, str) and len(other) == 2:
            return self.label == other
        return self.label == other.label



class Volcano:
    def __init__(self, lines, part):
        self.part = part
        self.valves = self.parse(lines)
        self.t = 0
        self.pressure = 0
        self.useful_valves = []

        self.index = {v.label: v for v in self.valves}

        for valve in self.valves:
            for tunnel in valve.tunnels:
                valve.add_tunnel(self.index[tunnel])
            if valve.flow_rate:
                self.useful_valves.append(valve)


    def __str__(self):
        return '\n'.join(str(valve) for valve in self.valves)

    def parse_valve(self, line):
        matches = Valve.pattern.match(line)
        label = matches[1]
        flow_rate = int(matches[2])
        tunnels = matches[3].split(', ')

        return Valve(label, flow_rate, tunnels, self)

    def parse(self, lines):
        return [self.parse_valve(line) for line in lines]

    def relieve_pressure(self, minutes):
        for valve in self.valves:
            valve.map_tunnels()
            if LOG_LEVEL == 'DEBUG': logger.debug('\n'.join(valve.render_paths()))

        current_valve = self.index['AA']
        open_valves = {}
        pressure_relieved = 0

        path = []

        for t in range(minutes):
            pressure = sum(v.flow_rate for v in open_valves.values())
            pressure_relieved += pressure
            logger.info(f"== Minute {t + 1} ==")
            logger.info(render_open_valves(open_valves, pressure))

            if path:
                # take next step
                pass

            # show options
            options = {
                valve.label: (valve.flow_rate, current_valve.paths[valve])
                for valve in self.useful_valves
            }
            breakpoint()




        return pressure_relieved


    def answer(self, *args, **kwargs):
        if self.part == 1:
            return self.relieve_pressure(*args)

        return 0





arg_parser = ArgumentParser('python -m 16.main 16', description="Advent of Code Day 16")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    thing = Volcano(parse_input(argus.input_path), argus.part)

    logger.info(thing)
    logger.debug('')

    print(f"answer:\n{thing.answer(30)}")
