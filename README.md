This is a repo of my solutions to (Advent of Code)[http://adventofcode.com/]

Dependencies:
- Pyenv
- Poetry
- Mustache (`npm install -g mustache`)

To Install for the year:

- Make sure you have the pyenv version installed (current 3.12)
- make sure you have poetry installed
- do `poetry install`

To start a day:

```
./start_day.sh <year> <day>
```

You can also pass in a class and object name as 3rd and 4th positionals, but the defaults are fine too: (Thing/thing)

run a test for a day:

```
./test.sh <year> <day>
```

run the main solution for the day:

```
./go.sh <year> <day>
```
