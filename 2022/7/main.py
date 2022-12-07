import fileinput

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def new_dir(*subdirs):
    return {'size': 0, 'subs': {sd: new_dir() for sd in subdirs}}


BIG_THRESH = 100_000


def parse_input():
    file_system = new_dir('/')
    prev_dir_stack = []
    current_dir = file_system
    smol_dirs = []


    for line in fileinput.input():
        parts = line.strip().split()

        debug(parts)
        if parts[0] == '$':
            if parts[1] == 'ls':
                continue
            if parts[1] == 'cd':
                if parts[2] == '..':
                    if current_dir['size'] <= BIG_THRESH:
                        smol_dirs.append(current_dir)

                    prev_dir = prev_dir_stack.pop()
                    prev_dir['size'] += current_dir['size']
                    current_dir = prev_dir
                else:
                    prev_dir_stack.append(current_dir)
                    current_dir = current_dir['subs'][parts[2]]
        elif parts[0] == 'dir':  # subdir
            current_dir['subs'][parts[1]] = new_dir()
        else: # file listing
            current_dir['size'] += int(parts[0])

    # step back out
    while prev_dir_stack:
        if current_dir['size'] <= BIG_THRESH:
            smol_dirs.append(current_dir)

        prev_dir = prev_dir_stack.pop()
        prev_dir['size'] += current_dir['size']
        current_dir = prev_dir


    return file_system, smol_dirs


if __name__ == '__main__':
    file_system, smol_dirs = parse_input()

    debug(file_system)

    print(sum(sd['size'] for sd in smol_dirs))
