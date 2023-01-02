import hashlib


def swing_pick(key, number):
    dig_spot = str(key) + str(number)
    ore_chunk = hashlib.md5(dig_spot)
    return ore_chunk.hexdigest()


def check_for_gold(chunk):
    return chunk.startswith('000000')


key = 'bgvyzdsv'
number = 0
while not check_for_gold(swing_pick(key, number)):
    number += 1

print(number)
