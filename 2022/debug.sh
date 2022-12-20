#! /bin/env bash

day=$1
shift
input=$1
shift
part=$1
shift

if [[ -z "$part" ]] ; then
  part='1'
fi

set -x
if [ $day -lt 15 ]; then
  ADVENT_PART="$part" PYTHONPATH="$(pwd)" python -m pdb $day/main.py $day/$input
else
  PYTHONPATH="$(pwd)" python -m pdb $day/main.py $day/$input $part $@
fi
