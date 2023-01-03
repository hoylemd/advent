#! /usr/bin/env bash

VERBOSE=false
LOG_LEVEL=WARNING

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

year=$1
shift
day=$1
shift

if [[ "$1" ]]; then
  verb="$1"
  shift
  VERBOSE=true
  LOG_LEVEL=INFO
  if [[ "$verb" == 'vv' ]]; then
    LOG_LEVEL=DEBUG
  fi
fi

usage() {
  echo "Usage: test.txt <year> <day> [<verbose mode>]"
  echo "  year: The year for the challenge to test"
  echo "  day: The day for the challenge to test"
  echo "  verbose mode: put anything here to activate verbose mode (optional)"
  echo ''
}

test_solution() {
  year=$1
  shift
  day=$1
  shift
  input=$1
  shift
  part=$1
  shift
  answer=$1

  echo "y=$year d=$day i=$input p=$part a=$answer"
}

if [[ ! "$year" ]]; then
  echo "Please supply a year"
  usage
  exit 1
fi

if [[ ! "$day" ]]; then
  echo "Please supply a day"
  usage
  exit 1
fi

dir=$year/$day

if [ ! -d $dir ]; then
  echo "Please supply a valid year and day ($year day $day not found)"
  usage
  exit 1
fi

touch_answers() {
  year=$1
  shift
  day=$1
  cat << EOF > $year/$day/answers.txt
test.txt 1 -
input.txt 1 -
test.txt 2 -
input.txt 2 -
EOF
}

if [ ! -f $dir/answers.txt ]; then
  echo "Answers file could not be found for $year day $day. Please populate $year/$day/answers.txt"
  touch_answers $year $day
  exit 2
fi

passing=true
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Running tests for $year day $day:"

if [ "$VERBOSE" = true ]; then
  debug_msg=''
  if [[ "$LOG_LEVEL" == 'DEBUG' ]]; then
    debug_msg='(logs: debug)'
  fi

  printf "${RED}Verbose mode activated.${NC}$debug_msg\n"
fi

while read spec; do
  args=($spec)
  path=$year/$day/${args[0]}
  part=${args[1]}
  answer=${args[2]}
  if [[ "$answer" == '-' ]]; then
    if [ "$VERBOSE" = true ]; then
      echo "No answer supplied for $path part $part, skipping"
    fi
  else
    if [ "$VERBOSE" = true ]; then
      echo "Testing $path part $part:"
    fi
    result=$(LOG_LEVEL=$LOG_LEVEL python -m $year.$day.main $path $part | tail -n1)
    if [[ $result == $answer ]]; then
      printf "${GREEN}-${NC} $path part $part ${GREEN}PASSED${NC}\n"
    else
      printf "${RED}X${NC} $path part $part ${RED}FAILED${NC}\n"
      if [ "$VERBOSE" = true ]; then
        echo "  exp: $answer"
        echo "  act: $result"
      fi
      passing=false
    fi
  fi
done < $dir/answers.txt

if [[ "$passing" == true ]]; then
  printf "Tests ${GREEN}passed!${NC}\n"
else
  printf "Tests ${RED}FAILED!${NC} Check above output\n"
  exit 3
fi
