This is a repo of my solutions to [Advent of Code](http://adventofcode.com/)

Dependencies:
- Python > 3.10
- Mustache (`npm install -g mustache`)

To start a day:

```
./start_day.sh <year> <day>
```

You can also pass in a class and object name as 3rd and 4th positionals, but the defaults are fine too: (Thing/thing)

TODO: tweak this to make it easier to prompt for the class/object names and solution method names etc
TODO: add standardized logging

run a test for a day:

```
./test.sh <year> <day>
```

run the main solution for the day:

```
./go.sh <year> <day> <input file> [<part #>]
```
