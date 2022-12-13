#! /bin/env bash

day=$1
input=$2
part=$3

if [[ -z "$part" ]] ; then
  part='1'
fi

set -x
ADVENT_PART="$part" python -m pdb $day/main.py $day/$input
