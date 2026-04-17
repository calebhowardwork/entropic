# entropic

A tiny command-line tool that measures password entropy and estimates
brute-force crack time. Pure Python, no dependencies.

## Install

```sh
git clone https://github.com/calebhowardwork/entropic.git
cd entropic
python entropic.py 'my password'
```

Or drop `entropic.py` on your `PATH` and `chmod +x` it.

## Usage

```sh
# analyze a password passed as an argument
entropic.py 'CorrectHorseBatteryStaple'

# hidden prompt (recommended — keeps it out of shell history)
entropic.py

# read from stdin (piping)
echo -n 'hunter2' | entropic.py --stdin

# disable color
entropic.py --no-color 'abc123'
```

### Example output

```
length:         28 chars
character pool: 88 (lowercase, uppercase, digits, symbols)
brute-force:    180.9 bits
shannon:        4.2 bits (given this string)
crack time:     2.44e+36 years at 10B guesses/sec
rating:         very strong
```

## What it measures

- **brute-force bits** — `len(password) × log2(pool_size)`. The upper bound
  assuming an attacker only knows the character classes used.
- **shannon bits** — the information content of the literal string. Low
  Shannon relative to brute-force means the string is repetitive (e.g.
  `aaaaaaaa`) and a smart attacker may reach it faster.
- **crack time** — average time at 10 billion guesses/second (a modern
  GPU cluster against an unsalted fast hash).

## Caveats

This tool does not check against known-breached password lists or
dictionary attacks. A high entropy score is necessary but not sufficient;
real password managers and cracker tools (zxcvbn, hashcat rules) model
human patterns that pure entropy misses.

## Tests

```sh
python -m pytest test_entropic.py
```

## License

MIT
