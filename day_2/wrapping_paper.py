import fileinput

filename = 'input.txt'

def calc_paper(length, width, height):
    length = int(length)
    width = int(width)
    height = int(height)

    front = height * width
    side = height * length
    top = length * width

    extra = min([front, side, top])

    return extra + 2 * front + 2 * side + 2 * top

paper = 0
for line in fileinput.input(filename):
    dimensions = line.split('x')
    paper += calc_paper(dimensions[0], dimensions[1], dimensions[2])

print paper
