#! /usr/bin/env bash

year=$1
shift
day=$1
shift
class=$1
shift
obj=$1
shift

mkdir -p $year/$day

if [[ ! "$class" ]]; then
  class='Thing'
fi

if [[ ! "$obj" ]]; then
  obj='thing'
fi

cat << EOF > temp_data.json
{
  "year": $year,
  "day": $day,
  "class": "$class",
  "obj": "$obj"
}
EOF

mustache temp_data.json main.mustache > $year/$day/main.py
touch $year/$day/test.txt
touch $year/$day/test2.txt
touch $year/$day/input.txt

cat << EOF > $year/$day/answers.txt
test.txt 1 -
input.txt 1 -
test.txt 2 -
input.txt 2 -
EOF

rm temp_data.json

echo "Advent $year day $day ready"

code $year/$day/main.py
