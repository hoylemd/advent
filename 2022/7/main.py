import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def new_dir(name, *subdirs):
    return {'size': 0, 'name': name, 'subs': {sd: new_dir(sd) for sd in subdirs}}


BIG_THRESH = 100_000


def parse_input():
    file_system = new_dir(None, '/')
    prev_dir_stack = []
    current_dir = file_system
    all_dirs = {}


    for line in fileinput.input():
        parts = line.strip().split()

        debug(parts)
        if parts[0] == '$':
            if parts[1] == 'ls':
                continue
            if parts[1] == 'cd':
                if parts[2] == '..':
                    all_dirs[current_dir['name']] = current_dir['size']

                    prev_dir = prev_dir_stack.pop()
                    prev_dir['size'] += current_dir['size']
                    current_dir = prev_dir
                else:
                    prev_dir_stack.append(current_dir)
                    current_dir = current_dir['subs'][parts[2]]
        elif parts[0] == 'dir':  # subdir
            current_dir['subs'][parts[1]] = new_dir(parts[1])
        else: # file listing
            current_dir['size'] += int(parts[0])

    # step back out
    while prev_dir_stack:
        all_dirs[current_dir['name']] = current_dir['size']

        prev_dir = prev_dir_stack.pop()
        prev_dir['size'] += current_dir['size']
        current_dir = prev_dir


    return file_system, all_dirs


TOTAL_SPACE = 70_000_000
NEEDED = 30_000_000


def find_target(file_system, all_dirs):
    inc_order = sorted(all_dirs.items(), key=lambda x: x[1])

    free_space = TOTAL_SPACE - file_system['size']

    for dir, size in inc_order:
        if free_space + size > NEEDED:
            debug(f"directory {dir} has {size}, which is enough")
            return size


if __name__ == '__main__':
    file_system, all_dirs = parse_input()

    debug(file_system)
    debug(all_dirs)
    print(find_target(file_system, all_dirs))
