import fileinput

filename = 'input.txt'


def calc_materials(dimensions):
    dimensions = line.split('x')
    length = int(dimensions[0])
    width = int(dimensions[1])
    height = int(dimensions[2])

    totals = {'paper': 0, 'ribbon': 0}

    # calculate side area
    front = height * width
    side = height * length
    top = length * width

    # calculate 'extra paper'
    extra = min([front, side, top])

    # calculate total paper needed
    totals['paper'] = extra + 2 * front + 2 * side + 2 * top

    # calculate perimeters
    front_perimeter = 2 * height + 2 * width
    side_perimeter = 2 * height + 2 * length
    top_perimeter = 2 * length + 2 * width

    # calculate wrapping ribbon needed
    totals['ribbon'] = min([front_perimeter, side_perimeter, top_perimeter])

    # calculate volume
    totals['ribbon'] += length * width * height

    return totals


paper = 0
ribbon = 0
for line in fileinput.input(filename):
    materials = calc_materials(line)
    paper += materials['paper']
    ribbon += materials['ribbon']


print(ribbon)
