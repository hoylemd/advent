import fileinput

filename = 'input.txt'
lines = []

for line in fileinput.input(filename):
    lines.append(line)

commands = ''.join(lines)

print commands.count('(') - commands.count(')')
