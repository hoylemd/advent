import fileinput

def parse_input():
    return (line.strip().split(' ') for line in fileinput.input())

# A = rock; B = paper; C = scissors
# X = lose; Y = draw; Z = win
OUTCOME_MAP = {
    ('A', 'X'): 'scissors',
    ('A', 'Y'): 'rock',
    ('A', 'Z'): 'paper',
    ('B', 'X'): 'rock',
    ('B', 'Y'): 'paper',
    ('B', 'Z'): 'scissors',
    ('C', 'X'): 'paper',
    ('C', 'Y'): 'scissors',
    ('C', 'Z'): 'rock'
}
SHAPE_MAP = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}
OUTCOME_SCORE_MAP = {
    'X': 0,
    'Y': 3,
    'Z': 6
}

def score_round(them, outcome):
    my_throw = OUTCOME_MAP[them, outcome]
    return (OUTCOME_SCORE_MAP[outcome], SHAPE_MAP[my_throw])


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
