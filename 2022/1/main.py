import fileinput

def cals_by_elf(input_lines):
    sums = []
    so_far = 0
    for line in input_lines:
        if line == '':  # next elf
            sums.append(so_far)
            so_far = 0
            continue

        so_far += int(line)

    sums.append(so_far) # last elf

    return sums

if __name__ == '__main__':
    input_lines = [line.strip() for line in fileinput.input()]
    cal_counts = sorted(cals_by_elf(input_lines), reverse=True)
    top_3 = cal_counts[0:3]
    print(sum(top_3))
