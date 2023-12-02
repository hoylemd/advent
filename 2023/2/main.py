from argparse import ArgumentParser
from utils import logger, parse_input

QUERY_CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14
}


def parse_round(spec):
    round = {}
    for cube_spec in spec.split(', '):
        count, colour = cube_spec.split()
        round[colour] = int(count)

    return round


def parse_game(line, part=1):
    id, cube_spec = line.split(': ')
    id = int(id.split()[1])

    rounds = (parse_round(round_spec) for round_spec in cube_spec.split('; '))

    game = None
    for round in rounds:
        if game is None:
            game = round
            continue

        for colour, count in round.items():
            if game.get(colour, 0) < count:
                game[colour] = count

    return id, game


def is_game_valid(game):
    """if none of the game cube specs are > the same colour spec in query"""
    for colour, count in game.items():
        if count > QUERY_CUBES.get(colour, 0):
            return False

    return True


def sum_valid_games(lines, part=1):
    result = 0

    for id, game in (parse_game(line, part) for line in lines):
        logger.info(f"{id}, {game}")

        if is_game_valid(game):
            logger.info(f"Game {id} is valid")
            result += id

    return result


arg_parser = ArgumentParser('python -m 2023.2.main', description="Advent of Code 2023 Day 2")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    result = sum_valid_games(parse_input(argus.input_path), part=argus.part)

    print(f"answer:\n{result}")
