import fileinput

readings = [int(line.strip()) for line in fileinput.input()]

prev = None
increases = 0

for reading in readings:
    if prev is not None:
        if reading > prev:
            increases += 1
    prev = reading

print(increases)
