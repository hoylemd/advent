#! /usr/bin/env bash

year=$1
shift
day=$1
shift
template='main.mustache'

if [[ -z "$year" ]]; then
    echo "need a year"
    exit 1
fi

if [[ -z "$day" ]]; then
    echo "need a day"
    exit 1
fi

declare -A my_array

while IFS= read -r line; do
    IFS='=' read -r key value <<< "$line"
    my_array["$key"]="$value"
done <<EOF
year=$year
day=$day
class=Thing
obj=thing
doc_name=lines
element=element
p1_function=answer1
p2_function=answer2
EOF

# Parse key/value pairs and store them in the array
for arg in "$@"; do
    IFS='=' read -r key value <<< "$arg"
    echo "overriding $key = $value"
    my_array["$key"]="$value"
done

# Convert associative array to JSON format
json_data="{"
for key in "${!my_array[@]}"; do
    echo "converting $key : ${my_array[$key]}"
    json_data+="\"$key\":\"${my_array[$key]}\","
done
json_data="${json_data%,}"  # Remove trailing comma
json_data+="}"

echo "$json_data" > temp_data.json

mkdir -p "$year/$day"

mustache temp_data.json $template > "$year/$day/main.py"
touch "$year/$day/test.txt"
touch "$year/$day/test2.txt"
touch "$year/$day/input.txt"

cat << EOF > "$year/$day/answers.txt"
test.txt 1 -
input.txt 1 -
test.txt 2 -
input.txt 2 -
EOF

rm temp_data.json

echo "Advent $year day $day ready"

code "$year/$day/main.py"
