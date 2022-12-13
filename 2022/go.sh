#! /bin/env bash

day=$1
input=$2
part=$3

if [[ -z "$part" ]]; then
  part="1"
fi

ADVENT_PART="$part" python $day/main.py $day/$input
