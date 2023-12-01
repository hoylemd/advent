#! /usr/bin/env bash

year=$1
shift
day=$1
shift
input=$1
shift
part=$1
shift

if [[ -z "$part" ]] ; then
  part='1'
fi

if [[ -z "$input" ]] ; then
  input='test.txt'
fi

PYTHONPATH="$(pwd)" python -m pdb $year/$day/main.py $year/$day/$input $part $@
