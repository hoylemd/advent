import fileinput

def parse_input():
    return (line.strip().split(' ') for line in fileinput.input())

# A, X = rock; B, Y = paper; C, Z = scissors
SCORE_MAP = {
    ('A', 'X'): 3,
    ('A', 'Y'): 6,
    ('A', 'Z'): 0,
    ('B', 'X'): 0,
    ('B', 'Y'): 3,
    ('B', 'Z'): 6,
    ('C', 'X'): 6,
    ('C', 'Y'): 0,
    ('C', 'Z'): 3
}
SHAPE_MAP = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

def score_round(them, me):
    return (SCORE_MAP[them, me], SHAPE_MAP[me])


if __name__ == '__main__':
    rounds = parse_input()

    total_score = 0
    for round in rounds:
        score, shape_val = score_round(*round)
        round_score = score + shape_val
        print(f"{round[0]} vs {round[1]}({shape_val}) -> {score} = {round_score}")
        total_score += round_score

    print()
    print(total_score)
