from argparse import ArgumentParser
from dataclasses import dataclass, field
import re

from utils import logger, parse_input, INFINITY, list_from_mask  # noqa F401


@dataclass(frozen=True)
class ValveStruct:
    """Represents a Valve in the Volcano

    :param str label: The label for the valve
    :param int flow_rate: Pressure relievef per minute this valve is open
    :param tuple[str] neighbors: tuple of valve labels that are adjacent to this valve
    """
    label: str = field(compare=True)
    flow_rate: int = field(compare=False)
    neighbors: tuple[str] = field(compare=False)

    pattern = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)$')

    @classmethod
    def parse(cls, input):
        """Instantiate a ValveStruct from a line from the challenge input

        :param str input: The line from the input representing this valve
        :return ValveStruct: The Valve object as specified
        """
        matches = ValveStruct.pattern.match(input)

        label = matches[1]
        flow_rate = int(matches[2])
        tunnels = matches[3].split(', ')

        return ValveStruct(label, flow_rate, tunnels)

    def render(self):
        """Render out the spec for this ValveStruct

        :return str: The Spec from which this ValveStruct was generated
        """
        pluralized = 'tunnels lead to valves' if len(self.neighbors) > 1 else 'tunnel leads to valve'
        return (
            f"Valve {self.label} has flow rate={self.flow_rate}; {pluralized} {', '.join(self.neighbors)}"
        )

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"<{self.label},{self.flow_rate}>"


class ValveGraph:
    """Represents the graph of Valves"""
    @classmethod
    def parse(cls, specs):
        return ValveGraph([ValveStruct.parse(spec) for spec in specs])

    def __init__(self, nodes):
        """Construct a ValveGraph.

        :param iter[ValveStruct] nodes: iterable of ValveStructs representing nodes in the graph
        """
        self.nodes = {node.label: node for node in nodes}
        self.paths = {}

    def backtrack(self, distances, dest, src):
        """Given tentative distances from Djikstra's algorithm, backtrack the path from an endpoint to a start point

        :param dict[str: int]: Dict of distances to a given node from _src_
        :param str dest: Label of the node from which to backtrack
        :param str src: Label of the node to backtrack to

        :returns list[str]: A list of node labels representing the optimal path from _src_ to _dest_ in the graph
        """
        cur = self.nodes[src]
        path = []

        def get_distance(key):
            return distances[key]

        while cur.label != dest:
            path.append(cur.label)

            cur = self.nodes[sorted(cur.neighbors, key=get_distance)[0]]

        # TODO: unnecessary?
        path.reverse()
        return path

    def _map_from_node(self, node: ValveStruct):
        """Map out all the paths from a given node

        Hello Djikstra my old friend...

        :param ValveStruct node: The node from which to start
        :return dict[str:list[str]]: dict of paths to each other node
        """
        paths = {}
        tent_dist = {}
        unvisited = []
        for n in self.nodes:
            tent_dist[n] = 0 if n == node.label else INFINITY
            unvisited.append(n)

        visited = set()

        while unvisited:
            unvisited.sort(key=tent_dist.get, reverse=True)
            cur = self.nodes[unvisited.pop()]

            c_dist = tent_dist[cur.label]
            neighbors = [self.nodes[t] for t in cur.neighbors if t not in visited]

            for n in neighbors:
                n_dist = c_dist + 1
                if n_dist < tent_dist[n.label]: tent_dist[n.label] = n_dist

            visited.add(cur)
            if node != cur:
                paths[cur.label] = self.backtrack(tent_dist, node.label, cur.label)

        return paths

    def map_paths(self):
        """Map out all of the paths from node to node, noting distances

        i.e. paths[x][y] will return the list of nodes in the optimal path from _x_ to _y_ (not including _x_)

        e.g.:

        paths['A']['D'] => ['B', 'C', 'D']

        :return dict: The pathing matrix
        """
        self.paths = {
            valve: self._map_from_node(self.nodes[valve])
            for valve in self.nodes
        }

    def get_distance(self, src: str, dest: str):
        """Get the distance between 2 nodes

        :param str src: label of initial node
        :param str dest: label of destination node

        :return int: the distance between the specified nodes
        """
        return len(self.paths[src][dest])

    def __str__(self):
        """Render a string-representation of the graph

        Basically, just repro the input for parse testing

        :return str: The spec that was used to generate this graph
        """
        return '\n'.join(valve.render() for valve in self.nodes.values())


