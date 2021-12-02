import fileinput

commands = [line.strip() for line in fileinput.input()]


def parse_command(command):
    parts = command.split()
    return parts[0], int(parts[1])


def follow_course(course, start_x=0, start_y=0):
    x = start_x
    y = start_y
    for direction, magnitude in (parse_command(command) for command in course):
        if direction == 'up':
            y -= magnitude
        elif direction == 'down':
            y += magnitude
        elif direction == 'forward':
            x += magnitude

    return x, y


end_x, end_y = follow_course(commands)

print(end_x * end_y)
