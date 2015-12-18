import hashlib


def swing_pick(key, number):
    digest = hashlib.md5(str(key) + str(number))
    return digest.hexdigest()


def check_for_gold(chunk):
    return chunk.startswith('00000')


key = 'abcdef'
number = 609043

print check_for_gold(swing_pick(key, number))