@dataclass(frozen=True, order=True)
class State:
    """Represents a possible state if a valve-opening procedure

    :field int t: The number of minutes remaining after this state is achieved
    :field str pos: The label for the valve that the current player is at in this state
    :field int open_valves: bitmask of open valves
    :field int score_so_far: Pressure relieved up to the moment of this state
    """
    t: int  # time left
    pos: str
    open_valves: int  # bitmask representing the open valves
    score_so_far: int

    @property
    def valid(self):
        """Whether this state is actually valid.

        States that occur after the time limit are not valid.

        :return bool: Whether this state is valid or not.
        """
        return self.t >= 0

    def __repr__(self):
        return f"<{self.pos}@{self.t}:{self.open_valves:016b}={self.score_so_far}>"


class Solver:
    """Top-level logic object for AoC 2022-16"""

    def __init__(self, graph):
        """Constructor

        :param ValveGraph graph: The ValveGraph representing the valves in the volcano
        """
        self.graph = graph
        self.scores = {}
        self.bitmasks = {
            valve: 2 ** i
            for i, valve in enumerate(self.good_valves)
        }

        self.flow_by_mask = {}

    def get_flow(self, mask: int):
        """Calculate the total flow rate for a set of open valves

        :param tuple[str] mask: bitmask for the valves in question
        :return int: The total flow rate for the specified valves
        """
        flow = self.flow_by_mask.get(mask)

        if flow is None:
            valves = list_from_mask(self.good_valves, mask)
            flow = sum(self.graph.nodes[v].flow_rate for v in valves)
            self.flow_by_mask[mask] = flow

        return flow

    def score_state(self, state):
        """Calculate the total score/pressure relieved for a given state if no further moves are taken

        Also memoizes the state in self.scores because DP BayBeeee

        :param State state: The state for which to calculate the score
        :return int: The score of the state provided
        """
        if state not in self.scores:
            self.scores[state] = state.score_so_far + state.t * self.get_flow(state.open_valves)

        return self.scores[state]

    def next_state(self, state: State, dest: str):
        """Compute a next state from a given State and the next node to move to

        :param State state: The current state from which to compute the next
        :param str dest: The next valve the player will move towards

        :return State: The next State, after the player has moved to the next node
        """
        delta_t = self.graph.get_distance(state.pos, dest) + 1
        additional_score = delta_t * self.get_flow(state.open_valves)

        return State(
            t=state.t - delta_t,
            pos=dest,
            open_valves=state.open_valves | self.bitmasks[dest],
            score_so_far=state.score_so_far + additional_score,
        )

    @property
    def good_valves(self):
        """List of labels of useful valves in the volcano.

        useful valves are those with a non-zero flow rate

        :return list[str]: List of the useful valve labels
        """

        return [v for v, valve in self.graph.nodes.items() if valve.flow_rate]

    def solve(self, time=30, start_node='AA', good_valves=None):
        """Calculate the optimal pressure relieved.

        :param int time: Number of minutes available to solve the puzzle, defaults to 30
        :param start_node: The label for the node which players start at, defaults to 'AA'
        :param int players: Number of players available (just me, or elephant too?), defaults to 1
        :param tuple[str] open_valves: Tuple of valves already opened by a previous player, optional

        :return int: The optimal pressure relieved
        """
        # create initial state
        state = State(time, start_node, 0, 0)
        best = self.score_state(state)
        to_explore = [state]

        # depth-first-search baybeee
        while to_explore:
            state = to_explore.pop()
            score = self.score_state(state)
            best = max(best, score)

            # determine where we can go from this state
            options = [
                self.next_state(state, v)
                for v in good_valves
                if (not self.bitmasks[v] & state.open_valves) and (self.graph.get_distance(state.pos, v) < state.t)
            ]

            for next_state in options:
                to_explore.append(next_state)

        return best

    def solve_part_2(self, time: int, start_node: str, players: int, valves: list[str]):
        pass


arg_parser = ArgumentParser('python -m 16.main 16', description="Advent of Code Day 16")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    graph = ValveGraph.parse(line for line in parse_input(argus.input_path))
    graph.map_paths()
    print(graph)  # to test parsing

    solver = Solver(graph)
    if argus.part == 1:
        print(solver.solve(30, 'AA', solver.good_valves))
    elif argus.part == 2:
        print(solver.solve_part_2(26, 'AA', 2, solver.good_valves))
