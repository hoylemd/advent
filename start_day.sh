#! /usr/bin/env bash

year=$1
shift
day=$1
shift
template='main.mustache'
if [[ "$1" == "--OO" ]]; then
  template='main_oo.mustache'
  shift
  class=$1
  shift
  obj=$1
  shift
else
  p1_function=$1
  shift
  doc_name=$1
  shift
  p2_function=$1
  shift
fi

mkdir -p $year/$day

if [[ ! "$class" ]]; then
  class='Thing'
fi

if [[ ! "$obj" ]]; then
  obj='thing'
fi

if [[ ! "$p1_function" ]]; then
  p1_function='answer_first_part'
fi

if [[ ! "$doc_name" ]]; then
  doc_name='lines'
fi

if [[ ! "$p2_function" ]]; then
  p2_function='answer_second_part'
fi

cat << EOF > temp_data.json
{
  "year": $year,
  "day": $day,
  "class": "$class",
  "obj": "$obj",
  "part_1_function": "$p1_function",
  "doc_name": "$doc_name",
  "part_2_function": "$p2_function"
}
EOF


mustache temp_data.json $template > $year/$day/main.py
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
