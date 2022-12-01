import fileinput

def who_has_most_cals(input_lines):
    sums = []
    so_far = 0
    for line in input_lines:
        if line == '':  # next elf
            sums.append(so_far)
            so_far = 0
            continue

        so_far += int(line)

    sums.append(so_far) # last elf

    return max(sums)

if __name__ == '__main__':
    input_lines = [line.strip() for line in fileinput.input()]
    print(who_has_most_cals(input_lines))
