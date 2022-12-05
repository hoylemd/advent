import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def parse_input():
    state_lines = []
    instructions = []

    state_parsed = False

    for line in fileinput.input():

        if state_parsed:
            instructions.append(line.strip())
            continue

        if not line.strip():
            state_parsed = True
            continue

        state_lines.append(line[0:-1])

    return state_lines, instructions


def parse_state(lines):
    n_stacks = len(lines.pop().split())
    stacks = []
    for i in range(n_stacks):
        stacks.append([])

    while(lines):
        line = lines.pop()
        debug(f"processing {line}")
        for i in range(n_stacks):
            lbound = i * 4 + 1
            if len(line) < lbound:
                break # no more on this line
            crate = line[lbound]
            debug(f"{crate=}")
            if crate.strip():
                debug(f"adding [{crate}] to stack {i+1} ")
                stacks[i].append(crate)

    return stacks


def parse_instruction(instruction):
    parts = instruction.split()
    return int(parts[1]), int(parts[3]), int(parts[5])


def execute_program(state, instructions):
    for inst in instructions:
        n, src, dest = parse_instruction(inst)

        debug(f"move {n} cr8s from {src} to {dest}")
        gripped = state[src-1][-n:]
        state[src-1] = state[src-1][0:-n]
        state[dest-1] = state[dest-1] + gripped

        debug(state)

    return state


if __name__ == '__main__':
    state_lines, instructions = parse_input()

    state = parse_state(state_lines)

    state = execute_program(state, instructions)

    print(''.join(stack.pop() for stack in state))
