import fileinput

filename = 'test.txt'
# filename = 'input.txt'

elfs_drunken_directions = ""
for line in fileinput.input(filename):
    elfs_drunken_directions += line

x = 0
y = 0
happy_children = {(x, y): 1}

for drunk_direction in elfs_drunken_directions:
    if drunk_direction == '^':
        y += 1
    elif drunk_direction == '>':
        x += 1
    elif drunk_direction == 'v':
        y -= 1
    elif drunk_direction == '<':
        x -= 1

    gps = (x, y)
    happy_children[gps] = 1


print len(happy_children.keys())
