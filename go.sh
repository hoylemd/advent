#! /usr/bin/env bash

year=$1
shift
day=$1
shift
input=$1
shift
part=$1
shift

if [[ -z "$part" ]]; then
  part="1"
fi

python -m $year.$day.main $year/$day/$input $part $@
