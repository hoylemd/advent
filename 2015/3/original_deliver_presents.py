import fileinput

filename = 'input.txt'

elfs_drunken_directions = ""
for line in fileinput.input(filename):
    elfs_drunken_directions += line

santa = {'x': 0, 'y': 0}
robo = {'x': 0, 'y': 0}
happy_children = {(0, 0): 1}
gifter = santa

for drunk_direction in elfs_drunken_directions:
    if drunk_direction == '^':
        gifter['y'] += 1
    elif drunk_direction == '>':
        gifter['x'] += 1
    elif drunk_direction == 'v':
        gifter['y'] -= 1
    elif drunk_direction == '<':
        gifter['x'] -= 1

    gps = (gifter['x'], gifter['y'])
    happy_children[gps] = 1

    if gifter == santa:
        gifter = robo
    else:
        gifter = santa


print(len(happy_children.keys()))
