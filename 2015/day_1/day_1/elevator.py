import fileinput

filename = 'input.txt'
lines = []

for line in fileinput.input(filename):
    lines.append(line)

commands = ''.join(lines)

floor = 0
for i in range(len(commands)):
    command = commands[i]
    if command == '(':
        floor += 1
    elif command == ')':
        floor -= 1

    if floor < 0:
        break;

print (i + 1)
