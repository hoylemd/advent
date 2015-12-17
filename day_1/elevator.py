import fileinput

lines = []

for line in fileinput.input():
    lines.append(line)

for line in lines:
    print line
