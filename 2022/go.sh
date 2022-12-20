#! /bin/env bash

day=$1
shift
input=$1
shift
part=$1
shift

if [[ -z "$part" ]]; then
  part="1"
fi

if [ $day -lt 15 ]; then
  ADVENT_PART="$part" python -m $day.main $day/$input
else
  python -m $day.main $day/$input $part $@
fi
