#! /usr/bin/env bash

year=$1
shift
day=$1
shift

mkdir -p $year/$day

cat << EOF > temp_data.yml
---
year: $year
day: $day
---
EOF

mustache temp_data.yml main.mustache > $year/$day/main.py
touch $year/$day/problem.txt
touch $year/$day/test.txt
touch $year/$day/input.txt

rm temp_data.yml

echo "Advent $year day $day ready"
